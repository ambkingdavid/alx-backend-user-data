#!/usr/bin/env python3
"""
session auth db module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    session auth from db_storage
    """
    def create_session(self, user_id=None):
        """
        create a session
        """
        session_id = super().create_session(user_id)
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        get user_id by requesting UserSession in db
        based on session_id
        """
        if not session_id:
            return None

        search = UserSession.search({"session_id": session_id})
        if len(search) == 0:
            return None
        user_session = search[0]
        if self.session_duration == 0:
            return user_session.user_id
        expire_time = user_session.created_at + timedelta(seconds=self.
                                                          session_duration)
        if expire_time < datetime.utcnow():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        destroys a user session based on session id
        """
        session_id = self.session_cookie(request)
        search = UserSession.search({"session_id": session_id})
        user_session = search[0]
        user_session.remove()
