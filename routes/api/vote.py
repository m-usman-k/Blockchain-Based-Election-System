from flask import request
from flask import jsonify
from flask import redirect
from flask import Response
from flask import Blueprint
from flask import make_response

from methods.database import Database

DATABASE = Database(db_name="database/election.db")


api_vote_bp = Blueprint("api_vote" , __name__)


@api_vote_bp.route("/vote/get-candidates" , methods=["POST"])
def api_get_candidates():
    data = request.json
    if (data.get("cnic") and data.get("password")):
        user = DATABASE.__login__(data=dict(data))
        if user:
            return jsonify(DATABASE.__get_all_candidates__())
            
    response = make_response(redirect("/logout"))
    return response

@api_vote_bp.route("/vote/post-vote" , methods=["POST"])
def api_post_vote():
    data = request.json
    
    if (data.get("cnic") and data.get("password") and data.get("poll_id")):
        user = DATABASE.__post_vote__(cnic=data.get("cnic") , password=data.get("password") , poll_id=data.get("poll_id"))
        if user:
            response = make_response(jsonify({
                "error": False,
                "message": "Vote posted successfully"
            }))
            
            response.set_cookie("national_vote" , str(user.national_vote) , max_age=60*60*72)
            response.set_cookie("provincial_vote" , str(user.provincial_vote) , max_age=60*60*72)
            return response
    
    response = make_response(redirect("/logout"))
    return response

@api_vote_bp.route('/vote/get-vote-details', methods=['POST'])
def get_vote_details():
    data = request.json
    cnic = data.get('cnic')
    password = data.get('password')

    user = DATABASE.__login__({"cnic":cnic, "password":password})
    if not user:
        return jsonify({"error": True, "message": "Invalid session"}), 403

    candidate = DATABASE.__get_one_candidate__(poll_id=user.provincial_vote)
    return_data = {
        "error": False,
        "voter_name": user.name,
        "cnic": user.cnic,
        "candidate_name": candidate.name,
        "party": candidate.party,
        "poll_id": candidate.poll_id,
    }
    print(return_data)
    return jsonify(return_data)
