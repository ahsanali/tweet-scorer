from celery.schedules import crontab
 
CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'tasks.job',
        'schedule': crontab(minute='*/1'),
        'args': (1,2),
    },
}
CELERYD_HIJACK_ROOT_LOGGER = False