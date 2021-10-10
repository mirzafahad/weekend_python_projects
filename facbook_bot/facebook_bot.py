from flask import Flask, request
import json
import requests
import os
import praw
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


PAT = os.environ.get('FACEBOOK_TOKEN')

reddit_id = os.environ.get('REDDIT_ID')
reddit_secret = os.environ.get('REDDIT_SECRET')
reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent='my user agent')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL2']
db = SQLAlchemy(app)

quick_replies_list = [
    {
        "content_type": "text",
        "title": "Meme",
        "payload": "meme",
    },
    {
        "content_type": "text",
        "title": "Motivation",
        "payload": "motivation",
    },
    {
        "content_type": "text",
        "title": "Shower Thought",
        "payload": "Shower_Thought",
    },
    {
        "content_type": "text",
        "title": "Jokes",
        "payload": "Jokes",
    }
]


@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling Verification.")
    if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
        print("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print("Verification failed!")
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling Messages")
    payload = request.get_data()
    print(f"payload: {payload}")
    for sender, message in messaging_events(payload):
        print("Incoming from %s: %s" % (sender, message))
        send_message(PAT, sender, message)

    return "ok"


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
       provided payload."""
    data = json.loads(payload)
    msg_events = data["entry"][0]["messaging"]
    for event in msg_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient."""
    if b"meme" in text.lower():
        subreddit_name = "memes"
    elif b"shower" in text.lower():
        subreddit_name = "Showerthoughts"
    elif b"joke" in text.lower():
        subreddit_name = "Jokes"
    else:
        subreddit_name = "GetMotivated"

    my_user = get_or_create(db.session, Users, name=recipient)
    payload = None

    if subreddit_name == "Showerthoughts":
        for submission in reddit.subreddit(subreddit_name).hot(limit=10):
            if submission.is_self:
                query_result = (Posts.query.filter(Posts.name == submission.id).first())
                if query_result is None:
                    my_post = Posts(submission.id, submission.title)
                    my_user.posts.append(my_post)
                    db.session.commit()
                    payload = submission.title
                    break
                elif my_user not in query_result.users:
                    my_user.posts.append(query_result)
                    db.session.commit()
                    payload = submission.title
                    break
                else:
                    continue

        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps(
                              {
                                  "recipient": {"id": recipient},
                                  "message": {
                                      "text": payload,
                                      "quick_replies": quick_replies_list
                                  }
                              }
                          ),
                          headers={'Content-type': 'application/json'})

    elif subreddit_name == "Jokes":
        payload_text = None
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            if submission.is_self and submission.link_flair_text is None:
                query_result = (Posts.query.filter(Posts.name == submission.id).first())
                if query_result is None:
                    my_post = Posts(submission.id, submission.title)
                    my_user.posts.append(my_post)
                    db.session.commit()
                    payload = submission.title
                    payload_text = submission.selftext
                    break
                elif my_user not in query_result.users:
                    my_user.posts.append(query_result)
                    db.session.commit()
                    payload = submission.title
                    payload_text = submission.selftext
                    break
                else:
                    continue

        requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps(
                          {
                              "recipient": {"id": recipient},
                              "message": {"text": payload}
                          }
                      ),
                      headers={'Content-type': 'application/json'})

        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps(
                              {
                                  "recipient": {"id": recipient},
                                  "message": {"text": payload_text, "quick_replies": quick_replies_list}
                              }
                          ),
                          headers={'Content-type': 'application/json'})
    else:
        payload = "http://imgur.com/WeyNGtQ.jpg"
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            if (submission.link_flair_css_class == 'image') or \
                    (submission.is_self != True and (".jpg" in submission.url or ".png" in submission.url)):

                query_result = (Posts.query.filter(Posts.name == submission.id).first())
                if query_result is None:
                    my_post = Posts(submission.id, submission.url)
                    my_user.posts.append(my_post)
                    db.session.commit()
                    payload = submission.url
                    break
                elif my_user not in query_result.users:
                    my_user.posts.append(query_result)
                    db.session.commit()
                    payload = submission.url
                    break
                else:
                    continue
        print("Payload: ", payload)
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps(
                              {
                                  "recipient": {"id": recipient},
                                  "message": {
                                      "attachment": {"type": "image", "payload": {"url": payload}},
                                      "quick_replies": quick_replies_list
                                  }
                              }
                          ),
                          headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print(r.text)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


relationship_table = db.Table(
    'relationship_table',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'post_id')
)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Posts', secondary=relationship_table, backref='users')

    def __init__(self, name):
        self.name = name


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __init__(self, name, url):
        self.name = name
        self.url = url


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
