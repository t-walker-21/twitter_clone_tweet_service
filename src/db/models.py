from mongoengine import Document, connect
from mongoengine.fields import StringField, ListField, DateTimeField, BooleanField, ReferenceField
from datetime import datetime
import os

connect(host=os.environ.get("MONGODB_URI_STRING", "mongodb://localhost:27017/tweets"))

class TweetComment(Document):
    comment_content = StringField(required=True, max_length=200)
    username = StringField(required=True)
    user_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    is_edited = BooleanField(default=False)
    likes = ListField(field=user_id)

class TweetDocument(Document):
    tweet_content = StringField(required=True, max_length=200)
    username = StringField(required=True)
    user_id = StringField(required=True)
    likes = ListField(field=user_id)
    mentions = ListField(field=user_id)
    hashtags = ListField(field=StringField())
    media_url = StringField(required=False)
    comments = ListField(ReferenceField(TweetComment))
    created_at = DateTimeField(default=datetime.now)
    is_edited = BooleanField(default=False)