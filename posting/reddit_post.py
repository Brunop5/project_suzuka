import praw


client_id = "kQQYEscST7QB5n8m_aOH9g"
secret = "_31tg0JlyqIbhkloCoxYGLQMV6DE8Q"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent="linux:com.example.mytestapp:1.0.0 (by u/Ok-Criticism-1946)",
)

print(reddit)