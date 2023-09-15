#!/usr/bin/env python3
"""
Main file
"""
import requests
from time import sleep


def register_user(email: str, password: str) -> None:
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    # Assert the expected status code
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    url = f"http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    # Assert the expected status code
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    url = f"http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    # Assert the expected status code
    assert response.status_code == 200

    # Return the session ID from the response JSON
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    url = f"http://localhost:5000/profile"
    response = requests.get(url)

    # Assert the expected status code
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    url = f"http://localhost:5000/profile"
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(url, headers=headers)

    # Assert the expected status code
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    url = f"http://localhost:5000/sessions"
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.delete(url, headers=headers)

    # Assert the expected status code (e.g., 200 OK for successful logout)
    assert response.json()['message'] == "Bienvenue"


def reset_password_token(email: str) -> str:
    url = f"http://localhost:5000/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)

    # Assert the expected status code (e.g., 200 OK for successful request)
    assert response.status_code == 200

    # Return the reset token from the response JSON
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f"http://localhost:5000/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)

    # Assert the expected status code
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    sleep(10)
    reset_token = None
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
