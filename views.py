import flask
from datetime import datetime, timezone
from flask import jsonify, request, render_template, make_response, send_file, send_from_directory, current_app, abort, redirect, url_for
from scripts.user_setup import set_up_user
from scripts.func import generate_confirmation_code
from server_config import *
from sql.sql import insert_log, insert_request_log, universel_db_query
from user.user import Admin

views = flask.Blueprint(__name__, "views")

@views.before_request
def before():
    # insert_request_log(time=datetime.now(timezone.utc), kind="INFO", status="precheck", ip=request.access_route[0], user_agent=request.path)
    pass

@views.route("/")
def main():
    tmp_user, response = set_up_user(request, make_response(""))
    response.set_data(render_template("main/index.html", user=tmp_user))
    return tmp_user.response

@views.route("/projects")
def projects():
    tmp_user, response = set_up_user(request, make_response(""))
    response.set_data(render_template("main/projects.html", user=tmp_user))
    return tmp_user.response

@views.route("/profile")
def profile():
    tmp_user, response = set_up_user(request, make_response(""))
    if tmp_user.rank == 'client':
        response.set_data(render_template("main/profile.html"))
        return response
    elif tmp_user.rank == 'admin':
        response.set_data(render_template("auth/profile.html", user=tmp_user))
        return response
    else:
        abort(400)

@views.route("/log")
def secret():
    code = generate_confirmation_code(10)
    insert_log(time=datetime.now(timezone.utc), kind="INFO", status="precheck", mas="secret page accessed {ip: " + request.access_route[0] + ", cf-ip: " + str(request.headers.get('Cf-Connecting-Ip')) + "}, code: " + code)
    tmp_user, response = set_up_user(request, make_response(""))
    if tmp_user.rank != "admin":
        abort(404)
    response.set_data(render_template("nimda/log.html", user=tmp_user))
    insert_log(time=datetime.now(timezone.utc), kind="INFO", status="passed", mas="secret page accessed {ip: " + request.access_route[0] + ", cf-ip: " + str(request.headers.get('Cf-Connecting-Ip')) + "} as admin with code: " + code)
    return response

@views.route("/login")
def secret_login():
    insert_log(time=datetime.now(timezone.utc), kind="INFO", status="precheck", mas="login secret page accessed {ip: " + request.access_route[0] + ", cf-ip: " + str(request.headers.get('Cf-Connecting-Ip')) + "}")
    tmp_user, response = set_up_user(request, make_response(""))
    response.set_data(render_template("auth/login.html", user=tmp_user))
    #print(response.cookies.get("firstacces"))
    return response

@views.route("/admin")
def admin():
    tmp_user, response = set_up_user(request, make_response(""))
    if tmp_user.rank == "admin" and type(tmp_user) == Admin:
        response.set_data(render_template("nimda/nimda.html", user=tmp_user))
        return response
    else:
        abort(404)

@views.route("/ip")
def ip():
    tmp_user, response = set_up_user(request, make_response(""))
    response.set_data(render_template("test/ip.html", user=tmp_user, access_route_zero=request.access_route[0], access_route=request.access_route, remote_addr=request.remote_addr, request=request))
    return response

# @views.route("/pdf")
# def pdf():
#     tmp_user = set_up_user(request, make_response(render_template("auth/profile.html")))
#     if tmp_user.rank == 'client':
#         abort(401)
#     erstelle_latex_pdf("nutzer_info", {"Name": "Felix", "Alter": 21, "Stadt": "Jugenheim"})
#     return send_file("nutzer_info.pdf")


@views.route("/static/js/admin/<path>")
def admin_route(path):
    if request.cookies.get(SECRET_KEY) == SECRET_VALUE:
        return send_from_directory('static/js/nimda', path)
    abort(404)

@views.route('/<path:path>')
def catch_all(path):
    abort(404)