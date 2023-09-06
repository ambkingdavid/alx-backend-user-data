#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for a given
        path based on excluded paths.
        """
        if path is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and\
              path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path.rstrip('/'):
                return False
        return False

    def authorization_header(self, request=None) -> str:
        """
        define the auth header
        """
        if request is None:
            return None
        try:
            auth = request.headers.get("Authorization")
            return auth
        except AttributeError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        define the current user
        """
        return None
