import flask
import os
from views import views
from api import api

app = flask.Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = os.environ.get('DB_HOST')
app.config['MYSQL_DATABASE_USER'] = os.environ.get('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('DB_NAME')

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    app.run(port=8099, host="0.0.0.0", debug=False)