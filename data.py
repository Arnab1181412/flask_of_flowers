from flask import Flask, jsonify, request

user_data = {'1':{'name':'Arnab Samanta','profession':'Data Scientist','company':'NVIDIA'}}

flower_data = {'1':{'flower_name':'Rose','flower_color':'Red'},
        '2':{'flower_name':'Sunflower','flower_color':'Yellow'}}

unified_data = {'users':user_data,
                'flowers':flower_data}

def insert(table_name,payload):

    max_id = int(max(unified_data[table_name].keys()))
    unified_data[table_name][f'{max_id+1}'] = payload
    
    return jsonify(payload)

def retrieve(table_name,id_=None,all_=False):
    if all_:
        return unified_data[table_name]
    return jsonify({id_:unified_data[table_name].get(id_,'Not Found!')})

def update(table_name,payload):
    id_ = payload.pop('id_')

    if id_ in unified_data[table_name]:
        unified_data[table_name].update({id_:payload})
        return jsonify({id_:unified_data[table_name][id_]})
    
    return jsonify({id_:f'Not present in {table_name} table'})

def delete(table_name,id_):
    
    del_data = unified_data[table_name].pop(id_,f'Not present in {table_name} table!')
    return jsonify({id_:del_data})


