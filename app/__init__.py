import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir

from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.refresh_view = 'refresh'

oauth = OAuth(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key='WajVXcRxH07y0ef8VMUEA',
    consumer_secret='IxPzvPhWhrkJdFWdYS0wQnuhAi5D4H2puuHZjnAUkDA',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
)

from app import views, models

