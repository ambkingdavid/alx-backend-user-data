#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    authenticate user session
    """
    email = request.form.get('email', None)
    if email == "" or email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password == "" or password is None:
        return jsonify({"error": "password missing"}), 400

    user_search = User.search({"email": email})
    if len(user_search) == 0:
        msg = "no user found for this email"
        return jsonify({"error": msg}), 404
    user = user_search[0]
    if not (user.is_valid_password(password)):
        return jsonify({"error": "wrong password"}), 401
    user_id = user.id
    if user_id:
        from api.v1.app import auth
    session_id = auth.create_session(user_id)
    session_name = os.getenv("SESSION_NAME")
    resp = jsonify(user.to_json())
    resp.set_cookie(session_name, session_id)
    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    """
    log user out and close the session
    """
    from api.v1.app import auth
    session = auth.destroy_session(request)
    if not session:
        abort(404)
    return jsonify({}), 200