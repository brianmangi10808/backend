from flask import Blueprint,render_template

main = Blueprint('main',__name__)

@main.route('/')
def home():
    return "home page"

@main.route('/profile')
def profile():
    return "login"