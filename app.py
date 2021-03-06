from aioflask import *
from flask import send_from_directory
import os
import json
from flask_cors import CORS, cross_origin

import time
from tinydb import TinyDB, Query

app = Flask(__name__)

cors = CORS(app, resources={r"/post": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

chats_db = TinyDB('database/chats.json')
users_db = TinyDB('database/users.json')
query = Query()

def register(data):
    if users_db.search(query.username == data['username']):
        return {'answer': 'this username already busy.'}
    else:
        users_db.insert({"username" : data['username'], 'chats': [], 'password': data['password']})
        return {'answer': 'account successfully created!'}
def login(data):
    user = users_db.search(query.username == data['username'])[0]
    print(user)
    if not user: 
        return {'answer': f"No account with username {data['username']}"}
    if user['password'] == data['password']:
        return {'answer': 'Succesfully logged!'}
    else:
        return {'answer': 'Wrong password!'}
def user_search(selector):
    users = users_db.search(query.username == selector)
    if len(users) > 0:
        return users
    else:
        return 'not found'

@app.route('/post', methods=['POST','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def post():
    content = request.json
    if content['type'] == 'register':
        return jsonify(register(content))
    elif content['type'] == 'login':
        return jsonify(login(content))
    elif content['type'] == 'user-search':
        return jsonify(user_search(content['selector']))
        
    return jsonify({'answer': 'default'})
    
@app.route("/", methods=['GET'])
async def index():
    html = open('index.html')
    return html.read()

@app.route("/script",  methods=['GET'])
async def script():
	return send_file("index.js")

@app.route("/data", methods=['GET'])
async def data():
    db = open('database/db.json')
    return jsonify(db.read())

@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)

app.run(host="0.0.0.0", port=5000, static_url_path='')

    
# from tinydb import TinyDB, Query

# chats = TinyDB('database/chats.json')
# users = TinyDB('database/users.json')
# query = Query()
# # users.insert({'name': 'Igor', "chats": [1,2]})
# # chats.insert({'id': 2, 'leghth': 36})
# # chats.insert({"chats": chats.search(query.name == "Igor")[0]["chats"].append(3)}, query.name == "Igor" )
# chats_array = users.search(query.name == "Igor")[0]['chats']
# chats_array.append(6)
# print(chats_array)
# users.update({"chats": chats_array}, query.name == 'Igor')

# print(chats.all())
# print(users.all())