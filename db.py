"""MySQL connection and schema setup helpers."""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = os.getenv("MYSQL_DATABASE", "student_result_db")


def _settings(include_database=True):
    settings = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
    }
    if include_database:
        settings["database"] = DATABASE
    return settings


def initialize_database():
    """Create the configured database and table when they do not exist."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**_settings(include_database=False))
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DATABASE.replace('`', '``')}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cursor.execute(f"USE `{DATABASE.replace('`', '``')}`")
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS students (
                roll_no VARCHAR(30) PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                semester VARCHAR(30) NOT NULL,
                python INT NOT NULL,
                dbms INT NOT NULL,
                software_engineering INT NOT NULL,
                mathematics INT NOT NULL,
                computer_networks INT NOT NULL,
                total INT NOT NULL,
                percentage DECIMAL(5,2) NOT NULL,
                grade VARCHAR(2) NOT NULL,
                result VARCHAR(10) NOT NULL,
                CONSTRAINT chk_python CHECK (python BETWEEN 0 AND 100),
                CONSTRAINT chk_dbms CHECK (dbms BETWEEN 0 AND 100),
                CONSTRAINT chk_software_engineering CHECK (software_engineering BETWEEN 0 AND 100),
                CONSTRAINT chk_mathematics CHECK (mathematics BETWEEN 0 AND 100),
                CONSTRAINT chk_computer_networks CHECK (computer_networks BETWEEN 0 AND 100)
            )"""
        )
        connection.commit()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def get_connection():
    """Open a connection to the configured student result database."""
    return mysql.connector.connect(**_settings())


def is_database_error(error):
    return isinstance(error, Error)
