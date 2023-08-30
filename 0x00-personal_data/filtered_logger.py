#!/usr/bin/env python3
"""
A module
"""

import re
import logging
import os
import mysql.connector
from typing import List

PII_FIELDS = ("ip", "email", "phone", "password", "ssn")



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formatter
        """
        filtered_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            filtered_message, self.SEPARATOR)


def filter_datum(fields, redaction, message, separator):
    """
    filter method
    """
    pattern = fr'({"|".join(map(re.escape, fields))})=[^{separator}]+'
    return re.sub(pattern, f'\\1={redaction}', message)

def get_logger():
    """ Return a logging.Logger object """
    
    # Create the logger
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)  # Set the log level to INFO
    
    # Prevent messages from propagating to other loggers
    logger.propagate = False
    
    # Create a StreamHandler with the RedactingFormatter
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(handler)
    
    return logger

def get_db():
    """
    get database
    """
    # Retrieve database credentials from environment variables
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Check if the database name is provided
    if db_name is None:
        raise ValueError("PERSONAL_DATA_DB_NAME environment variable is not set.")

    # Create a connection to the database
    try:
        conn = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )
        return conn
    except mysql.connector.Error as err:
        # Handle any connection errors here
        print(f"Error: {err}")
        return None