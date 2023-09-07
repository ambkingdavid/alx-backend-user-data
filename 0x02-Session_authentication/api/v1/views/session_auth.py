#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
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
    response = make_response(jsonify(user.to_json()), 200)
    response.set_cookie(session_name, session_id)
    return response