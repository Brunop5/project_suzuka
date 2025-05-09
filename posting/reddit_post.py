import praw

def test_reddit(client_id, secret, subreddit_name, username, password):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=secret,
        user_agent=f"linux:com.example.mytestapp:1.0.0 (by {username})",
        username=username,
        password=password
    )

    try:
        reddit.user.me()
        reddit.subreddit(subreddit_name)
        return "Successfully logged in and found subreddit"
    except Exception as e:
        return e
    

def post_on_reddit(client_id, secret, subreddit_name, username, password, args):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=secret,
        user_agent=f"linux:com.example.mytestapp:1.0.0 (by {username})",
        username=username,
        password=password
    )

    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(args)
        return "Success!"
    except Exception as e:
        return e
    