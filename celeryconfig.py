from celery.schedules import crontab
 
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'dump-tweet': {
        'task': 'tasks.dump_tweet_job',
        'schedule': crontab(minute='*/59'),
        'args': (1,2),
    },
    # 'dump-fav':{
    # 	'task':'tasks.fav_tweet_job',
    # 	'schedule': crontab(minute='*/1'),
    # 	'args': (1,2),
    # },

}
CELERYD_HIJACK_ROOT_LOGGER = False