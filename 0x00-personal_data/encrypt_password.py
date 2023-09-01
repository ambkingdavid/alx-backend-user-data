#!/usr/bin/env python3
"""
A module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """"
    password hashing
    """
    #generate a random salt
    salt = bcrypt.gensalt()

    #hash the password using the salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password