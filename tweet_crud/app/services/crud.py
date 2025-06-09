from app.db.models import TweetDocument
from typing import List, Dict
import json

def create_tweet(tweet_content=str, username=str, user_id=str, media_url:str=None, mentions:List[str]=None, hashtags:List[str]=None) -> str:
    
    new_tweet = TweetDocument(tweet_content=tweet_content,
                              username=username,
                              user_id=user_id,
                              mentions=mentions,
                              hashtags=hashtags,
                              media_url=media_url)
    
    print (new_tweet.to_json())
    
    return str(new_tweet.save().id)

def delete_tweet(tweet_id:str) -> None:

    target_tweet = None
    
    for tweet in TweetDocument.objects(id=tweet_id):
        target_tweet = tweet
        
    if target_tweet:
        target_tweet.delete()
        
        return {'success': True}
    
    return {'success': False}

def update_tweet(tweet_id: str, user_id: str, tweet_content: str) -> str:

    target_tweet = None
    for tweet in TweetDocument.objects(id=tweet_id):
        target_tweet = tweet
    
    if target_tweet:
        return target_tweet.update(tweet_content=tweet_content, is_edited=True)
    
    return 0

def get_tweets() -> List[Dict]:

    tweets = []
    
    for tweet in TweetDocument.objects().order_by('-created_at'):
        tweets.append(json.loads(tweet.to_json()))

    return tweets

def get_tweet(tweet_id: str) -> Dict:

    tweet_dict = None
    
    for tweet in TweetDocument.objects(id=tweet_id):
        tweet_dict = json.loads(tweet.to_json())

    return tweet_dict

def get_tweets_of_user(user_id: str) -> List[Dict]:

    tweets = []
    
    for tweet in TweetDocument.objects(user_id=user_id).order_by('-created_at'):
        tweets.append(json.loads(tweet.to_json()))

    return tweets

def add_like_to_tweet(tweet_id: str, user_id: str) -> bool:
    target_tweet = None
    
    for tweet in TweetDocument.objects(id=tweet_id):
        target_tweet = tweet
        
    if target_tweet:
        # Check if user already liked the tweet
        if user_id not in target_tweet.likes:
            target_tweet.update(push__likes=user_id)
            return True
    
    return False

def remove_like_from_tweet(tweet_id: str, user_id: str) -> bool:
    target_tweet = None
    
    for tweet in TweetDocument.objects(id=tweet_id):
        target_tweet = tweet
        
    if target_tweet:
        # Check if user has liked the tweet
        if user_id in target_tweet.likes:
            target_tweet.update(pull__likes=user_id)
            return True
    
    return False