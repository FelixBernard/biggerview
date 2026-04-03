# from sql.db_connector import *
import os
import mysql.connector
from sql.sql_token import SQL_TOKEN

def init_query(query, parameters=None):
    err = False
    database =  mysql.connector.connect(
        host=os.environ.get('DB_HOST') if os.environ.get('DB_HOST') == None else "localhost",
        user=os.environ.get('DB_USER') if os.environ.get('DB_USER') == None else "root",
        passwd=os.environ.get('DB_PASSWORD') if os.environ.get('DB_PASSWORD') == None else SQL_TOKEN,
        database=os.environ.get('DB_NAME') if os.environ.get('DB_NAME') == None else "biggerview",
        auth_plugin='mysql_native_password',
        autocommit=False
    )
    try:
        curser = database.cursor()
        curser.execute(query, parameters)
        database.commit()
    except Exception as e:
        err = str(e)
    finally:
        curser.close()
        database.close()
        return err

def insert_query(query, db=None):
    init_query(query, db)

def universel_db_query(query, with_col_names:bool=True, parameters:tuple=None):
    err = False
    database = mysql.connector.connect(
        host=os.environ.get('DB_HOST') if os.environ.get('DB_HOST') == None else "localhost",
        user=os.environ.get('DB_USER') if os.environ.get('DB_USER') == None else "root",
        passwd=os.environ.get('DB_PASSWORD') if os.environ.get('DB_PASSWORD') == None else SQL_TOKEN,
        database=os.environ.get('DB_NAME') if os.environ.get('DB_NAME') == None else "biggerview",
        auth_plugin='mysql_native_password',
        # autocommit=False
    )

    try:
        cursor = database.cursor()
        cursor.execute(query, parameters)
        
        # Spaltennamen abrufen
        column_names = [column[0] for column in cursor.description]
        
        results = []
        if with_col_names:
            results.append(dict(zip(column_names, column_names)))
        for row in cursor.fetchall():
            results.append(dict(zip(column_names, row)))

    except:
        results = [{"error": "error"}]
        err = True
    
    finally:
        cursor.close()
        database.close()
        return results, err
    
def universel_db_query_on_maindb(query):
    return universel_db_query(query)

#print(universel_db_query("select * from functable;"))

def insert_general_user_table(email, password) -> bool:
    init_query(f"INSERT INTO user VALUES ('{email}', '{password}')")

def insert_general_client_table(client_id, ip, time_stemp) -> bool:
    init_query(f"INSERT INTO client VALUES ('{client_id}', '{ip}', '{time_stemp}')")

def insert_general_client_session_id_table(client_session_id, ip, time_stemp, user_agent) -> bool:
    init_query(f"INSERT INTO clientsession (session_id, ip, time_stemp, useragent) VALUES (%s, %s, %s, %s)", (client_session_id, ip, time_stemp, user_agent))

def insert_general_member_table(member) -> bool:
    init_query(f"INSERT INTO member VALUES ('{member.id}', '{member.email}', '{member.ip}', '{member.entry_date}', '{member.first_name}', '{member.last_name}', '{member.street}', '{member.house_number}', '{member.town}', '{member.town_number}', '{member.country}')")

def insert_general_member_session_id_table(member_id, member_session_id, ip, entry_date) -> bool:
    init_query(f"INSERT INTO membersession VALUES ('{member_id}', '{member_session_id}', '{ip}', '{entry_date}')")

def insert_general_admin_table(admin) -> bool:
    init_query(f"INSERT INTO admin (email, ip, entry_date, name, second_name) VALUES ('{admin.email}', '{admin.ip}', '{admin.entry_date}', '{admin.name}', '{admin.second_name}')")

def insert_general_admin_session_id_table(admin_id, admin_session_id, time_stemp) -> bool:
    init_query(f"INSERT INTO adminsession VALUES ('{admin_id}', '{admin_session_id}', '{time_stemp}')")

def insert_general_admin_key_table(admin_id, admin_key, active, time_stemp) -> bool:
    init_query(f"INSERT INTO adminveri VALUES ('{admin_id}', '{admin_key}', {active}, '{time_stemp}')")

def insert_sus_ip(ip, time, flag_count) -> None:
    print('sus ip')
    
def insert_blocked_ip(ip, time) -> None:
    init_query(f"INSERT INTO blockedip (ip, time_stemp) VALUES ('{ip}', '{time}')")

def insert_log(time, kind, status, mas):
    init_query(f"INSERT INTO log VALUES ('{time}', '{kind}', '{status}', '{mas}')")

def insert_request_log(time, kind, status, ip, user_agent):
    init_query(f"INSERT INTO requestlog VALUES (%s, %s, %s, %s, %s)", (time, kind, status, ip, user_agent)) #user_agent is route



def search_for_cookie(rank, cookie) -> int:
    foo, err = universel_db_query(f"SELECT id FROM {rank}session WHERE session_id = %s", False, (cookie,))
    if err or (len(foo) != 1):
        return -1
    return foo[0]["id"]

def search_for_client_cookie(cookie):
    return search_for_cookie('client', cookie)

def search_for_member_cookie(cookie):
    return search_for_cookie('member', cookie)

def search_for_admin_cookie(cookie):
    return search_for_cookie('admin', cookie)

