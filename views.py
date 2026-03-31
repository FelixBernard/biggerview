import redis
import flask
from datetime import datetime, timezone
from flask import jsonify, request, render_template, make_response, send_file, send_from_directory, current_app, abort, redirect, url_for
from scripts.pdf import erstelle_latex_pdf
from scripts.user_setup import set_up_user
from scripts.func import generate_confirmation_code
from server_config import *
from sql.sql import insert_log, insert_request_log
from user.user import Admin

views = flask.Blueprint(__name__, "views")

@views.before_request
def before():
    temp_ip = request.headers.get('Cf-Connecting-Ip')
    if temp_ip == None:
        temp_ip = request.access_route[0]
    # print("views/before_request -- ip: " + temp_ip + ", cf-ip: " + str(request.headers.get('Cf-Connecting-Ip')) + ", path: " + request.path)
    if (request.cookies.get(SECRET_KEY) == SECRET_VALUE):
        # classifyed as admin
        pass
    else:
        #r = redis.Redis(host='localhost', port=6379, db=0)
        #shutting_down = r.get("SHUTTING_DOWN")
        #if shutting_down and shutting_down.decode() == "true":
        #    return jsonify(message="Server is shut down"), 503
        insert_request_log(time=datetime.now(timezone.utc), kind="INFO", status="precheck", ip=temp_ip, user_agent=request.path)

@views.route("/")
def main():
    tmp_user, response = set_up_user(request, make_response(""))
    response.set_data(render_template("main/index.html", user=tmp_user, link=SECRET_PATH))
    return tmp_user.response

@views.route("/projects")
def projects():
    tmp_user, response = set_up_user(request, make_response(""))
    response.set_data(render_template("main/projects.html", user=tmp_user, link=SECRET_PATH))
    return tmp_user.response

@views.route("/profile")
def profile():
    tmp_user, response = set_up_user(request, make_response(""))
    if tmp_user.rank == 'client':
        response.set_data(render_template("main/profile.html"))
        return response
    elif tmp_user.rank == 'admin':
        response.set_data(render_template("auth/profile.html", user=tmp_user, link=SECRET_PATH))
        return response
    else:
        abort(400)

@views.route("/log/" + SECRET_PATH)
def secret():
    code = generate_confirmation_code(10)
    insert_log(time=datetime.now(timezone.utc), kind="INFO", status="precheck", mas="secret page accessed {ip: " + request.access_route[0] + ", cf-ip: " + str(request.headers.get('Cf-Connecting-Ip')) + "}, code: " + code)
    tmp_user, response = set_up_user(request, make_response(""))
    if tmp_user.rank != "admin":
        abort(404)
    response.set_data(render_template("nimda/log.html", user=tmp_user, link=SECRET_PATH))
    insert_log(time=datetime.now(timezone.utc), kind="INFO", status="passed", mas="secret page accessed {ip: " + request.access_route[0] + ", cf-ip: " + str(request.headers.get('Cf-Connecting-Ip')) + "} as admin with code: " + code)
    return response

@views.route("/3rqjdf/" + SECRET_PATH)
def secret_login():
    insert_log(time=datetime.now(timezone.utc), kind="INFO", status="precheck", mas="login secret page accessed {ip: " + request.access_route[0] + ", cf-ip: " + str(request.headers.get('Cf-Connecting-Ip')) + "}")
    tmp_user, response = set_up_user(request, make_response(""))
    response.set_data(render_template("auth/login.html", user=tmp_user, link=SECRET_PATH))
    #print(response.cookies.get("firstacces"))
    return response

@views.route("/283hr3u/" + SECRET_PATH)
def admin():
    tmp_user, response = set_up_user(request, make_response(""))
    if tmp_user.rank == "admin" and type(tmp_user) == Admin:
        response.set_data(render_template("nimda/nimda.html", user=tmp_user, link=SECRET_PATH))
        return response
    else:
        abort(404)

@views.route("/ip/" + SECRET_PATH)
def ip():
    tmp_user, response = set_up_user(request, make_response(""))
    response.set_data(render_template("test/ip.html", user=tmp_user, access_route_zero=request.access_route[0], access_route=request.access_route, remote_addr=request.remote_addr, request=request, link=SECRET_PATH))
    return response

# @views.route("/pdf")
# def pdf():
#     tmp_user = set_up_user(request, make_response(render_template("auth/profile.html")))
#     if tmp_user.rank == 'client':
#         abort(401)
#     erstelle_latex_pdf("nutzer_info", {"Name": "Felix", "Alter": 21, "Stadt": "Jugenheim"})
#     return send_file("nutzer_info.pdf")


# @views.route("/io")
# def io():
#     tmp_user = set_up_user(request, redirect(url_for('views.main')))
#     if tmp_user.rank != "admin":
#         abort(401)
#     r = redis.Redis(host='localhost', port=6379, db=0)
#     shutting_down = r.get("SHUTTING_DOWN")
#     if shutting_down and shutting_down.decode() == "true":
#         r.set("SHUTTING_DOWN", "false")
#         return jsonify(message="Server wurde hochgefahren"), 503
#     r.set("SHUTTING_DOWN", "true")
#     return jsonify(message="Server wurde heruntergefahren")

@views.route("/static/js/nimda/<path>")
def admin_route(path):
    if request.cookies.get(SECRET_KEY) == SECRET_VALUE:
        return send_from_directory('static/js/nimda', path)
    abort(404)

@views.route('/<path:path>')
def catch_all(path):
    abort(404)