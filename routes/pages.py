import requests as rq

from flask import request
from flask import redirect
from flask import Blueprint
from flask import make_response
from flask import render_template


pages_bp = Blueprint("pages" , __name__)

@pages_bp.route("/" , methods=["GET"])
def home():
    return render_template("home.html")

@pages_bp.route("/signup" , methods=["GET"])
def signup():
    return render_template("signup.html")

@pages_bp.route("/signin" , methods=["GET"])
def signin():
    return render_template("signin.html")

@pages_bp.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/signin'))
    
    cookies = request.cookies
    for cookie in cookies:
        resp.set_cookie(cookie, '', expires=0)
    
    return resp

@pages_bp.route("/vote-details" , methods=["GET"])
def vote_details():
    return render_template("votes.html")