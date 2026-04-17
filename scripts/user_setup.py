from user.user import Admin, Member, Client
from server_config import *
from sql import sql
from datetime import datetime, timedelta
from server_config import *

def set_up_user(request, response):
    if request.cookies.get(ADMIN_KEY) != None:
        id = sql.search_for_admin_cookie(request.cookies.get("bv_user"))
        if (id == -1):
            return new_client(request=request, response=response)
        tmp_user = Admin(request=request, response=response)
        return tmp_user, response
    else:
        id = sql.search_for_client_cookie(request.cookies.get("bv_user"))
        if (id == -1):
            return new_client(request=request, response=response)
        tmp_user = Client(request=request, response=response)
        tmp_user.load_client(id)
        return tmp_user, response
        

def new_client(request, response):
    tmp_user = Client(request=request, response=response)
    tmp_user.load_new_client()
    tmp_user.response.set_cookie("bv_user", tmp_user.session, samesite='Strict', expires=datetime.now() + timedelta(days=90)) #httponly=True, secure=True
    tmp_user.response.set_cookie("firstaccess", 'y', samesite='Strict')
    return tmp_user, response