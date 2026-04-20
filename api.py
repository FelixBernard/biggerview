from flask import Blueprint, render_template, request, jsonify, make_response, send_file, send_from_directory, current_app, abort
from werkzeug.utils import secure_filename
#from scripts.cookie_man import handle_client_cookie
#from classes.user import User, Admin, Member, Client, delete_user
import sql.sql as sql
from datetime import datetime, timezone, timedelta
from scripts.func import hash_in, create_post_response, generate_confirmation_code
#from scripts.print_in_file import print_in_file
from scripts.security import prevent_sql_inqeckt, send_email, is_blocked
from user.user import Admin, Member
from scripts.user_setup import *
from server_config import *

UPLOAD_FOLDER = '/static/pictures/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

PRIMARY_KEYS = {
    "admin": "email",
    "adminsession": "session_id",
    "adminveri": "veri",
    "member": "email",
    "membersession": "session_id",
    "client": "id",
    "clientsession": "session_id",
    "user": "email",
    "blockedip": "ip",
    "log": "time"
}

api = Blueprint(__name__, "api")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_admin(request) -> bool:
    key = request.cookies.get(ADMIN_KEY)
    cookie = request.cookies.get('user')
    if key == None:
        return False
    
    idk, err_ak = sql.search_for_admin_key(key)
    idc, err_ac = sql.search_for_admin_cookie(cookie)
    if err_ak or err_ac:
        return False
    if idk != None:
        if idk == idc:
            return True
        else:
            return False
    else:
        return False
    
@api.before_request
def before_request():
    # if request.access_route[0] != '79.192.157.46':
    #     return 'Access dinied', 503
    # if current_app.config['DEEP_SHUTTING_DOWN']:
    #    return 'Server is shutting down...', 503
    #if is_blocked(request.access_route[0]):
    #    return 'Acces dinied', 403
    # if current_app.config['SHUTTING_DOWN']:
    #     admin = is_admin(request)
    #     if admin: #or request.access_route[0] == '79.192.156.158':     {request.remote_addr}
    #         pass
    #     else:
    #         return 'Server is shutting down...', 503
    # else:
    #     urs:str = str(request.url_rule)
    #     if 'admin' in urs or 'api/download' in urs:
    #         if is_admin(request):
    #             pass
    #         else:
    #             return make_response(render_template("error/not_found.html"))
    #     else:
    #         pass
    pass

@api.route("admin/login", methods = ['POST'])
def api_login():
    if request.method == 'POST':
        code = generate_confirmation_code(10)
        # if not current_app.config['LOGIN_OPEN']:
        #     return jsonify(create_post_response('error', 'login geschlossen', '/')), 503

        # extract data from json form
        try:
            data = request.get_json()
            current_email = data['e-mail']
            current_password = data['password']
        except:
            sql.insert_log(time=datetime.now(timezone.utc), kind="WARN", status="login failed", mas="could not extract data from json in api_login; code:" + code)
            return jsonify(create_post_response('error', 'anmeldung fehlgeschlagen ' + code, '/login')), 400

        # suchen nach email in email db, möchten keinen err provozieren
        found_email, found_password_hash, found_err = sql.search_for_user_email(current_email)

        # keine email gefunden
        if found_err:
            sql.insert_log(time=datetime.now(timezone.utc), kind="WARN", status="login failed", mas="email not found in db in api_login; code:" + code)
            return jsonify(create_post_response('error', 'anmeldung fehlgeschlagen ' + code, '/login')), 400

        id, a_err = sql.get_id('admin', found_email)
        if not a_err:
            # sql.insert_log(time=datetime.now(timezone.utc), kind="WARN", status="login failed", mas="admin key error in api_login with admin-error " + str(a_err) + "; code:" + code)
            # return jsonify(create_post_response('error', 'id error on admin ' + code, '/login')), 400
            if hash_in(current_password + SALT) == found_password_hash:
                # send flag mail
                temp_admin = Admin(id=id, email=found_email)
                temp_admin.ip_adress = request.access_route[0]
                temp_cookie = temp_admin.create_admin_session()
                # temp_admin.send_warning_email()
                sql.init_query(f"Update adminveri SET active = 1 where id = '{id}'")
                respp = jsonify(create_post_response('ok', 'erfolgreicher login', '/', temp_cookie))
                respp.set_cookie('user', temp_cookie, samesite='Strict', expires=datetime.now() + timedelta(days=90), httponly=True, secure=True)
                respp.set_cookie('isauth', 'true', samesite='Strict', expires=datetime.now() + timedelta(days=900), httponly=True, secure=True)
                return respp, 200
            else:
                # sql.insert_blocked_ip(request.access_route[0], datetime.now(timezone.utc))
                sql.insert_log(time=datetime.now(timezone.utc), kind="WARN", status="login failed", mas="admin login failed in api_login hash or key or status not matching; code:" + code)
                return jsonify(create_post_response('error', 'anmeldung fehlgeschlagen ' + code, url='/login')), 400 
        id, err = sql.get_id('member', found_email)
        if err:
            # kein id gefunden, obwohl email gefunden wurde, das sollte nicht passieren
            return jsonify(create_post_response('error', 'anmeldung fehlgeschlagen (667)', '/login')), 400
        if hash_in(current_password + SALT) == found_password_hash:
            temp_member = Member()
            temp_member.ip_adress = request.access_route[0]
            temp_cookie = temp_member.create_member_session_id()
            sql.insert_general_member_session_id_table(id, temp_cookie, request.access_route[0], datetime.now(timezone.utc))
            resp = jsonify(create_post_response('ok', 'angemeldet', '/profile', temp_cookie))
            resp.set_cookie('user', temp_cookie, samesite='Strict', expires=datetime.now() + timedelta(days=90))
            return resp, 200
        else:
            return jsonify(create_post_response('error', 'anmeldung fehlgeschlagen (x87)', '/login')), 400

