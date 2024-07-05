from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template_string('<h1>Welcome to home page. Please use "/users" and "/flowers" to access respective endpoints.</h1>')

if __name__=='__main__':
    app.run(debug=True)