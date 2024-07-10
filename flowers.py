from flask import Flask, request, jsonify, Blueprint
from data import CustomTable
# CRUD API
# pip freeze | grep package_name

flower_bp = Blueprint('flowers',__name__)

# you have a flower shop

# creation
# you're adding a flower to the inventory
# flower details: flower_name, flower_color, 
@flower_bp.route('/insert_flower',methods=['POST'])
def insert_flower():
    flowers_table = CustomTable('flowers')
    payload = dict(request.json)
    record = flowers_table.insert(**payload)
    return record

# retirieval
# you want all of the flowers in your inventory in two scenarios
# 1. all flowers in the DB
@flower_bp.route('/retrieve_all_flowers')
def retrieve_all_flowers():
    flowers_table = CustomTable('flowers')
    return flowers_table.retrieve(**{'all':True})

# 2. flowers with yellow color
@flower_bp.route('/retrieve_color_flowers/<string:flower_color>',methods=['GET'])
def retrieve_color_flowers(flower_color):
    flowers_table = CustomTable('flowers')
    data = flowers_table.retrieve(**{'all':True})
    retrieved_data = {flower_id:data[flower_id] for flower_id in data if data[flower_id].get('flower_color')==flower_color}
    return retrieved_data

# update
# update the color of the flower corresponding to a name
# @app.route('/modify_flowers/<string:flower_name>',defaults={'flower_color':None},methods=['PUT'])
@flower_bp.route('/modify_flowers',methods=['POST'])
def modify_flowers():
    flowers_table = CustomTable('flowers')
    payload = dict(request.json)
    update_record = flowers_table.update(**payload)
    return update_record

# deletion
@flower_bp.route('/delete_flowers/<string:flower_id>',methods=['DELETE'])
def delete_flowers(flower_id):
    flowers_table = CustomTable('flowers')
    del_data = flowers_table.delete(**{'id':flower_id})
    return del_data
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