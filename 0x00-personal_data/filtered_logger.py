#!/usr/bin/env python3
"""
A module
"""

import re


def filter_datum(fields, redaction, message, separator):
    # Create a regex pattern to match the specified fields and their values
    pattern = fr'({"|".join(map(re.escape, fields))})=[^;]+'
    
    # Use re.sub to replace the matched fields with redaction
    return re.sub(pattern, f'\\1={redaction}', message)
