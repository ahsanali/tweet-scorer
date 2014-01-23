from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique= True)
    name = db.Column(db.String(60))
    oauth_token = db.Column(db.String(200))
    oauth_secret = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime)
    last_tweet_id = db.Column(db.String(100))

    def get_id(self):
      return self.id

    def is_authenticated(self):
      return True

    def is_active(self):
      return True

    def is_anonymous(self):
      return False

    def __repr__(self):
        return '<ID %r, Name %r, Last_Seen %r>' % (self.id, self.name, self.last_seen)

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    created_by = db.Column(db.String(200))
    date_created = db.Column(db.DateTime)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<IDs %r>' % (self.created_by)
    