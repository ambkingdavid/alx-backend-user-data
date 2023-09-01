#!/usr/bin/env python3
"""
A module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """"
    password hashing
    """
    # generate a random salt
    salt = bcrypt.gensalt()

    # hash the password using the salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate if a password matches a stored hashed passwd
    """
    try:
        # Check if the provided password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except ValueError:
        # Handle invalid hashed_password gracefully
        return False
