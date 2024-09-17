from pymongo import MongoClient
from flask import Flask, request, Blueprint, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.environ.get('MONGO_URI')
cluster = MongoClient('MONGO_URI')
db = cluster['flask-of-flowers']
flowers_col = db['flowers']# CRUD API
# pip freeze | grep package_name

flower_bp = Blueprint('flowers',__name__)

def get_last_flower_id():
    last_flower_id = flowers_col.find().sort([('flower_id',-1)]).limit(1)
    try:
        last_flower_id = last_flower_id[0]['flower_id']
    except:
        last_flower_id = 0

    return last_flower_id
# you have a flower shop

# creation
# you're adding a flower to the inventory
# flower details: flower_name, flower_color, 
@flower_bp.route('/insert_flower',methods=['POST'])
def insert_flower():
    flower_name = request.json['flower_name']
    flower_color = request.json['flower_color']
    last_flower_id = get_last_flower_id()
    curr_flower_id = last_flower_id + 1
    flower_dict = {
        'flower_id':curr_flower_id,
        'flower_name':flower_name,
        'flower_color':flower_color
        }
    
    flowers_col.insert_one(flower_dict)
    return {'msg':'flower inserted successfully'}

# retirieval
# you want all of the flowers in your inventory in two scenarios
# 1. all flowers in the DB
@flower_bp.route('/retrieve_all_flowers')
def retrieve_all_flowers():
    flowers = flowers_col.find()
    flower_list = []
    for flower in flowers:
        flower_dict = {
        'flower_id':flower['curr_flower_id'],
        'flower_name':flower['flower_name'],
        'flower_color':flower['flower_color']
        }
        flower_list.append(flower_dict)

    return jsonify(flower_list)

# 2. flowers with yellow color
@flower_bp.route('/retrieve_color_flowers/<string:flower_color>',methods=['GET'])
def retrieve_color_flowers(flower_color):
    flower = flowers_col.find_many({'flower_id':flower_color})
    flower_list = []
    for flower in flowers:
        flower_dict = {
        'flower_id':flower['curr_flower_id'],
        'flower_name':flower['flower_name'],
        'flower_color':flower['flower_color']
        }
        flower_list.append(flower_dict)

    return jsonify(flower_list)
    

# update
# update the color of the flower corresponding to a name
# @app.route('/modify_flowers/<string:flower_name>',defaults={'flower_color':None},methods=['PUT'])
@flower_bp.route('/modify_flowers/<string:flower_id>',methods=['POST'])
def modify_flowers(flower_id):
    payload = dict(request.json)
    flowers_col.update_many({'flower_id':int(flower_id)},{'$set':payload})

    return {'msg':f'flower {flower_id} updated successfully'}

# deletion
@flower_bp.route('/delete_flowers/<string:flower_id>',methods=['DELETE'])
def delete_flowers(flower_id):
    flowers_col.delete_many({'flower_id':int(flower_id)})
    return {'msg':'flower deleted successfully'}
# # 1. delete all red flowers
# @app.route('/delete_color_flowers/<string:flower_color>',methods=['DELETE'])
# def delete_color_flowers(flower_color):
#     pass

# # 2. delete flower with name "kurtosis" and color red
# @app.route('/delete_flowers/<string:flower_color>/<string:flower_name>',methods=['DELETE'])
# def delete_flowers(flower_color,flower_name):
#     pass


# if __name__=='__main__':
#     flower_bp.run(debug=True)