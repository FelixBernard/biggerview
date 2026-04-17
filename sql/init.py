import os
from sql.sql import init_query # type: ignore
# from sql.db_connector import main_db_plus_database

#def create_database(name) -> bool:
#    init_query(f"CREATE DATABASE {name}", main_db_minus_database)

def create_system_table() -> bool:
    init_query("CREATE TABLE bvsystem (adminkey text, salt text)")

def create_general_user_table() -> bool:
    init_query("CREATE TABLE user (email text, password text)")

def create_general_rank_table() -> bool:
    init_query("CREATE TABLE userrank (id int, rank text)")

def create_general_client_session_id_table() -> bool:
    init_query("CREATE TABLE clientsession (id int not null Auto_increment, session_id text, ip text, time_stemp text, useragent text, PRIMARY KEY (id))")

def create_general_client_table() -> bool:
    init_query("CREATE TABLE client (id int not null Auto_increment, ip text, time_stemp text, PRIMARY KEY (id))")

def create_general_member_table() -> bool:
    init_query("CREATE TABLE member (id int not null Auto_increment, email text, ip text, entry_date text, first_name text, last_name text, street text, house_number text, town text, town_number text, country text, PRIMARY KEY (id))")

def create_general_member_session_id_table() -> bool:
    init_query("CREATE TABLE membersession (id int, session_id text, ip text, time_stemp text)")

def create_general_admin_table() -> bool:
    init_query("CREATE TABLE admin (id int not null Auto_increment, email text, ip text, entry_date text, name text, second_name text, PRIMARY KEY (id))")

def create_general_admin_session_id_table() -> bool:
    init_query("CREATE TABLE adminsession (id int, session_id text, time_stemp	text)")

def create_general_admin_key_table():
    init_query("CREATE TABLE adminveri (id int, veri text, active bool, time_stemp	text)")

def create_data_table(user, name) -> bool:
    init_query("CREATE TABLE data (amount float, bankkonto float, day int, month int, year int, info text, full_year text, transsaction_id int)")

def create_temp_path_table():
    init_query("CREATE TABLE temppath (id int, time_stemp TIMESTEMP)")

def create_diray_table():
    init_query("CREATE TABLE diray (time_stemp DATE, diraytext text, flags text, sleepscore int, sleeptime TIMESTEMP, ,PRIMARY KEY (time_stemp))")

# def create_user_log_db(rank:chr, id) -> bool:
#     with sqlite3.connect('data/user/individual/'+rank+id+'/invoice'+id+'.db') as database:
#         database.execute("CREATE TABLE user (ip text, time_stemp text, side text)")

def create_member_folder(id):
    os.makedirs(f'data/user/individual/m{id}')


def create_blocked_ip_table():
    init_query("CREATE TABLE blockedip (id int not null Auto_increment, ip text, time_stemp text, PRIMARY KEY (id))")

def create_log_table():
    init_query("CREATE TABLE log (time text, kind text, status text, massage text)")

def create_errlog_table():
    init_query("CREATE TABLE errlog (time text, kind text, status text, massage text)")

def create_requestlog_table():
    init_query("CREATE TABLE requestlog (time text,  kind text, status text, ip text, useragent text, path text)")