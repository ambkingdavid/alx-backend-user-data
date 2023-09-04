#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views
import json

# Create a dictionary with the desired structure
error_data = {
    "error": "Unauthorized"
}

# Convert the dictionary to a JSON string with indentation
json_string = json.dumps(error_data, indent=2)

# Print the JSON string
print(json_string)



@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', strict_slashes=False)
def unauthorised() -> str:
    """
    GET /api/v1/unauthorised
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'])
def trigger_forbidden_error():
    """
    GET /api/v1/forbidden
    """
    abort(403)
