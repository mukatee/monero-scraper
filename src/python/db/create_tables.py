__author__ = 'teemu kanstren'

#https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html

import mysql.connector as mariadb
from mysql.connector import errorcode
from db import sql

def create_database(cnx, cursor):
    try:
        cursor.execute(f"USE {sql.DB_NAME}")
        print(f"Using existing DB {sql.DB_NAME}")
    except mariadb.Error as err:
        print(f"Database {sql.DB_NAME} does not exists.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute(sql.CREATE_DB_SQL)
            except mariadb.Error as err:
                print(f"Failed creating database: {err}")
                exit(1)
            print(f"Database {sql.DB_NAME} created successfully.")
            cnx.database = sql.DB_NAME
        else:
            print(err)
            exit(1)

def create_tables(cursor):
    for table_name in sql.TABLES:
        table_description = sql.TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ", end = '')
            cursor.execute(table_description)
        except mariadb.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def main():
    cnx = mariadb.connect(host=sql.DB_HOST,
#                                         user = sql.DB_USER, password = sql.DB_PW)
                                         user = sql.DB_USER, password = sql.DB_PW, database = sql.DB_NAME)
    cursor = cnx.cursor()
    create_database(cnx, cursor)
    create_tables(cursor)
    #cursor.execute("USE "+sql.DB_NAME)
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    print(result)
    cursor.close()
    cnx.close()

if __name__== "__main__":
  main()


