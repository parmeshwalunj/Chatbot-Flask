from flask import Blueprint, render_template, request
from flask_login import login_user, login_required, logout_user, current_user
from . import respond,check1,check2,wishme
import requests

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user, name=current_user.first_name, wish=wishme())

@views.route('/get')
@login_required
def get_bot_response():
    userText = request.args.get('msg')
    return str(check1(userText))