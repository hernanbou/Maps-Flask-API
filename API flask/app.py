from flask import Flask, jsonify, request, send_from_directory
import mimetypes

app = Flask(__name__)

maps = [
    {
        'id': 1,
        'owner': 'Chitãozinho e Xoxoró',
        'name' : 'Rancho Fundo',
        'image': 'img/farm_1.png'
    },
    {
        'id': 2,
        'owner': 'Menino da Porteira',
        'name' : 'Sérgio Reis',
        'image': 'img/farm_2.png'
    },
    {
        'id': 3,
        'owner': 'Seu Lobato',
        'name' : 'Sítio do Seu Lobato',
        'image': 'img/farm_3.png'
    },
    {
        'id': 4,
        'owner': 'Thiago Violeiro e Thalysson',
        'name' : 'Ranchinho',
        'image': 'img/farm_4.png'
    }
]

#Validar dados de entrada
def handle_map(data):
    required_fields = {'owner', 'name', 'image'}
    if not all(field in data for field in required_fields):
        return False
    if not isinstance(data['owner'], str) or not isinstance(data['name'], str) or not isinstance(data['image'], str):
        return False
    return True

#Consultar(todos)
@app.route('/maps', methods = ['GET'])
def get_maps():
    return jsonify(maps)

#Consultar(ID)
@app.route('/maps/<int:id>', methods=['GET'])
def get_map_id(id):
    for map in maps:
        if map.get('id') == id:
            return jsonify(map)
    return jsonify({'erro': 'Mapa não encontrado'}), 404
#Exibir Imagem por ID
@app.route('/maps/<int:id>/image', methods = ['GET'])
def get_map_img(id):
    for map in maps:
        if map.get('id') == id:
            try:
                filename = map['image'].split('/')[-1]
                mime_type = mimetypes.guess_type(map['image'])[0]
                return send_from_directory('img', filename, mimetype = mime_type)
            except FileNotFoundError:
                return jsonify({'erro':'Imagem não encontrada'}), 404
    return jsonify({'erro': 'Mapa não encontrado'}), 404
#Adicionar
@app.route('/maps', methods=['POST'])
def post_new_map():
    new_map = request.get_json()
    if not handle_map(new_map):
        return jsonify({'erro': 'Dados inválidos'}), 400
    new_map['id'] = max(map['id'] for map in maps) + 1 if maps else 1
    maps.append(new_map)
    return jsonify(new_map), 201

#Editar
@app.route('/maps/<int:id>', methods = ['PUT'])
def put_map_id(id):
    set_map = request.get_json()
    for i, map in enumerate(maps):
        if map.get('id') == id:
            set_map['id'] = map['id']
            maps[i].update(set_map)
            return jsonify(maps[i])
    return jsonify({'erro': 'Mapa não encontrado'}), 404

#Excluir
@app.route('/maps/<int:id>', methods=['DELETE'])
def delete_map(id):
    for i, map in enumerate(maps):
        if map.get('id') == id:
            del maps[i]
            return jsonify(maps)
    return jsonify({'erro': 'Mapa não encontrado'}), 404

app.run(port=5000,host='localhost',debug=True)