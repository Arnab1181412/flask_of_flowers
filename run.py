# from flask import Flask, request, redirect
from flowers.main import app as flower_app
from users.main import app as user_app
from home import app as home_page
from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.serving import run_simple # werkzeug development server


if __name__ == "__main__":
    application = DispatcherMiddleware(home_page, {'/users': user_app,'/flowers':flower_app})
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True, use_evalex=True)

