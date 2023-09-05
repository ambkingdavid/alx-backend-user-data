#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, Response
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    msg = {
        "status": "OK"
    }
    return jsonify(msg)


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
    msg = {
        "error": "Unauthorized"
    }
    abort(401, msg)


@app_views.route('/forbidden', methods=['GET'])
def trigger_forbidden_error() -> str:
    """
    GET /api/v1/forbidden
    """
    msg = {
        "error": "Forbidden"
    }
    abort(403, msg)
