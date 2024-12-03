from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.tweet import Tweet
from services.crud import get_tweet, get_tweets_of_user, get_tweets, create_tweet, update_tweet, delete_tweet
import jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    
    if token is None:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user_info = jwt.decode(jwt=token, key="secret", algorithms=["HS256",])
    return user_info  # In a real application, you would return a user object

@app.get("/tweets")
def _get_tweets(current_user: str = Depends(get_current_user)):
    result = get_tweets()
    return {'tweets': result}

@app.get("/tweets/{tweet_id}")
def _get_tweet(tweet_id: str, current_user: str = Depends(get_current_user)):
    return {'tweets': get_tweet(tweet_id=tweet_id)}

@app.get("/users/{user_id}")
def _get_tweets_of_user(user_id: str, current_user: str = Depends(get_current_user)):
    return {'tweets': get_tweets_of_user(user_id=user_id)}

@app.post("/tweets", status_code=201)
def _create_tweet(tweet: Tweet, current_user: str = Depends(get_current_user)) -> str:

    tweet_id = create_tweet(tweet_content=tweet.tweet_content, username=current_user['username'], user_id=current_user['sub'], mentions=tweet.mentions, hashtags=tweet.hashtags)
    return tweet_id

@app.delete("/tweets/{tweet_id}")
def _delete_tweet(tweet_id: str) -> None:
    return delete_tweet(tweet_id=tweet_id)

@app.put("/tweets/{tweet_id}")
def _update_tweet(tweet_id:str, tweet_content:str, current_user: str = Depends(get_current_user)):
    result = update_tweet(tweet_id=tweet_id, user_id=current_user['sub'], tweet_content=tweet_content)
    
    if result:
        return {'success': True}
    
    else:
        return {'success': False}