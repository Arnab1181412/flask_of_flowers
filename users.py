from pymongo import MongoClient
from flask import Flask, request, Blueprint, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.environ.get('MONGO_URI')
cluster = MongoClient('MONGO_URI')
db = cluster['flask-of-flowers']
users_col = db['users']
users_bp = Blueprint('users',__name__)

def get_last_user_id():
    last_user_id = users_col.find().sort([('user_id',-1)]).limit(1)
    try:
        last_user_id = last_user_id[0]['user_id']
    except:
        last_user_id = 0

    return last_user_id
       
@users_bp.route('/insert_user',methods=['POST'])
def new_user():
    name = request.json['name']
    profession = request.json['profession']
    company = request.json['company']
    last_user_id = get_last_user_id()
    curr_user_id = last_user_id + 1
    user_dict = {
        'user_id':curr_user_id,
        'name':name,
        'profession':profession,
        'company':company
    }
    users_col.insert_one(user_dict)
    return {'msg':'user inserted successfully'}

@users_bp.route('/retrieve_all_users',methods=['GET'])
def retrieve_all_users():
    users = users_col.find()
    user_list = []
    for user in users:
        user_dict = {
        'user_id':user['user_id'],
        'name':user['name'],
        'profession':user['profession'],
        'company':user['company']
        }
        user_list.append(user_dict)

    return jsonify(user_list)

@users_bp.route('/retrieve_user/<string:user_id>',methods=['GET'])
def retrieve_id(user_id):
    user = users_col.find_one({'user_id':int(user_id)})
    user_dict = {
        'user_id':user['user_id'],
        'name':user['name'],
        'profession':user['profession'],
        'company':user['company']
    }
    return user_dict

@users_bp.route('/update_user/<string:user_id>',methods=['POST'])
def update_user(user_id):
    payload = dict(request.json)
    users_col.update_many({'user_id':int(user_id)},{'$set':payload})

    return {'msg':f'user {user_id} updated successfully'}



@users_bp.route('/delete_user/<string:user_id>',methods=['DELETE'])
def delete_user(user_id):
    users_col.delete_many({'user_id':int(user_id)})
    return {'msg':'User deleted successfully'}


# if __name__=='__main__':
#     app.run(debug=True)