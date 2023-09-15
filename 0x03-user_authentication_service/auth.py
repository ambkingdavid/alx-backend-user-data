#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt

from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """
    generate a uuid str
    """
    new_id = str(uuid4())
    return new_id


def _hash_password(password: str) -> bytes:
    """
    hash a password and return bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        initialize
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register a user into the db if not exist
        """
        try:
            user = self._db.find_user_by(email=email)
            msg = f"User {email} already exists"
            raise ValueError(msg)
        except NoResultFound:
            passwd = _hash_password(password)
            user = self._db.add_user(email, passwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate a login session
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_pwd = user.hashed_password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pwd):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        creates a session
        """
        try:
            user = self._db.find_user_by(email=email)
            id = _generate_uuid()
            self._db.update_user(user.id, session_id=id)
            return id
        except NoResultFound:
            pass
        return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        gets a user using the session id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int):
        """
        destroys a session
        """
        user = self._db.find_user_by(id=user_id)
        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        get reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            id = _generate_uuid()
            self._db.update_user(user.id, reset_token=id)
        except NoResultFound:
            raise ValueError
        return id

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
