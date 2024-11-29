from flask import request
from flask import jsonify
from flask import Response
from flask import Blueprint
from flask import make_response

from methods.database import Database

DATABASE = Database(db_name="database/election.db")


api_auth_bp = Blueprint("api_auth" , __name__)


@api_auth_bp.route("/auth/signup" , methods=["POST"])
def api_signup():
    data = request.json
    if data.get("name") and data.get("cnic") and data.get("password"):
        user = DATABASE.__signup__(data=data)
        if user:
            return jsonify({
                "error": False,
                "message": "Signup successful"
            })
        else:
            return jsonify({
                "error": True,
                "message": "CNIC already exists"
            })
    else:
        return jsonify({
            "error": True,
            "message": "All Details Not Provided"
        })
        
@api_auth_bp.route("/auth/signin" , methods=["POST"])
def api_signin():
    data = request.json
    if data.get("cnic") and data.get("password"):
        user = DATABASE.__login__(data=data)
        if user:
            response = make_response(jsonify({
                "error": False,
                "message": "Login Successful"
            }))
            
            response.set_cookie("session_key" , user.session_key , max_age=60*60*72)
            response.set_cookie("password" , data.get("password") , max_age=60*60*72)
            
            if user.national_vote:
                response.set_cookie("national_vote" , str(user.national_vote) , max_age=60*60*72)
            else:
                response.set_cookie("national_vote" , "" , max_age=60*60*72)
            
            if user.provincial_vote:
                response.set_cookie("provincial_vote" , str(user.provincial_vote) , max_age=60*60*72)
            else:
                response.set_cookie("provincial_vote" , "" , max_age=60*60*72)
                
            response.set_cookie("cnic" , user.cnic , max_age=60*60*72)
            return response
        
        else:
            return jsonify({
                "error": True,
                "message": "User does not exist"
            })
    else:
        return jsonify({
            "error": True,
            "message": "All Details Not Provided"
        })