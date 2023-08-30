#!/usr/bin/env python3
"""
A module
"""

import re

def filter_datum(fields, redaction, message, separator):
    """
    obfuscated message method
    """
    pattern = fr'({separator.join(fields)})[^{separator}]*'
    return re.sub(pattern, redaction, message)
