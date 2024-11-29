import json

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask import make_response

from methods.database import Database

from routes.pages import pages_bp
from routes.api.auth import api_auth_bp
from routes.api.vote import api_vote_bp

app = Flask(__name__, template_folder="static/pages", static_folder="static")
CORS(app)

# All blueprints:
app.register_blueprint(pages_bp)
app.register_blueprint(api_auth_bp , url_prefix="/api")
app.register_blueprint(api_vote_bp , url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)