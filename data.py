from flask import Flask, jsonify, request

user_data = {'1':{'name':'Arnab Samanta','profession':'Data Scientist','company':'NVIDIA'}}

flower_data = {'1':{'flower_name':'Rose','flower_color':'Red'},
        '2':{'flower_name':'Sunflower','flower_color':'Yellow'}}

unified_data = {'users':user_data,
                'flowers':flower_data}

class CustomTable:

    def __init__(self,table_name) -> None:
        self.table_name = table_name

    def insert(self,**kwargs):

        max_id = int(max(unified_data[self.table_name].keys()))
        unified_data[self.table_name][f'{max_id+1}'] = kwargs
        
        return kwargs

    def retrieve(self,**kwargs):
        if kwargs['all']:
            return unified_data[self.table_name]
        return jsonify({kwargs['id']:unified_data[self.table_name].get(kwargs['id'],'Not Found!')})

    def update(self,**kwargs):
        id_ = kwargs.pop('id')

        if id_ in unified_data[self.table_name]:
            unified_data[self.table_name].update({id_:kwargs})
            return {id_:unified_data[self.table_name][id_]}
        
        return {id_:f'Not present in {self.table_name} table'}

    def delete(self,**kwargs):
        
        del_data = unified_data[self.table_name].pop(kwargs['id'],f'Not present in {self.table_name} table!')
        return {kwargs['id']:del_data}


