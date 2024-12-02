from ..db.models import TweetDocument
from typing import List, Dict
import json

def create_tweet(tweet_content=str, username=str, user_id=str) -> str:
    
    new_tweet = TweetDocument(tweet_content=tweet_content,
                              username=username,
                              user_id=user_id)
    
    return str(new_tweet.save().id)

def delete_tweet(tweet_id:str) -> None:

    for tweet in TweetDocument.objects(id=tweet_id).first():
        tweet.delete()

def update_tweet(tweet_id: str, user_id: str, tweet_content: str) -> str:

    updated_tweet = None
    
    for tweet in TweetDocument.objects(id=tweet_id, user_id=user_id).first():
        updated_tweet = tweet
    
    updated_tweet.tweet_content = tweet_content

def get_tweets() -> List[Dict]:

    tweets = []
    
    for tweet in TweetDocument.objects():
        tweets.append(json.loads(tweet.to_json()))

    return tweets

def get_tweet(tweet_id: str) -> Dict:

    tweet_dict = None
    
    for tweet in TweetDocument.objects(id=tweet_id).first():
        tweet_dict = json.loads(tweet.to_json())

    return tweet_dict

def get_tweets_of_user(user_id: str) -> List[Dict]:

    tweets = []
    
    for tweet in TweetDocument.objects(user_id=user_id):
        tweets.append(json.loads(tweet.to_json()))

    return tweets