@api.route("admin/log", methods = ['POST'])
def api_log():
    if request.method == 'POST':
        temp_user, response = set_up_user(request, make_response(""))
        if temp_user.rank == 'admin':
            try:
                data = request.get_json()
                offset = int(data['offset'])
                liste, err = sql.return_show_all("log", 50, offset*50, "order by time desc")
                masg = {
                    "primary_key": "time",
                    "datas": liste
                }
                if err:
                    return jsonify(create_post_response('err', masg)), 400
                return jsonify(create_post_response('ok', masg)), 200
            except:
                # sql.insert_log(datetime.now(timezone.utc), 'api_log', 'err', 'Es konnte keine datenbank gefunden werden')
                liste = []
                return jsonify(create_post_response('err', liste)), 403
        else:
            abort(404)

@api.route("admin/requests", methods = ['POST'])
def api_request():
    if request.method == 'POST':
        temp_user, response = set_up_user(request, make_response(""))
        if temp_user.rank == 'admin':
            try:
                liste, err = sql.universel_db_query("select useragent, count(useragent) as count from requestlog group by useragent having count > 1 order by count desc", False)
                masg = {
                    "datas": liste
                }
                if err:
                    return jsonify(create_post_response('err with query', masg)), 400
                return jsonify(create_post_response('ok', masg)), 200
            except Exception as e:
                # sql.insert_log(datetime.now(timezone.utc), 'api_log', 'err', 'Es konnte keine datenbank gefunden werden')
                liste = []
                return jsonify(create_post_response('err' + str(e), liste)), 403
        else:
            abort(404)


@api.route("admin/activity", methods = ['POST'])
def api_activity():
    if request.method == 'POST':
        temp_user, response = set_up_user(request, make_response(""))
        if temp_user.rank == 'admin':
            try:
                liste, err = sql.universel_db_query("""
                    SELECT DATE_FORMAT(STR_TO_DATE(time, '%Y-%m-%d %H:%i:%s.%f'), '%Y-%m-%d %H:00:00') AS hour, COUNT(*) AS request_count 
                    FROM requestlog 
                    WHERE STR_TO_DATE(time, '%Y-%m-%d %H:%i:%s.%f') >= DATE_SUB(NOW(), INTERVAL 7 DAY) 
                    GROUP BY hour 
                    ORDER BY hour
                """, False)
                masg = {
                    "datas": liste
                }
                if err:
                    return jsonify(create_post_response('err with query', masg)), 400
                return jsonify(create_post_response('ok', masg)), 200
            except Exception as e:
                # sql.insert_log(datetime.now(timezone.utc), 'api_log', 'err', 'Es konnte keine datenbank gefunden werden')
                liste = []
                return jsonify(create_post_response('err' + str(e), liste)), 403
        else:
            abort(404)

@api.route("admin/diray", methods = ['POST'])
def api_diray():
    if request.method == 'POST':
        temp_user, response = set_up_user(request, make_response(""))
        try:
            data = request.get_json()
            offset = int(data['offset'])
            liste, err = sql.return_show_all("diray", 50, offset*50, "order by time_stemp desc")
            if err:
                return jsonify(create_post_response('err', masg)), 400
            masg = {
                "primary_key": "time_stemp",
                "datas": liste
            }
            return jsonify(create_post_response('ok', masg)), 200
        except:
            # sql.insert_log(datetime.now(timezone.utc), 'api_log', 'err', 'Es konnte keine datenbank gefunden werden')
            liste = []
            return jsonify(create_post_response('err', liste)), 403
        else:
            abort(404)

    
# @api.route("admin/db/<db>", methods= ['POST'])
# def api_db(db:str):
#     if request.method == 'POST':
#         temp_user, boo = set_up_user(request, make_response(render_template("admin/a_profile.html")), False)
#         if temp_user.rank == 'admin':
#             try:
#                 data = request.get_json()
#                 offset = int(data['offset'])
#                 liste, err = sql.return_show_all(db, 50, offset*50)
#                 masg = {
#                     "primary_key": PRIMARY_KEYS[db],
#                     "datas": liste
#                 }
#                 if err:
#                     return jsonify(create_post_response('err', masg)), 400
#                 return jsonify(create_post_response('ok', masg)), 200
#             except:
#                 print_in_file('ERR', 'exe', 'Es konnte keine datenbank gefunden werden')
#                 return jsonify(create_post_response('err', liste)), 403