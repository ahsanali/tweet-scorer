from celery import Celery
from app import db,models
from twitter import Twitter, OAuth, TwitterHTTPError
from datetime import datetime, timedelta
import logging
import json

celery = Celery('tasks', broker='amqp://guest@localhost//')
celery.config_from_object('celeryconfig')

CONSUMER_KEY = 'WajVXcRxH07y0ef8VMUEA'
CONSUMER_SECRET = 'IxPzvPhWhrkJdFWdYS0wQnuhAi5D4H2puuHZjnAUkDA'


@celery.task
def dump_tweet_job(x, y):
	users = models.User.query.all()
	for (index , user) in enumerate(users):
		try:
			logging.info("\nStarting Job For User:" + user.name)
			set_last_tweet_id = user.last_tweet_id
			temp_tweet_id = None
			twitterHandler = Twitter(auth=OAuth(user.oauth_token, user.oauth_secret,CONSUMER_KEY, CONSUMER_SECRET))
			for i in range(0,5):
				data = { 'count': 200}
				if temp_tweet_id is not None:
					data.update({'max_id':temp_tweet_id})
				data.update({'since_id':user.last_tweet_id})
				logging.info("Request data:%s" % data)
				tweets=twitterHandler.statuses.home_timeline(**data)
				logging.info("\nTotal Numbers of Tweets:%s" % len(tweets))
				if len(tweets) > 0:
					set_last_tweet_id = tweets[0]['id_str']
					print type(tweets[0]['id_str'])
					temp_tweet_id = unicode(int(tweets[-1]['id_str']) - 1)
					print temp_tweet_id
					for tweet in tweets:
						t = models.Tweets(tweet_id = tweet['id_str'], user_id=user.id, created_by=tweet['user']['screen_name'], date_created=datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), content = json.dumps(tweet))
						db.session.add(t)
						db.session.commit()
				else:
					break
			user.last_tweet_id = set_last_tweet_id
			db.session.add(user)
			db.session.commit()
			logging.info("\nClosing job for User:%s" % user.name)
		except Exception, exp:
			logging.info("Exception: %s" % exp)

@celery.task
def fav_tweet_job(x,y):
	data = {}
	users = models.User.query.all()
	for (index , user) in enumerate(users):
		if user.last_fav_tweet_id != None :
			data.update({'since_id':user.last_fav_tweet_id})

		twitterHandler = Twitter(auth=OAuth(user.oauth_token, user.oauth_secret,CONSUMER_KEY, CONSUMER_SECRET))
		tweets=twitterHandler.favorites.list(**data)
		if len(tweets) == 0:
			continue
		for tweet in tweets:
			ft = models.FavTweets(user_id = user.id, tweet_id = tweet['id_str'])
			db.session.add(ft)
			db.session.commit(ft)
		user.last_fav_tweet_id = unicode(int(tweets[-1]['id_str']) - 1)
		db.session.add(user)
		db.session.commit()

