#!/usr/bin/env python3
"""
basic auth module
"""

import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    A BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extract base64 header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        decode the encoded header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
        except Exception:
            return None
        return decoded_string

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        extract email and password
        """
        if decoded_base64_authorization_header is None:
            return ((None, None))
        if not isinstance(decoded_base64_authorization_header, str):
            return ((None, None))
        if not (':' in decoded_base64_authorization_header):
            return ((None, None))
        user = decoded_base64_authorization_header.split(':')
        email = user[0]
        password = user[1]
        return ((email, password))
