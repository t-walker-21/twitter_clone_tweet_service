from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
import time
import jwt
import os
from src.models.tweet import Tweet
from src.services.crud import get_tweet, get_tweets_of_user, get_tweets, create_tweet, update_tweet, delete_tweet, add_like_to_tweet, remove_like_from_tweet
from src.utils.metrics import REQUESTS, ERRORS, REQUEST_DURATION

app = FastAPI()
router = APIRouter(prefix="/tweets")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    
    if token is None:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        user_info = jwt.decode(jwt=token, key=os.environ["JWT_SECRET"], algorithms=["HS256",])
        return user_info
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/metrics")
def metrics():
    metrics_data = generate_latest()  # Generate metrics in Prometheus format
    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)

@router.get("/tweets/")
def _get_tweets(current_user: str = Depends(get_current_user)):
    start_time = time.time()
    result = get_tweets()
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    REQUEST_DURATION.labels(endpoint="/get/tweets").observe(latency)
    REQUESTS.labels(endpoint="/tweets/").inc()
    return {'tweets': result}

@router.get("/tweets/{tweet_id}")
def _get_tweet(tweet_id: str, current_user: str = Depends(get_current_user)):
    return {'tweets': get_tweet(tweet_id=tweet_id)}

@router.get("/users/{user_id}")
def _get_tweets_of_user(user_id: str, current_user: str = Depends(get_current_user)):
    return {'tweets': get_tweets_of_user(user_id=user_id)}

@router.post("/tweets/", status_code=201)
def _create_tweet(tweet: Tweet, current_user: str = Depends(get_current_user)) -> str:

    start_time = time.time()
    tweet_id = create_tweet(tweet_content=tweet.tweet_content, username=current_user['username'], user_id=current_user['sub'], mentions=tweet.mentions, hashtags=tweet.hashtags, media_url=tweet.media_url)
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    REQUEST_DURATION.labels(endpoint="/post/tweets/").observe(latency)
    REQUESTS.labels(endpoint="/post/tweets/").inc()
    return tweet_id

@router.delete("/tweets/{tweet_id}")
def _delete_tweet(tweet_id: str,  current_user: str = Depends(get_current_user)) -> None:
    return delete_tweet(tweet_id=tweet_id)

@router.put("/tweets/{tweet_id}")
def _update_tweet(tweet_id:str, tweet_content:str, current_user: str = Depends(get_current_user)):
    result = update_tweet(tweet_id=tweet_id, user_id=current_user['sub'], tweet_content=tweet_content)
    
    if result:
        return {'success': True}
    
    else:
        return {'success': False}

@router.post("/tweets/{tweet_id}/likes")
def _add_like(tweet_id: str, current_user: str = Depends(get_current_user)) -> dict:
    start_time = time.time()
    result = add_like_to_tweet(tweet_id=tweet_id, user_id=current_user['sub'])
    end_time = time.time()
    REQUESTS.labels(endpoint="/tweets/likes").inc()
    latency = (end_time - start_time) * 1000
    REQUEST_DURATION.labels(endpoint="/tweets/likes").observe(latency)
    if result:
        return {'success': True}
    raise HTTPException(status_code=400, detail="Could not add like")

@router.delete("/tweets/{tweet_id}/likes")
def _remove_like(tweet_id: str, current_user: str = Depends(get_current_user)) -> dict:
    result = remove_like_from_tweet(tweet_id=tweet_id, user_id=current_user['sub'])
    if result:
        return {'success': True}
    raise HTTPException(status_code=400, detail="Could not remove like")

app.include_router(router)