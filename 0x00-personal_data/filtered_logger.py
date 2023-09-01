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


def get_logger() -> logging.Logger:
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
    """establish a connection to db"""
    connection = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    return connection


def main():
    # Set up logging
    logger = get_logger()

    try:
        # Obtain a database connection
        connection = get_db()

        # Create a cursor
        cursor = connection.cursor(dictionary=True)

        # Retrieve all rows from the 'users' table
        cursor.execute("SELECT * FROM users")

        # Loop through each row
        for user in cursor.fetchall():
            log_message = "; ".join([f"{key}={value}" for key, value in user.items()])
            logger.info(log_message)

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# Ensure only the main function runs when the module is executed
if __name__ == "__main__":
    main()
