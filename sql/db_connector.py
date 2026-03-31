import mysql.connector
from sql.sql_token import SQL_TOKEN

main_db_plus_database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=SQL_TOKEN,
    database="muj",
    auth_plugin='mysql_native_password',
    autocommit=False
)

def generate_connector(host:str, user:str, explicit_db:bool=None, db_name:str=None):
    generated_db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=SQL_TOKEN,
        auth_plugin='mysql_native_password'
    )
    if explicit_db:
        generated_db.database = db_name

    return generated_db