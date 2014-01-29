import os
import logging

if not os.path.exists("logs"):
	os.makedirs("logs")
#logging.basicConfig(filename='logs/tweet-scorer.log',level=logging.DEBUG)

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

    
SQLALCHEMY_DATABASE_URI = 'postgres://scorer:tweet-scorer@localhost/tweetscorer'
