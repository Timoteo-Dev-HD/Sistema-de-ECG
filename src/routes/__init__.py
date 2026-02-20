from flask import Blueprint, render_template

web = Blueprint('web', __name__)

@web.route('/')
def home():
    return render_template("login.html")

def register_routes(app):
    app.register_blueprint(web)
