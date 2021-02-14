import pandas as pd
import numpy as np
import requests
import praw

client_ID = 'jRRw9hMnJBVXfQ'
secret_key = 'nkFXjrzRGLMf54iwJOjsdvnWQDbyMQ'

# User　Name: hg558636565
# Pass Word: hg55863656365

reddit = praw.Reddit(client_id = client_ID,
                     client_secret = secret_key,
                     password='hg55863656365',
                     user_agent="RyanAPI/hg558636565",
                     username='hg558636565')

# Get post title and other informations.
posts = []
ml_subreddit = reddit.subreddit('wallstreetbets')

# limit could change to 'all'. means get all the post.
for post in ml_subreddit.hot(limit=10):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

# Get Comments
# id value is each post id. you could write a loop to download it.
submission = reddit.submission(id="likmpp")
submission.comments.replace_more(limit=0)
comm = []
for top_level_comment in submission.comments:
    comm.append(top_level_comment.body)
    
    
