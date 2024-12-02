from fastapi import FastAPI
from models.tweet import Tweet
from services.crud import get_tweet, get_tweets_of_user, get_tweets, create_tweet, update_tweet, delete_tweet

app = FastAPI()

@app.get("/tweets")
def _get_tweets():
    result = get_tweets()
    return {'tweets': result}

@app.get("/tweets/{tweet_id}")
def _get_tweet(tweet_id: str):
    return {'tweets': get_tweet(tweet_id=tweet_id)}

@app.get("/users/{user_id}")
def _get_tweets_of_user(user_id: str):
    return {'tweets': get_tweets_of_user(user_id=user_id)}

@app.post("/tweets", status_code=201)
def _create_tweet(tweet: Tweet) -> str:
    tweet_id = create_tweet(tweet_content=tweet.tweet_content, username=tweet.username, user_id=tweet.user_id)
    return tweet_id

@app.delete("/tweets/{tweet_id}")
def _delete_tweet(tweet_id: str) -> None:
    delete_tweet(tweet_id=tweet_id)

@app.put("/tweets/{tweet_id}")
def _update_tweet(tweet_id:str, user_id:str, tweet_content:str):
    update_tweet(tweet_id=tweet_id, user_id=user_id, tweet_content=tweet_content)