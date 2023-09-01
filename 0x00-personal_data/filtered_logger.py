#!/usr/bin/env python3
"""
A module
"""

import re
import logging
import os
import mysql.connector
from typing import List, Optional, Any, Union

PII_FIELDS = ("name", "email", "phone", "password", "ssn")

USERNAME: str = os.getenv("PERSONAL_DATA_DB_USERNAME")
PASSWORD: str = os.getenv("PERSONAL_DATA_DB_PASSWORD")
HOST: str = os.getenv("PERSONAL_DATA_DB_HOST")
DATABASE: str = os.getenv("PERSONAL_DATA_DB_NAME")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        initialise
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formatter
        """
        filtered_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            filtered_message, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    filter method
    """
    pattern = fr'({"|".join(fields)})=[^{separator}]+'
    filter_mess = re.sub(pattern, f'\\1={redaction}', message)
    return filter_mess


def get_logger(none) -> logging.Logger:
    """ Return a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler with the RedactingFormatter
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """:returns a secured connection"""
    connection = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    return connection
