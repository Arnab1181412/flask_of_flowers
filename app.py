from flask import Flask
from flowers import flower_bp
from users import users_bp
app = Flask(__name__)

app.register_blueprint(flower_bp, url_prefix='/api')
app.register_blueprint(users_bp, url_prefix='/api')

@app.route('/')
def home():
    return "Central App - Use /api/flowers or /api/users"

if __name__ == '__main__':
    app.run(debug=True)