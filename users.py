from flask import Flask, request, jsonify, Blueprint
from data import insert,delete,retrieve,update

users_bp = Blueprint('users',__name__)

       
@users_bp.route('/insert_user',methods=['POST'])
def new_user():

    payload = dict(request.json)
    record = insert('users',payload)
    return record

@users_bp.route('/retrieve_all_users',methods=['GET'])
def retrieve_all_users():
    return jsonify(retrieve('users',all_=True))

@users_bp.route('/retrieve_user/<string:user_id>',methods=['GET'])
def retrieve_id(user_id):

    record = retrieve('users',id_=user_id)
    return record

@users_bp.route('/update_user',methods=['POST'])
def update_user():

    payload = dict(request.json)
    update_record = update('users',payload)
    return update_record



@users_bp.route('/delete_user/<string:user_id>',methods=['DELETE'])
def delete_user(user_id):
    
    del_data = delete('users',user_id)
    return del_data


# if __name__=='__main__':
#     app.run(debug=True)