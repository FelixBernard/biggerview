import flask
import os
from views import views
from api import api
import system
from server_config_temp import *
from sql.sql import universel_db_query

app = flask.Flask(__name__)

# Prüfe, ob die Datenbank bereits initialisiert wurde
if not os.environ.get("DB_INITIALIZED") == "false":
    print("Erstes Mal: Datenbank wird konfiguriert...")
    system.init_server(False)
    os.environ.setdefault("DB_INITIALIZED", "true")
    print("Datenbank konfiguriert!")

system_config, err = universel_db_query("SELECT * FROM bvsystem", False, None)
ADMIN_KEY = system_config[0]["adminkey"]
SALT = system_config[0]["salt"]

app.config['MYSQL_DATABASE_HOST'] = os.environ.get('DB_HOST')
app.config['MYSQL_DATABASE_USER'] = os.environ.get('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('DB_NAME')

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    app.run(port=8099, host="0.0.0.0", debug=False)