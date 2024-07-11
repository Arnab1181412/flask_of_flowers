from flask import Flask, request, Blueprint
from data import CustomTable

users_bp = Blueprint('users',__name__)

       
@users_bp.route('/insert_user',methods=['POST'])
def new_user():
    users_table = CustomTable('users')
    payload = dict(request.json)
    record = users_table.insert(**payload)
    return record

@users_bp.route('/retrieve_all_users',methods=['GET'])
def retrieve_all_users():
    users_table = CustomTable('users')
    return users_table.retrieve(**{'all':True})

@users_bp.route('/retrieve_user/<string:user_id>',methods=['GET'])
def retrieve_id(user_id):
    users_table = CustomTable('users')
    record = users_table.retrieve(**{'id':user_id,'all':False})
    return record

@users_bp.route('/update_user',methods=['POST'])
def update_user():
    users_table = CustomTable('users')
    payload = dict(request.json)
    update_record = users_table.update(**payload)
    return update_record



@users_bp.route('/delete_user/<string:user_id>',methods=['DELETE'])
def delete_user(user_id):
    users_table = CustomTable('users')
    del_data = users_table.delete(**{'id':user_id})
    return del_data


# if __name__=='__main__':
#     app.run(debug=True)