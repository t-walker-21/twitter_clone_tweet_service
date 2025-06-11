from typing import List, Dict
import json
import time
import random
from src.db.models import TweetDocument
from src.utils.logging import logger

def create_tweet(tweet_content=str, username=str, user_id=str, media_url:str=None, mentions:List[str]=None, hashtags:List[str]=None) -> str:
    
    new_tweet = TweetDocument(tweet_content=tweet_content,
                              username=username,
                              user_id=user_id,
                              mentions=mentions,
                              hashtags=hashtags,
                              media_url=media_url)
    
    tweet_id = str(new_tweet.save().id)

    logger.info(f"Created tweet with ID: {tweet_id} by user: {username}")
    
    return tweet_id

def delete_tweet(tweet_id:str) -> None:

    target_tweet = None
    
    for tweet in TweetDocument.objects(id=tweet_id):
        target_tweet = tweet
        
    if target_tweet:
        target_tweet.delete()

        logger.info(f"Deleted tweet with ID: {tweet_id}")
        
        return {'success': True}
    
    logger.error(f"Attempted to delete non-existent tweet with ID: {tweet_id}")
    return {'success': False}

def update_tweet(tweet_id: str, user_id: str, tweet_content: str) -> str:

    target_tweet = None
    for tweet in TweetDocument.objects(id=tweet_id):
        target_tweet = tweet
    
    if target_tweet:
        logger.info(f"Updating tweet with ID: {tweet_id} by user: {user_id}")
        return target_tweet.update(tweet_content=tweet_content, is_edited=True)
    
    return 0

def get_tweets() -> List[Dict]:

    tweets = []

    time.sleep(random.uniform(0.1, 3.5))
    
    for tweet in TweetDocument.objects().order_by('-created_at'):
        tweets.append(json.loads(tweet.to_json()))

    logger.info(f"Retrieved {len(tweets)} tweets.")

    return tweets

def get_tweet(tweet_id: str) -> Dict:

    tweet_dict = None
    
    for tweet in TweetDocument.objects(id=tweet_id):
        tweet_dict = json.loads(tweet.to_json())

    if tweet_dict is None:
        logger.error(f"Tweet with ID: {tweet_id} not found.")
        return {}
    
    logger.info(f"Retrieved tweet with ID: {tweet_id}")

    return tweet_dict

def get_tweets_of_user(user_id: str) -> List[Dict]:

    tweets = []
    
    for tweet in TweetDocument.objects(user_id=user_id).order_by('-created_at'):
        tweets.append(json.loads(tweet.to_json()))

    logger.info(f"Retrieved tweets for user ID: {user_id}, count: {len(tweets)}")
    return tweets

def add_like_to_tweet(tweet_id: str, user_id: str) -> bool:
    target_tweet = None
    
    for tweet in TweetDocument.objects(id=tweet_id):
        target_tweet = tweet
        
    if target_tweet:
        # Check if user already liked the tweet
        if user_id not in target_tweet.likes:
            target_tweet.update(push__likes=user_id)
            logger.info(f"User {user_id} liked tweet with ID: {tweet_id}")
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
            logger.info(f"User {user_id} removed like from tweet with ID: {tweet_id}")
            return True
    
    return False