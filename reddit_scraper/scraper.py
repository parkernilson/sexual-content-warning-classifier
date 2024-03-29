import configparser
import praw

from ..data.db import DB

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("reddit.ini")
    client_id = config["reddit"]["client_id"]
    secret = config["reddit"]["secret"]
    user_agent = config["reddit"]["user_agent"]

    reddit = praw.Reddit(
        client_id=client_id, client_secret=secret, user_agent=user_agent
    )

    subreddit_name = "3Dprinting"
    feed = reddit.subreddit(subreddit_name).hot(limit=10)
    for submission in feed:
        # TODO: Save submission to database
        pass