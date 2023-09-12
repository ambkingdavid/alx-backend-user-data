#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt

from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
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
            passwd = self._hash_password(password)
            user = self._db.add_user(email, passwd)
            self._db._session.add(user)
            self._db._session.commit()
            return user

    def _hash_password(self, password: str) -> bytes:
        """
        hash a password and return bytes
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    def valid_login(self, email: str, password: str) -> bool:
        """
        validate a login session
        """
        try:
            user = self._db.find_user_by(email=email)
            pwd = password.encode('utf-8')
            if bcrypt.checkpw(pwd, user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def _generate_uuid(self) -> str:
        """
        generate a uuid str
        """
        new_id = str(uuid4())
        return new_id

    def create_session(self, email: str) -> str:
        """
        creates a session
        """
        try:
            user = self._db.find_user_by(email=email)
            id = self._generate_uuid()
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