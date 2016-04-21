from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('config')
#config file still has original WTF CSRF and secret key values...need to changes
db = SQLAlchemy(app)

from app import views, models
