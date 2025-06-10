from unittest.mock import MagicMock, patch
import pytest
from src.services.crud import (
    create_tweet,
    delete_tweet,
    update_tweet,
    get_tweets,
    get_tweet,
    get_tweets_of_user,
    add_like_to_tweet,
    remove_like_from_tweet,
)

@patch("src.services.crud.TweetDocument")
def test_create_tweet(mock_tweet_document):
    # Mock the save method to return an object with an id
    mock_tweet = MagicMock()
    mock_tweet.save.return_value.id = "12345"
    mock_tweet_document.return_value = mock_tweet

    tweet_id = create_tweet(
        tweet_content="Hello, world!",
        username="test_user",
        user_id="user123",
        media_url=None,
        mentions=["user456"],
        hashtags=["#test"],
    )

    assert tweet_id == "12345"
    mock_tweet_document.assert_called_once_with(
        tweet_content="Hello, world!",
        username="test_user",
        user_id="user123",
        media_url=None,
        mentions=["user456"],
        hashtags=["#test"],
    )
    mock_tweet.save.assert_called_once()

@patch("src.services.crud.TweetDocument")
def test_delete_tweet(mock_tweet_document):
    # Mock the objects method to return a list with one tweet
    mock_tweet = MagicMock()
    mock_tweet_document.objects.return_value = [mock_tweet]

    result = delete_tweet("12345")

    assert result == {"success": True}
    mock_tweet.delete.assert_called_once()

@patch("src.services.crud.TweetDocument")
def test_update_tweet(mock_tweet_document):
    # Mock the objects method to return a list with one tweet
    mock_tweet = MagicMock()
    mock_tweet_document.objects.return_value = [mock_tweet]

    result = update_tweet("12345", "user123", "Updated content")

    assert result == mock_tweet.update.return_value
    mock_tweet.update.assert_called_once_with(tweet_content="Updated content", is_edited=True)

@patch("src.services.crud.TweetDocument")
def test_get_tweet(mock_tweet_document):
    # Mock the objects method to return a list with one tweet
    mock_tweet = MagicMock()
    mock_tweet.to_json.return_value = '{"id": "12345", "content": "Hello, world!"}'
    mock_tweet_document.objects.return_value = [mock_tweet]

    tweet = get_tweet("12345")

    assert tweet == {"id": "12345", "content": "Hello, world!"}
    mock_tweet.to_json.assert_called_once()

@patch("src.services.crud.TweetDocument")
def test_add_like_to_tweet(mock_tweet_document):
    # Mock the objects method to return a list with one tweet
    mock_tweet = MagicMock()
    mock_tweet.likes = []
    mock_tweet_document.objects.return_value = [mock_tweet]

    result = add_like_to_tweet("12345", "user123")

    assert result is True
    mock_tweet.update.assert_called_once_with(push__likes="user123")

@patch("src.services.crud.TweetDocument")
def test_remove_like_from_tweet(mock_tweet_document):
    # Mock the objects method to return a list with one tweet
    mock_tweet = MagicMock()
    mock_tweet.likes = ["user123"]
    mock_tweet_document.objects.return_value = [mock_tweet]

    result = remove_like_from_tweet("12345", "user123")

    assert result is True
    mock_tweet.update.assert_called_once_with(pull__likes="user123")