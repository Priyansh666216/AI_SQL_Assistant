import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# DATABASE CONNECTION
# ============================================================
def get_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return connection


# ============================================================
# GET DATABASE SCHEMA
# ============================================================
def get_schema():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
    SELECT
        TABLE_NAME,
        COLUMN_NAME,
        DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    ORDER BY TABLE_NAME, ORDINAL_POSITION
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    schema = {}
    for table, column, data_type in rows:
        if table not in schema:
            schema[table] = []
        schema[table].append(f"{column} ({data_type})")
    return schema


# ============================================================
# GET FOREIGN KEYS
# ============================================================
def get_relationships():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
    SELECT
        TABLE_NAME,
        COLUMN_NAME,
        REFERENCED_TABLE_NAME,
        REFERENCED_COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = DATABASE()
      AND REFERENCED_TABLE_NAME IS NOT NULL
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    relationships = []
    for row in rows:
        relationships.append(f"{row[0]}.{row[1]} -> {row[2]}.{row[3]}")
    return relationships


# ============================================================
# EXECUTE SELECT QUERY
# ============================================================
def execute_query(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    connection.close()

    dataframe = pd.DataFrame(rows, columns=columns)
    return dataframe
