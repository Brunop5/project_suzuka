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
        sub = reddit.subreddit(subreddit_name)
        for submission in sub.hot(limit=1):
            print(submission.title)

        return "Successfully logged in and found subreddit"
    except Exception as e:
        return f"An error has occured: {e}"
    

def post_on_reddit(client_id, secret, subreddit_name, username, password, args):
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
    