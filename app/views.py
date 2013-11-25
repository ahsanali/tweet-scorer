from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm, oauth, twitter

from models import User

from random import randint
from datetime import datetime


@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if current_user.is_authenticated():
        g.user = current_user.id


#@app.after_request
#def after_request(response):
#    db.session.remove()
#    return response


@app.route('/')
def index():
    tweets = None
    tweet_temp = None
    user_info = None
    time_length = datetime.utcnow()
    if g.user is not None:

        user_info = session['twitter_oauth']
        get_user = twitter.request('users/show.json', data={'screen_name': user_info['screen_name']})
        if get_user.status == 200:
            user_info = get_user.data

        resp = twitter.request('statuses/home_timeline.json')
        
        if resp.status == 200:
            tweets = resp.data
            tweet_temp = []

            for tweet in tweets:
                tweet_time = datetime.utcnow().strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                user = User.query.filter_by(name=user_info['screen_name']).first()        
                if user.last_seen is None:
                    tweet_temp.append(tweet)

                elif tweet_time > user.last_seen:
                    tweet_temp.append(tweet)
                    time_length = datetime.utcnow() - user.last_seen
            score_inverse_freq(tweets=tweet_temp, time_length=time_length, user_info=user_info)

        else:
            flash('Unable to load tweets from Twitter.')

    return render_template('index.html', tweets=tweet_temp, user_info=user_info)


@app.route('/login')
def login():
    if current_user.is_authenticated():
        return redirect('/')
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    if current_user.is_authenticated():
        user_info = session['twitter_oauth']
        user = User.query.filter_by(name=user_info['screen_name']).first()
        user.last_seen = datetime.utcnow()
        db.session.commit()
    logout_user()
    return redirect(url_for('index'))

@app.route('/oauthorized')
@twitter.authorized_handler
def oauthorized(resp):
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    user = User.query.filter_by(name=resp['screen_name']).first()

    # user never signed in
    if user is None:
        user = User(name=resp['screen_name'], oauth_token=resp['oauth_token'], oauth_secret=resp['oauth_token_secret'])
        db.session.add(user)
        db.session.commit()
        login_user(user)

    # if new tokens
    user.oauth_token = resp['oauth_token']
    user.oauth_secret = resp['oauth_token_secret']

    db.session.commit()
    login_user(user)

    return redirect(url_for('index'))

@lm.user_loader
def load_user(userid):
    return User(id = userid)

@app.route('/score')
def score_inverse_freq(tweets, time_length, user_info, frequency=None):
    i = 0
    for tweet in tweets:
        tweets[i]['score'] = randint(2,30)
        i = i+1

    from operator import itemgetter
    sorted_tweets = sorted(tweets, key=itemgetter('score'), reverse=True)

    return None
