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
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=secret,
        user_agent=f"linux:com.example.mytestapp:1.0.0 (by {username})",
        username=username,
        password=password
    )
    
    test_photo = praw.models.InlineImage("fotka", "test_photo.jpg")
    media = {"fotka", test_photo}
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(title=args[0], selftext=args[1], inline_media=media)
        return "Success!"
    except Exception as e:
        return f"ERROR: {e}"
    