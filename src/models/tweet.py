from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Tweet(BaseModel):
    tweet_id: str=None
    tweet_content: str
    likes: Optional[List[str]]
    mentions: Optional[List[str]]
    hashtags: Optional[List[str]]
    media_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)