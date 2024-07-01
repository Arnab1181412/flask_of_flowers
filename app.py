from flask import Flask, redirect, url_for, request
# CRUD API
# pip freeze | grep package_name

app = Flask(__name__)

# you have a flower shop
data = [{'flower_name':'Rose','flower_color':'Red'},
        {'flower_name':'Sunflower','flower_color':'Yellow'}]
# deletion
# 1. delete all red flowers
@app.route('/delete_color_flowers/<string:flower_color>',methods=['DELETE'])
def delete_color_flowers(flower_color):
    tobe_deleted = []
    for item in data:
        if item['flower_color'] == flower_color:
            tobe_deleted.append(item)
    for item in tobe_deleted:
        data.remove(item)
    if len(tobe_deleted)!=0:
        return f'Flower with color {flower_color} are deleted.'
    return 'Flower with specified colour is not present'

# 2. delete flower with name "kurtosis" and color red
@app.route('/delete_flowers/<string:flower_color>/<string:flower_name>',methods=['DELETE'])
def delete_flowers(flower_color,flower_name):
    tobe_deleted = []
    for item in data:
        if (item['flower_color'] == flower_color) and (item['flower_name'] == flower_name):
            tobe_deleted.append(item)
    for item in tobe_deleted:
        data.remove(item)
    if len(tobe_deleted)!=0:
        return f'Flower with color {flower_color} and {flower_name} are deleted.'
    return 'Flower with specified colour is not present'

# creation
# you're adding a flower to the inventory
# flower details: flower_name, flower_color, 
@app.route('/insert_flower',methods=['POST'])
def insert_flower():
    new_flower = {'flower_name':request.json['flower_name'],'flower_color':request.json['flower_color']}
    data.append(new_flower)
    return new_flower
# retirieval
# you want all of the flowers in your inventory in two scenarios
# 1. all flowers in the DB
@app.route('/retrieve_all_flowers')
def retrieve_all_flowers():
    return data
# 2. flowers with yellow color
@app.route('/retrieve_color_flowers/<string:flower_color>',methods=['GET'])
def retrieve_color_flowers(flower_color):
    retrieved_data = []
    for item in data:
        if item['flower_color'] == flower_color:
            retrieved_data.append(item)
    if len(retrieved_data)!=0:
        return retrieved_data
    return f'No {flower_color} flowers are present in the database'

# update
# update the color of the flower corresponding to a name
@app.route('/modify_flowers/<string:flower_name>/<string:flower_color>',methods=['PUT'])
def modify_flowers(flower_name,flower_color):
    c = 0
    for item in data:
        if item['flower_name']==flower_name:
            c += 1
            item['flower_color'] = flower_color
    if c != 0:
        return data
    return f'Flower with name {flower_name} is not present'



if __name__=='__main__':
    app.run(debug=True)