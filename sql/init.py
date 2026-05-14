import os
from sql.sql import init_query # type: ignore
# from sql.db_connector import main_db_plus_database

#def create_database(name) -> bool:
#    init_query(f"CREATE DATABASE {name}", main_db_minus_database)

def create_system_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS bvsystem (adminkey text, salt text, adminprefix text)")

def create_general_user_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS user (email VARCHAR(254), password text, PRIMARY KEY (email))")

def create_general_rank_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS userrank (id int, rank text)")

def create_general_client_session_id_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS clientsession (id int not null Auto_increment, session_id text, ip text, time_stemp text, useragent text, PRIMARY KEY (id))")

def create_general_client_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS client (id int not null Auto_increment, ip text, time_stemp text, PRIMARY KEY (id))")

def create_general_member_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS member (id int not null Auto_increment, email text, ip text, entry_date text, first_name text, last_name text, street text, house_number text, town text, town_number text, country text, PRIMARY KEY (id))")

def create_general_member_session_id_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS membersession (id int, session_id text, ip text, time_stemp text)")

def create_general_admin_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS admin (id int not null Auto_increment, email text, ip text, entry_date text, name text, second_name text, PRIMARY KEY (id))")

def create_general_admin_session_id_table() -> bool:
    init_query("CREATE TABLE IF NOT EXISTS adminsession (id int, session_id text, time_stemp	text)")

def create_general_admin_key_table():
    init_query("CREATE TABLE IF NOT EXISTS adminveri (id int, veri text, active bool, time_stemp	text)")

def create_data_table(user, name) -> bool:
    init_query("CREATE TABLE IF NOT EXISTS data (amount float, bankkonto float, day int, month int, year int, info text, full_year text, transsaction_id int)")

def create_temp_path_table():
    init_query("CREATE TABLE IF NOT EXISTS temppath (id int, time_stemp TIMESTEMP)")

def create_diary_table():
    init_query(f"CREATE TABLE IF NOT EXISTS diary (user_id int, date DATE, diarytext text, flags text, sleepid int, eatid int)")

def create_eat_table():
    init_query(f"CREATE TABLE IF NOT EXISTS eat (user_id int, date DATE, eatid int, weight float)")

def create_meal_table():
    init_query(f"CREATE TABLE IF NOT EXISTS meal (user_id int, eatid int, mealid int, weight float)")

def create_mealocc_table():
    init_query(f"CREATE TABLE IF NOT EXISTS mealocc (mealid int, name text, kcal float, carbs float, protein float, fat float)")

def create_sleep_table():
    init_query(f"CREATE TABLE IF NOT EXISTS sleep (user_id int, date DATE, sleeptime float, sleepid int)")

def create_bank_table():
    init_query(f"CREATE TABLE IF NOT EXISTS bank (user_id int, date DATE, timestemp TIMESTAMP, bankid int not null Auto_increment, bankkonto text, flags text, info text, amount float, PRIMARY KEY (bankid))")

def create_transaction_table():
    init_query(f"CREATE TABLE IF NOT EXISTS transfer (user_id int, date DATE, timestemp TIMESTAMP, transferid int not null Auto_increment, amount float, bankid int, flags text, info text, PRIMARY KEY (transferid))")

def create_skills_table():
    init_query(f"CREATE TABLE IF NOT EXISTS skills (user_id int, skilltext text, score int)")

# def create_user_log_db(rank:chr, id) -> bool:
#     with sqlite3.connect('data/user/individual/'+rank+id+'/invoice'+id+'.db') as database:
#         database.execute("CREATE TABLE user (ip text, time_stemp text, side text)")

def create_member_folder(id):
    os.makedirs(f'data/user/individual/m{id}')


def create_blocked_ip_table():
    init_query("CREATE TABLE IF NOT EXISTS blockedip (id int not null Auto_increment, ip text, time_stemp text, PRIMARY KEY (id))")

def create_log_table():
    init_query("CREATE TABLE IF NOT EXISTS log (time text, kind text, status text, massage text)")

def create_errlog_table():
    init_query("CREATE TABLE IF NOT EXISTS errlog (time text, kind text, status text, massage text)")

def create_requestlog_table():
    init_query("CREATE TABLE IF NOT EXISTS requestlog (time text,  kind text, status text, ip text, useragent text, path text)")