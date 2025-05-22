import praw
import os

def test_reddit(client_id, secret, subreddit_name, username, password):
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=secret,
            user_agent=f"linux:com.example.mytestapp:1.0.0 (by {username})",
            username=username,
            password=password
        )

        reddit.user.me()
        sub = reddit.subreddit(subreddit_name)
        for submission in sub.hot(limit=1):
            print(submission.title)
    except Exception as e:
        return e

    return "Successfully logged in and found subreddit"

    

def post_on_reddit(args):
    client_id, secret, subreddit_name, username, password = os.getenv("REDDIT_ID"), os.getenv("REDDIT_SECRET"), \
    os.getenv("SUBREDDIT"), os.getenv("REDDIT_USERNAME"), os.getenv("REDDIT_PASSWORD")

    if client_id is None:
        return "ERROR: Reddit Client ID is missing"
    if secret is None:
        return "ERROR: Reddit Client Secret is missing"
    if subreddit_name is None:
        return "ERROR: Subreddit name is missing"
    if username is None:
        return "ERROR: Reddit username is missing"
    if password is None:
        return "ERROR: Reddit password is missing"
    
    
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=secret,
        user_agent=f"linux:com.example.mytestapp:1.0.0 (by {username})",
        username=username,
        password=password
    )

    try:
        subreddit = reddit.subreddit(subreddit_name)
        res = subreddit.submit(title=args[0], selftext=args[1])
        print(res)
        return "Success!"
    except Exception as e:
        return f"ERROR: {e}"
    