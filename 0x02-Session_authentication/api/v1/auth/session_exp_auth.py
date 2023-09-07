#!/usr/bin/env python3
"""
session auth expiration module
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    A session Auth expiration class
    """
    def __init__(self):
        """"
        initialize class
        """
        self.session_duration = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(self.session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        creates a session with duration
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[
            session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        link user id to session id
        """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if self.session_duration == 0:
            session_dict = self.user_id_by_session_id.get(session_id)
            return session_dict.get("user_id")
        if "created_at" not in self.user_id_by_session_id[session_id].keys():
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        expire_time = session_dict.get(
            "created_at") + timedelta(seconds=self.session_duration)
        if expire_time < datetime.now():
            return None
        return session_dict.get("user_id")
