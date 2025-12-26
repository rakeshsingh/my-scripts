import feedparser
import tweepy
import os
import time

from my_scripts.secrets_manager import my_secrets

# --- CONFIGURATION ---
# Replace with your WordPress RSS URL (usually https://yourblog.com/feed/)
RSS_URL = "https://rakeshkumar.wordpress.com/feed/"

# File to store the ID of the last tweeted post
ID_FILE = "last_seen_id.txt"


def get_twitter_client():
    """Initializes and returns the Tweepy Client (Twitter API v2)."""
    return tweepy.Client(
        bearer_token=my_secrets["x_bearer_token"],
        consumer_key=my_secrets["x_consumer_key"],
        consumer_secret=my_secrets["x_consumer_secret"],
        access_token=my_secrets["x_access_token"],
        access_token_secret=my_secrets["x_access_token_secret"],
    )


def get_last_seen_id():
    """Reads the last seen post ID from a file."""
    if not os.path.exists(ID_FILE):
        return None
    with open(ID_FILE, "r") as f:
        return f.read().strip()


def save_last_seen_id(post_id):
    """Saves the last seen post ID to a file."""
    with open(ID_FILE, "w") as f:
        f.write(post_id)


def main():
    # 1. Parse the RSS Feed
    print("Checking for new posts...")
    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("No entries found in RSS feed.")
        return

    last_seen_id = get_last_seen_id()

    # 2. Identify new posts
    new_posts = []

    # Iterate through entries. Note: Feeds usually start with the newest.
    for entry in feed.entries:
        # If we hit the last seen ID, we stop gathering posts
        if entry.id == last_seen_id:
            break
        new_posts.append(entry)

    # If this is the first run (no history), let's only tweet the latest one
    # to avoid spamming Twitter with your entire blog history.
    if last_seen_id is None and new_posts:
        new_posts = [new_posts[0]]

    # 3. Tweet new posts (Reversed so we tweet Oldest -> Newest)
    client = get_twitter_client()

    for post in reversed(new_posts):
        title = post.title
        link = post.link

        # Format the tweet
        tweet_text = f"Just wrote a new blog post: {title}\n{link}"

        try:
            # Post to Twitter
            response = client.create_tweet(text=tweet_text)
            print(f"Tweeted: {title}")

            # Update the last seen ID immediately after a success
            save_last_seen_id(post.id)

            # Sleep briefly to avoid hitting rate limits if posting multiple
            time.sleep(2)

        except Exception as e:
            print(f"Error tweeting post '{title}': {e}")
            break

    if not new_posts:
        print("No new posts to tweet.")


if __name__ == "__main__":
    main()
