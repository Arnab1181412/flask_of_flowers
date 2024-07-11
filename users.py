from flask import Flask, request, Blueprint
from postgre_data import CustomTable

users_bp = Blueprint('users',__name__)

       
@users_bp.route('/insert_user',methods=['POST'])
def new_user():
    users_table = CustomTable('users')
    payload = dict(request.json)
    insert_msg = users_table.insert(**payload)
    return insert_msg

@users_bp.route('/retrieve_all_users',methods=['GET'])
def retrieve_all_users():
    users_table = CustomTable('users').retrieve(**{'all':True})
    records = {}
    for entry in users_table:
        records[entry[0]] = {'name':entry[1],'profession':entry[2],'company':entry[3]}
    
    return records

@users_bp.route('/retrieve_user/<string:user_id>',methods=['GET'])
def retrieve_id(user_id):
    users_table = CustomTable('users').retrieve(**{'id':user_id,'all':False})
    records = {}
    for entry in users_table:
        records[entry[0]] = {'name':entry[1],'profession':entry[2],'company':entry[3]}
    
    return records

@users_bp.route('/update_user',methods=['POST'])
def update_user():
    users_table = CustomTable('users')
    payload = dict(request.json)
    update_msg = users_table.update(**payload)
    return update_msg



@users_bp.route('/delete_user/<string:user_id>',methods=['DELETE'])
def delete_user(user_id):
    users_table = CustomTable('users')
    del_msg = users_table.delete(**{'id':user_id})
    return del_msg


# if __name__=='__main__':
#     app.run(debug=True)