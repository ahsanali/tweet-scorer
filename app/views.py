from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from operator import itemgetter
from app import app, db, lm, oauth, twitter

from models import User, Tweets

from random import randint
from datetime import datetime, timedelta

from collections import Counter

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

        resp = twitter.request('statuses/home_timeline.json', data={ 'count': 200})
        
        if resp.status == 200:

            # to store in database to generate home timeline
            user = User.query.filter_by(name=user_info['screen_name']).first()
            temp_tweets = resp.data

            if user.last_seen is None:
                
                for tweet in temp_tweets:
                    # minus 7 days from current time
                    current_date = datetime.utcnow()
                    previous_date = current_date - timedelta(days=7)
                    tweet_time = datetime.utcnow().strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    
                    if tweet_time > previous_date:
                        t = Tweets(user_id=user_info['id'], created_by=tweet['user']['screen_name'], date_created=tweet['created_at'])
                        db.session.add(t)
                        db.session.commit()

                    else:
                        break
            else:
   
                for tweet in temp_tweets:
                    tweet_time = datetime.utcnow().strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    if tweet_time > user.last_seen:
                        t = Tweets(user_id=user_info['id'], created_by=tweet['user']['screen_name'], date_created=tweet['created_at'])
                        db.session.add(t)
                        db.session.commit()


            tweets = resp.data
            tweet_temp = []
            temp_tweets = resp.data

            # to display in timeline
            if user.last_seen is None:
                i = 0
                for tweet in temp_tweets:
                    # minus 7 days from current time
                    current_date = datetime.utcnow()
                    previous_date = current_date - timedelta(days=7)
                    tweet_time = datetime.utcnow().strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    
                    if tweet_time >= previous_date:
                        tweet_temp.append(tweet)
                    else:
                        break
            else:
                for tweet in temp_tweets:
                    tweet_time = datetime.utcnow().strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    if tweet_time > user.last_seen:
                        tweet_temp.append(tweet)
                        time_length = datetime.utcnow() - user.last_seen
     
            score_inverse_freq(time_length=time_length, user_info=user_info)
            
            fav_resp = twitter.request('favorites/list.json')
            if fav_resp.status == 200:
                timeline_resp = twitter.request('statuses/user_timeline.json', data={ 'screen_name': user_info['screen_name']})
                if timeline_resp.status == 200:
                    tweet_temp = score_prob_star(tweets=tweet_temp, favorite_tweets=fav_resp.data, user_tweets=timeline_resp.data)
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
        user = User(id=resp['user_id'], name=resp['screen_name'], oauth_token=resp['oauth_token'], oauth_secret=resp['oauth_token_secret'])
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

def score_inverse_freq(time_length, user_info, frequency=None):
    # "tweets" below contain the entire hometime of the logged in user starting from 7 days before the first login
    tweets = Tweets.query.filter_by(user_id=user_info['id'])

    for i in tweets:
        # this will give u the tweet date
        print i.date_created
        # this will give u the user who created this tweet
        print i.created_by

    #from operator import itemgetter
    #sorted_tweets = sorted(tweets, key=itemgetter('score'), reverse=True)

    return None

def user_tweets_stared_by_current_user(tweet_user, favorite_tweets):
    result = []
    i = 0
    for tweet in favorite_tweets:
        if tweet_user == favorite_tweets[i]['user']['screen_name']:
            result.append(tweet)
        i = i+1
    return result

# assign score to single tweet according to the second algo
def assign_score(tweets, starred_tweets, user_tweets):
    return randint(2,30)

def score_prob_star(tweets, favorite_tweets, user_tweets):
    i = 0
    scored_tweets = []
    scored_tweets2 = []
    tweet_freq = Counter()
    for i in range(0,len(tweets)):
       tweet_user = tweets[i]['user']['screen_name']
       tweet_freq[tweet_user] += 1
    star_freq = Counter()
    for i in range(0,len(favorite_tweets)):
       tweet_user = favorite_tweets[i]['user']['screen_name']
       star_freq[tweet_user] += 1

    for i in range(0,len(tweets)):
        tweet_user = tweets[i]['user']['screen_name']
        temp = user_tweets_stared_by_current_user(tweet_user=tweet_user, favorite_tweets=favorite_tweets)
        #score = assign_score(tweets=tweets, starred_tweets=temp, user_tweets=user_tweets)
        score = 1./tweet_freq[tweet_user]
        score2 = (1.*star_freq[tweet_user])/tweet_freq[tweet_user]
        # put the result from score algo here...
        tweets[i]['score'] = score
        tweets[i]['score2'] = score2
#    print tweets[2]
    sorted_tweets = sorted(tweets, key=itemgetter('score'), reverse=True)
    return sorted_tweets

def pull_tweets(last_id):
    resp = twitter.request('statuses/home_timeline.json', data={ 'count': 200, 'max_id': last_id})
    if resp.status == 200:
        older_tweets = resp.data
        return older_tweets



