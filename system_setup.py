import os
import sys
import mysql
import mysql.connector

def token_files():
    print("not implemented")
    # sql_token = input('Passwort für den sql root: ')
    # google_token = input('Google mail token: ')
    # with open('sql/sql_token.py', 'a') as datei:
    #     datei.writelines(f"SQL_TOKEN = '{sql_token}'")
    # with open('scripts/token_google.py', 'a') as datei:
    #     datei.writelines(f"TOKEN = '{google_token}'")

def create_database():
    try:
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
    except mysql.connector.Error as err:
        print(f"Error: {err} -- no database created")

def delete_database():
    try:
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
    except mysql.connector.Error as err:
        print(f"Error: {err} -- no database created")

def rebuilt_database():
    delete_database()
    create_database()

if __name__ == '__main__':
    dic = {
        'add_token_files': token_files,
        'create_db': create_database,
        'delete_db': delete_database,
        'rebuilt_db': rebuilt_database
    }
    # setup_server.py


    if len(sys.argv) > 1:
        sys_input = sys.argv[1]
        if sys_input in dic:
            dic[sys_input]()
        else:
            print('not in command list')
            print('--------------')
            for i in dic:
                print(i)
    else:
        while ((i := input('aktion(quit zum beenden): ')) != 'quit'):
            if i in dic:
                dic[i]()
            else:
                print('not in command list')
                print('--------------')
                for i in dic:
                    print(i)