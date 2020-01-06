__author__ = 'teemu kanstren'

#https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html

import mysql.connector as mariadb
from mysql.connector import errorcode
import os

DB_NAME = "xmr"
CREATE_DB_SQL = "CREATE DATABASE IF NOT EXISTS "+DB_NAME+" DEFAULT CHARACTER SET 'utf8'"
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PW = os.environ['DB_USER_PW']

def create_database(cnx, cursor):
    try:
        cursor.execute(f"USE {DB_NAME}")
        print(f"Using existing DB {DB_NAME}")
    except mariadb.Error as err:
        print(f"Database {DB_NAME} does not exists.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute(CREATE_DB_SQL)
            except mariadb.Error as err:
                print(f"Failed creating database: {err}")
                exit(1)
            print(f"Database {DB_NAME} created successfully.")
            cnx.database = DB_NAME
            cursor.execute(f"USE {DB_NAME}")
            print(f"Using existing DB {DB_NAME}")
        else:
            print(err)
            exit(1)

def create_tables(cursor):
    my_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{my_path}/create_tables.sql', 'r') as file:
        sql = file.read()
    tables_sql = sql.split(";")
    tables_sql = [table_sql.strip() for table_sql in tables_sql]
    for table_sql in tables_sql:
        if len(table_sql) < 10:
            #skip any short cruft created by split()
            continue
        print(f"Creating table:\n{table_sql}")
        try:
            cursor.execute(table_sql)
            #it is quite confusing, but apparently even with autocommit off, you do not need to commit a create db or create table command
            #due to some property, those are autocommitted and non-rollbackable: https://stackoverflow.com/questions/4692690/is-it-possible-to-roll-back-create-table-and-alter-table-statements-in-major-sql
        except mariadb.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def main():
    cnx = mariadb.connect(host=DB_HOST,
                                         user = DB_USER, password = DB_PW,  autocommit = False)
#                                         user = DB_USER, password = DB_PW, database = DB_NAME)
    cursor = cnx.cursor()
    create_database(cnx, cursor)
    create_tables(cursor)
    # https://stackoverflow.com/questions/11583083/python-commands-out-of-sync-you-cant-run-this-command-now
    cursor.close()
    cursor = cnx.cursor()
    #cursor.execute("USE "+sql.DB_NAME)
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    print(result)
    cursor.close()
    cnx.close()

if __name__== "__main__":
  main()


