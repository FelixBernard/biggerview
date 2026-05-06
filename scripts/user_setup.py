from user.user import Admin, Member, Client
from server_config import *
from sql import sql
from datetime import datetime, timedelta
# from server_config_temp import *
from config import Config

def set_up_user(request, response):
    if request.cookies.get(Config.ADMIN_KEY) != None:
        id = sql.search_for_admin_cookie(request.cookies.get("bv_user"))
        key = sql.search_for_admin_key(request.cookies.get(Config.ADMIN_KEY))
        if (id == -1 or key == -1):
            return new_client(request=request, response=response)
        tmp_user = Admin(id=id, request=request, response=response)
        tmp_user.load_admin(id=id, cookie=request.cookies.get('bv_user'), key=request.cookies.get(Config.ADMIN_KEY))
        return tmp_user, response
    else:
        if request.cookies.get("bv_user") == None:
            return new_client(request=request, response=response)
        id = sql.search_for_member_cookie(request.cookies.get("bv_user"))
        if (id == -1):
            return new_client(request=request, response=response)
        tmp_user = Member(id=id, request=request, response=response)
        tmp_user.load_member(id=id)
        return tmp_user, response
        

def new_client(request, response):
    tmp_user = Client(request=request, response=response)
    tmp_user.load_new_client_dummy()
    # tmp_user.load_new_client()
    # tmp_user.response.set_cookie("bv_user", tmp_user.session, samesite='Strict', expires=datetime.now() + timedelta(days=90)) #httponly=True, secure=True
    # tmp_user.response.set_cookie("firstaccess", 'y', samesite='Strict')
    return tmp_user, response