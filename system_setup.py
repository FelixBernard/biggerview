import os
import mysql
import mysql.connector
from sql.sql_token import SQL_TOKEN

def token_files():
    print("not implemented")
    # sql_token = input('Passwort für den sql root: ')
    # google_token = input('Google mail token: ')
    # with open('sql/sql_token.py', 'a') as datei:
    #     datei.writelines(f"SQL_TOKEN = '{sql_token}'")
    # with open('scripts/token_google.py', 'a') as datei:
    #     datei.writelines(f"TOKEN = '{google_token}'")

def create_database():
    database = mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        passwd=os.environ.get('DB_PASSWORD'),
        auth_plugin='mysql_native_password'
    )
    try:
        curser = database.cursor()
        curser.execute('CREATE DATABASE biggerview')
    finally:
        curser.close()
        database.close()

if __name__ == '__main__':
    dic = {
        'add token files': token_files,
        'create db': create_database
    }
    while ((i := input('aktion(quit zum beenden): ')) != 'quit'):
        if i in dic:
            dic[i]()
        else:
            print('not in command list')
            print('--------------')
            for i in dic:
                print(i)