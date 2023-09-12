#!/usr/bin/env python3
"""
flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

app = Flask(__name__)

AUTH = Auth()


@app.route('/')
def welcome():
    """
    root route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    create a user if not exist
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
        })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    session login authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({
        "email": email,
        "message": "logged in"
    })
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    logout from session
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """
    get user profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    reset password
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    updates a user's password
    """
    email = request.form.get('email')
    reset_token = request.form.get('request_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
