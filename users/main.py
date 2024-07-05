from flask import Flask, request, render_template_string

app = Flask(__name__)

user_data = {'1':{'name':'Arnab Samanta','profession':'Data Scientist','company':'NVIDIA'}}

@app.route('/')
def user_home_page():
    html = '''<h1>Welcome to Users app!!</h1>
              <h2>Use the following endpoints :-</h2>
                    <h2>1. /insert (POST) - to insert a new user.</h2>
                    <h2>2. /retrieve_all (GET) - to retrieve all user database.</h2>
                    <h2>3. /retrieve/{user_id} (GET) - to retrieve a certain user_id.</h2>
                    <h2>4. /update (POST) - to update a user_id.</h2>
                    <h2>5. /delete/{user_id} (DELETE) - to delete a user_id.</h2>
                
    '''         
    return render_template_string(html)
@app.route('/insert',methods=['POST'])
def new_user():

    max_id = int(max(user_data.keys()))
    new_entry = {'name':request.json['name'],'profession':request.json['profession'],'company':request.json['company']}
    user_data[f'{max_id+1}'] = new_entry
    
    return new_entry

@app.route('/retrieve_all',methods=['GET'])
def retrieve_all_users():
    return user_data

@app.route('/retrieve/<string:user_id>',methods=['GET'])
def retrieve_id(user_id):

    return user_data.get(user_id,'User not Found!')

@app.route('/update',methods=['POST'])
def update_user():

    request_dict = dict(request.json)

    is_present = user_data.get(request_dict['user_id'],0)
    user_id = request_dict.pop('user_id')
    if is_present:
        print(request_dict)
        user_data[user_id].update(request_dict)
        return f'The user ID {user_id} has been updated.'

    return f'The {user_id} is not present in the database.'



@app.route('/delete/<string:user_id>',methods=['DELETE'])
def delete_user(user_id):
    
    if user_id in user_data:
        user_data.pop(user_id)
        return f'User {user_id} has been deleted.'
    return f'User with {user_id} not present in the database.'


if __name__=='__main__':
    app.run(debug=True)