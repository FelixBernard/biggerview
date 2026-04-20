import sys
import os
import sql.init as init_files
import sql.sql as sql
from user.user import Admin
from scripts.func import hash_in, generate_confirmation_code
from server_config import SALT, ADMIN_KEY

def count_clients():
    return 0

def init_server(set_admin_manually:bool=True):
    # Alle DB's für Nutzer erzeugen
    init_files.create_system_table()
    init_files.create_general_user_table()
    # init_files.create_general_client_table()
    # init_files.create_general_client_session_id_table()
    init_files.create_general_member_table()
    init_files.create_general_member_session_id_table()
    init_files.create_general_admin_table()
    init_files.create_general_admin_session_id_table()
    init_files.create_general_admin_key_table()
    
    # System Datenbanken
    init_files.create_blocked_ip_table()
    init_files.create_log_table()
    init_files.create_errlog_table()
    init_files.create_requestlog_table()

    config, err = sql.universel_db_query("SELECT * FROM bvsystem", False, None)
    if len(config) != 0:
        print("Configs bereits gesetzt")
    else: 
        admin_key = generate_confirmation_code(20)
        ADMIN_KEY = admin_key
        salt = generate_confirmation_code(5)
        SALT = salt
        print("ADMINKEY, SALT", ADMIN_KEY, SALT)
        sql.insert_query("INSERT INTO bvsystem (adminkey, salt) VALUES (%s, %s)", (admin_key, salt))

    # Admin festlegen
    if set_admin_manually:
        new_admin()
    else:
        new_prep_admin()



def init_session():
    init_files.create_general_client_session_id_table()
    print('intit general user table')

def init():
    init_files.create_general_client_table()
    print('init gc')

def init_user():
    init_files.create_general_user_table()

def init_data_folder():
    try:
        os.makedirs('data/user/individual')
        os.makedirs('data/user/general')
        os.makedirs('data/shop')
    except:
        pass

def init_member():
    init_files.create_general_member_session_id_table()
    init_files.create_general_member_table()


def delete_output_log():
    os.remove('output.log')

def delete_all_dbs():
    import shutil

    if os.path.exists('data/user/general'):
        shutil.rmtree('data/user/general')
    if os.path.exists('data/user/individual'):
        shutil.rmtree('data/user/individual')

    os.mkdir('data/user/general')
    os.mkdir('data/user/individual')
    open('data/user/general/track.txt', 'a').close()
    open('data/user/individual/track.txt', 'a').close()

def all_session():
    while ((i := input('rank zum printen(quit zum beenden): ')) != 'quit'):
        sql.show_all(i)

def all():
    while ((i := input('rank zum printen(quit zum beenden): ')) != 'quit'):
        sql.show_all_gc(i)

def deletee():
    while ((i := input('rank zum deleten(quit zum beenden): ')) != 'quit'):
        while ((m := input('id zum deleten(quit zum beenden): ')) != 'quit'):
            sql.delete_user_session(i, m)

def deletee_2():
    while ((i := input('rank zum deleten(quit zum beenden): ')) != 'quit'):
        while ((m := input('id zum deleten(quit zum beenden): ')) != 'quit'):
            sql.delete_user(i, m)

def ss():
    cookie = input('cookie to search: ')
    print(sql.search_for_client_cookie(cookie))
    
def new_admin():
    e_mail = input('lege eine Admin email fest: ')
    password = input('lege ein Admin password fest: ')
    admin = Admin(email=e_mail)
    admin.set_new_admin(first=True)
    sql.insert_general_user_table(admin.email, hash_in(f'{password}{SALT}'))
    # sql.init_query(f"Update adminveri set active = 1 where id = %s", (admin.id,)) -- weil der erste Admin so rein darf?

def new_prep_admin():
    e_mail = "admin@admin.com"
    password = "admin"
    admin = Admin(email=e_mail)
    admin.set_new_admin(first=True)
    sql.insert_general_user_table(admin.email, hash_in(f'{password}{SALT}'))

def try_info():
    sql.tryyy_info()

def sql_query():
    while ((x := input('Init/Insert/Delete -> 1 || Select -> 2 || quit -> abbruch: ')) != 'quit'):
        if x != '1' and x != '2':
            print('error')
            break
        q = input('Geben sie ihre query ein: ')
        if int(x) == 1:
            try:
                err = sql.init_query(q)
                print(f"Error: {err}")
            except Exception as e:
                print('error' + str(e))
        elif int(x) == 2:
            try:
                foo, err = sql.universel_db_query(q)
                print(foo)
                print(f"Error: {err}")
            except Exception as e:
                print('error' + str(e))
        else:
            print('error')

def show_pic():
    files = os.listdir('static/pictures')
    for file in files:
        print(file)

def delete_pic():
    file = input('Welches Bild möchtest du löschen? ')
    try:
        os.remove(f'static/pictures/{file}')
        print(f'File {file} gelöscht')
    except:
        print('Es hat nicht geklappt')

def new_news():
    news = input("Was ist die neue News: ")
    id, err = sql.get_news('id')
    sql.insert_query(f"Insert into news values ({id+1}, '{news}')")

def overview():
    print("Clientsessions:")
    print(sql.universel_db_query(f"SELECT * FROM clientsession"))
    print("Adminsessions:")
    print(sql.universel_db_query(f"SELECT * FROM adminsession"))
    print("Adminveri:")
    print(sql.universel_db_query(f"SELECT * FROM adminveri"))
    print("Admins:")
    print(sql.universel_db_query(f"SELECT * FROM admin"))

if __name__ == '__main__':
    dic = {
        'init server': init_server,
        'init user file/table': init,
        'init session': init_session,
        'init data folder(not needet)': init_data_folder,
        'init user': init_user,
        'init member': init_member,
        'clear(delete) output.log': delete_output_log,
        'all session': all_session,
        'delete': deletee,
        'delete2': deletee_2,
        'search': ss,
        'all': all,
        'new admin': new_admin,
        'delete dbs': delete_all_dbs,
        'try_info': try_info,
        'query': sql_query,
        'bilder anzeigen': show_pic,
        'bild loschen': delete_pic,
        'new news': new_news,
        'overview': overview,
        'reqestlog': lambda: print(sql.universel_db_query("SELECT DATE_FORMAT(STR_TO_DATE(time, '%Y-%m-%d %H:%i:%s.%f'), '%Y-%m-%d %H:00:00') AS hour, COUNT(*) AS request_count FROM requestlog WHERE STR_TO_DATE(time, '%Y-%m-%d %H:%i:%s.%f') >= DATE_SUB(NOW(), INTERVAL 7 DAY) GROUP BY hour ORDER BY hour"))
    }
    while ((i := input('aktion(quit zum beenden): ')) != 'quit'):
        if i in dic:
            dic[i]()
        else:
            print('not in command list')
            print('--------------')
            for i in dic:
                print(i)