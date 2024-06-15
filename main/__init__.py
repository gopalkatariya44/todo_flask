from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from oauthlib.oauth2 import WebApplicationClient
from sqlalchemy.orm import DeclarativeBase

from main.core.config import settings


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = settings.JWT_SECRET_KEY
app.config['SQLALCHEMY_ECHO'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI + settings.DATABASE_NAME
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

db.init_app(app)

login_manager.init_app(app)
client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)

from main import features
