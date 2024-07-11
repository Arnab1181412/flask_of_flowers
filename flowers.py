from flask import Flask, request, Blueprint
from postgre_data import CustomTable
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
    insert_msg = flowers_table.insert(**payload)
    return insert_msg

# retirieval
# you want all of the flowers in your inventory in two scenarios
# 1. all flowers in the DB
@flower_bp.route('/retrieve_all_flowers')
def retrieve_all_flowers():
    flowers_table = CustomTable('flowers').retrieve(**{'all':True})
    records = {}
    for entry in flowers_table:
        print(entry)
        records[entry[0]] = {'flower_name':entry[1],'flower_color':entry[2]}
    
    return records

# 2. flowers with yellow color
@flower_bp.route('/retrieve_color_flowers/<string:flower_color>',methods=['GET'])
def retrieve_color_flowers(flower_color):
    flowers_table = CustomTable('flowers').retrieve(**{'all':True})
    records = {}
    for entry in flowers_table:
        records[entry[0]] = {'flower_name':entry[1],'flower_color':entry[2]}
    retrieved_data = {flower_id:records[flower_id] for flower_id in records if records[flower_id].get('flower_color')==flower_color}
    return retrieved_data

# update
# update the color of the flower corresponding to a name
# @app.route('/modify_flowers/<string:flower_name>',defaults={'flower_color':None},methods=['PUT'])
@flower_bp.route('/modify_flowers',methods=['POST'])
def modify_flowers():
    flowers_table = CustomTable('flowers')
    payload = dict(request.json)
    update_msg = flowers_table.update(**payload)
    return update_msg

# deletion
@flower_bp.route('/delete_flowers/<string:flower_id>',methods=['DELETE'])
def delete_flowers(flower_id):
    flowers_table = CustomTable('flowers')
    del_msg = flowers_table.delete(**{'id':flower_id})
    return del_msg
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