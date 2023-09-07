#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv("AUTH_TYPE")
excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/', '/api/v1/auth_session/login/']

if auth_type == "auth":
    from api.v1.auth.basic_auth import Auth
    auth = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()

# auth.logger = logging.getLogger()
# auth.logger.setLevel(logging.DEBUG)
# auth.logger.addHandler(logging.StreamHandler())


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

    if auth.authorization_header(request
                                 ) is None and auth.session_cookie(request
                                                                   ) is None:
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

    request.current_user = auth.current_user(request)


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
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
