from flask import Flask, request, render_template_string
# CRUD API
# pip freeze | grep package_name

app = Flask(__name__)

# you have a flower shop
data = {'1':{'flower_name':'Rose','flower_color':'Red'},
        '2':{'flower_name':'Sunflower','flower_color':'Yellow'}}

@app.route('/')
def flower_home_page():
    html = '''<h1>Welcome to Flowers app!!</h1>
              <h2>Use the following endpoints :-</h2>
                    <h2>1. /insert_flower - to insert a new flower.</h2>
                    <h2>2. /retrieve_all_flowers - to retrieve all flower database.</h2>
                    <h2>3. /retrieve_color_flowers/{flower_color} - to retrieve a certain colored flower.</h2>
                    <h2>4. /modify_flowers/flower_name/flower_color - to update a color of an existing flower.</h2>
                    <h2>5. /delete_color_flowers/{flower_color} - to delete a flower with a certain color.</h2>
                    <h2>6. /delete_flowers/{flower_color}/{flower_name} - to delete a flower with a certain color and name.</h2>
                
    '''         
    return render_template_string(html)
# creation
# you're adding a flower to the inventory
# flower details: flower_name, flower_color, 
@app.route('/insert_flower',methods=['POST'])
def insert_flower():

    max_id = int(max(data.keys()))
    new_flower = {'flower_name':request.json['flower_name'],'flower_color':request.json['flower_color']}
    data[f'{max_id+1}'] = new_flower
    
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
    retrieved_data = {}
    for flower_id in data:
        if data[flower_id].get('flower_color') == flower_color:
            retrieved_data[flower_id] = data[flower_id]
    if len(retrieved_data)!=0:
        return retrieved_data
    return f'No {flower_color} flowers are present in the database'

# update
# update the color of the flower corresponding to a name
# @app.route('/modify_flowers/<string:flower_name>',defaults={'flower_color':None},methods=['PUT'])
@app.route('/modify_flowers/<string:flower_name>/<string:flower_color>',methods=['PUT'])
def modify_flowers(flower_name,flower_color):
    c = 0
    for flower_id in data:
        if data[flower_id].get('flower_name')==flower_name:
            c += 1
            data[flower_id]['flower_color'] = flower_color
    if c != 0:
        return data
    return f'Flower with name {flower_name} is not present'

# deletion
# 1. delete all red flowers
@app.route('/delete_color_flowers/<string:flower_color>',methods=['DELETE'])
def delete_color_flowers(flower_color):
    original_len = len(data)
    keys = list(data.keys())
    for key in keys:
        if data[key]['flower_color']==flower_color:
            data.pop(key)
    if len(data)<original_len:
        return f'Flower with color {flower_color} are deleted.'
    return 'Flower with specified colour is not present'

# 2. delete flower with name "kurtosis" and color red
@app.route('/delete_flowers/<string:flower_color>/<string:flower_name>',methods=['DELETE'])
def delete_flowers(flower_color,flower_name):
    original_len = len(data)
    keys = list(data.keys())
    for key in keys:
        if (data[key]['flower_color']==flower_color) and (data[key]['flower_name']==flower_name):
            data.pop(key)
    if len(data)<original_len:
        return f'Flower with color {flower_color} and {flower_name} are deleted.'
    return 'Flower with specified colour is not present'


if __name__=='__main__':
    app.run(debug=True)