def search_for_admin_key(key) -> int:
    foo, err = universel_db_query(f"SELECT id FROM adminveri WHERE veri = %s", False, (key,))
    if err or (len(foo) != 1):
        return -1
    return foo[0]["id"]
        
def search_for_existing_admin_key(key) -> int:
    foo, err = universel_db_query(f"SELECT veri FROM adminveri WHERE veri = %s", False, (key,))
    return foo, err

def search_for_user_email(email):
    foo, err = universel_db_query(f"SELECT * FROM user WHERE email = %s", False, (email,))
    if err or len(foo) != 1:
        return 'err@mail', 'errhash', True
    return foo[0]['email'], foo[0]['password'], False

def get_id(rank:str, email:str):
    foo, err = universel_db_query(f"SELECT id FROM {rank} WHERE email = %s", False, (email,))
    if err or len(foo) == 0:
        return -1, True
    return foo[0]['id'], False

def get_password(email) -> str:
    return universel_db_query(f"SELECT password FROM user WHERE email = '{email}'")
        
def get_email(id) -> str:
    foo, err = universel_db_query(f"SELECT email FROM member WHERE id = %s", False, (id,))
    return foo, err
        
def get_user(rank, cookie) -> int:
    foo, err = universel_db_query(f"SELECT id FROM {rank}session WHERE session_id = %s", False, (cookie,))
    # print_in_file('sql/get_user -- searche for cookie:' + str(cookie) + 'foo => ' + foo)
    return foo, err

def get_client(id) -> list:
    foo, err = universel_db_query(f"SELECT * FROM clientsession WHERE id = %s", False, (id,))
    if err or len(foo) != 1:
        return -1, True
    return foo[0], False

def get_member(id) -> list:
    foo, err = universel_db_query(f"SELECT * FROM member WHERE id = %s", False, (id,))
    if err or len(foo) != 1:
        return -1, True
    return foo[0], False

def get_member_new(id:int) -> list:
    foo, err = universel_db_query(f"SELECT * FROM member WHERE id = %s", False, (id,))
    if err or len(foo) != 1:
        return -1, True
    return foo[0], False

def get_admin_key(id) -> int:
    foo, err = universel_db_query(f"SELECT veri FROM adminveri WHERE id = %s", False, (id,))
    if err or len(foo) == 0:
        return -1
    else:
        return foo[0]['veri']
    
def get_admin_key_and_status(id) -> dict:
    foo, err = universel_db_query(f"SELECT veri, active FROM adminveri WHERE id = %s", False, (id,))
    if err or len(foo) == 0:
        return -1, True
    return foo, False


def show_all(rank) -> None:
    foo, err = universel_db_query(f"SELECT * FROM {rank}session")

def show_all_gc(rank) -> None:
    foo, err = universel_db_query(f"SELECT * FROM {rank}")

def return_show_all(rank:str, limit:int, offset:int, addition:str="") -> list:
    # rank = rank.replace('_session', '')
    # rank = rank.replace('_key', '')
    foo, err = universel_db_query(f"SELECT * FROM {rank} {addition} LIMIT {limit} OFFSET {offset} ")
    if err or len(foo) == 0:
        return [], True
    return foo, False
    
def delete_user_session(rank, session_id, key=None) -> None:
    insert_query(f"DELETE FROM {rank}session WHERE session_id = '{session_id}'")
    if rank == 'admin':
        insert_query(f"DELETE FROM adminveri WHERE veri = '{key}'")

def delete_user(rank, id) -> None:
    insert_query(f"DELETE FROM {rank} WHERE id = '{id}'")

def delete_password(email) -> None:
    insert_query(f"DELETE FROM user WHERE email = '{email}'")


def get_news(colum):
    foo, err = universel_db_query('Select * from news', False)
    if err or len(foo) == 0:
        return 'Keine News'
    return foo[-1][colum]


def search_blocked_ip(ip):
    foo, err = universel_db_query(f"SELECT * from blockedip WHERE ip = '{ip}'", False)
    return foo
    

def tryyy_info() -> None:
    foo, err = universel_db_query(f"SELECT count(id), ip FROM client group by ip having count(id) > 1 order by ip asc")
    for result in foo:
        print(result)

# from sqlalchemy import create_engine, Column, Integer, String, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Verbindung zu MySQL-Datenbank herstellen
# DATABASE_URL = "mysql://root:passwd@localhost:3306/texst"
# engine = create_engine(DATABASE_URL)

# # Session konfigurieren
# Session = sessionmaker(bind=engine)
# session = Session()

# # Base-Klasse für ORM-Modelle erstellen
# Base = declarative_base()

# # Beispiel-ORM-Modell
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     email = Column(String(120))

# # Tabellen erstellen (falls sie noch nicht existieren)
# Base.metadata.create_all(engine)

# # Beispielabfrage
# def get_all_users():
#     return session.query(User).all()

# # Beispiel für das Einfügen von Daten
# def insert_user(name, email):
#     new_user = User(name=name, email=email)
#     session.add(new_user)
#     session.commit()

# insert_user("Max Mustermann", "max@example.com")

# # Beispiel für das Abfragen von Daten
# users = get_all_users()
# for user in users:
#     print(f"User: {user.name}, Email: {user.email}")

# # Einfügen eines neuen Nutzers
