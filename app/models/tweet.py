from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Tweet(BaseModel):
    tweet_id: str=None
    tweet_content: str
    likes: List[str]
    mentions: List[str]
    hashtags: List[str]
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: str
    username: str