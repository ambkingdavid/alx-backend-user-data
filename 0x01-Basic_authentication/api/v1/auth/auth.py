#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        define a require path method
        """
        if path is None or not excluded_paths:
            return True
        sanitized_excluded_paths = [p.rstrip('/') + '/'
                                    for p in excluded_paths]
        sanitized_path = path.rstrip('/') + '/'
        return sanitized_path not in sanitized_excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        define the auth header
        """
        if request is None:
            return None
        try:
            auth = request.headers.get("Authorization")
        except AttributeError:
            return None
        return auth

    def current_user(self, request=None) -> TypeVar('User'):
        """
        define the current user
        """
        return None
