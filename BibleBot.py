#! /usr/bin/env python3

import os
import logging
import logging.handlers
import os
import random
import time

import requests
import tweepy
from systemd import journal

# Configure logging
def setup_logging():
    """Sets up logging to either journald or syslog based on availability."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    try:
        handler = journal.JournaldLogHandler()
        log_type = "journald"
    except ImportError:
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        log_type = "syslog"

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, log_type

# Set up logging
log, log_type = setup_logging()

log.info(f"Starting BibleBot with {log_type} logging...")  # Add a startup message

# Load X API credentials from environment variables
API_KEY = os.getenv("X_API_KEY")
API_SECRET = os.getenv("X_API_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Authenticate with X API v2
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Function to get a random Bible verse from bible-api.com
def get_random_verse():
    """
    Retrieves a random Bible verse from the bible-api.com API.

    Returns:
        str: A formatted string containing the verse text and reference,
             or a fallback verse if the API request fails.
    """
    url = "https://bible-api.com//data/kjv/random"
    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            if response.status_code == 200:
                data = response.json()
                verse_data = data["random_verse"]
                book = verse_data["book"]
                chapter = verse_data["chapter"]
                verse_num = verse_data["verse"]
                text = verse_data["text"].strip()
                translation = data["translation"]["identifier"].upper()
                reference = f"{book} {chapter}:{verse_num}, {translation}"
                return f"'{text}' ({reference})"
            elif response.status_code == 429:
                log.warning(f"Rate limited on attempt {attempt + 1}. Retrying after delay.")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                log.error(f"Attempt {attempt + 1} failed: HTTP status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            log.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
        except (KeyError, ValueError) as e:
            log.error(f"Error parsing JSON: {e}")
            break  # stop retrying if the json is bad

    # Fallback verses
    fallback_verses = [
        "John 3:16 - For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life. - John 3:16 KJV",
        "Psalm 23:1 - The Lord is my shepherd; I shall not want. - Psalm 23:1 KJV",
        "Romans 8:28 - And we know that all things work together for good to them that love God, to them who are the called according to his purpose. - Romans 8:28 KJV"
    ]
    # Return a random fallback verse
    return random.choice(fallback_verses)

# Function to post to X
def post_verse():
    tweet = get_random_verse()
    try:
        response = client.create_tweet(text=tweet)
        log.info(f"Posted: {tweet}")
    except tweepy.TweepyException as e:
        log.error(f"Error posting: {e}")

if __name__ == "__main__":
    post_verse()
