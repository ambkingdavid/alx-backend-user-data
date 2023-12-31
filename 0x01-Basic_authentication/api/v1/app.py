#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv("AUTH_TYPE")
excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/']

if auth_type == "auth":
    from api.v1.auth.basic_auth import Auth
    auth = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request():
    """
    function to be called before each request is handled
    """
    if auth is None:
        # auth.logger.info("auth is none")
        return

    if not auth.require_auth(request.path, excluded_paths):
        # auth.logger.info(f"request: {request.path}")
        return

    if auth.authorization_header(request) is None:
        # auth.logger.info("No header found")
        msg = {
                "error": "Unauthorized"
                }
        abort(401, msg)

    if auth.current_user(request) is None:
        # auth.logger.info("Cannot retrieve user")
        msg = {
                "error": "Forbidden"
                }
        abort(403, msg)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """
    Unauthorized handler
    """
    response = jsonify(error.description)
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """
    handle forbidden error
    """
    response = jsonify(error.description)
    response.status_code = 403
    return response


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
