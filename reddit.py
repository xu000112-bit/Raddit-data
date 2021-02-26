import pandas as pd
import numpy as np
import requests
import praw
import datetime

client_ID = 'jRRw9hMnJBVXfQ'
secret_key = 'nkFXjrzRGLMf54iwJOjsdvnWQDbyMQ'

# User　Name: hg558636565
# Pass Word: hg55863656365

# https://api.pushshift.io/reddit/search/submission/?subreddit=wallstreetbets&sort=desc&sort_type=created_utc&after=1523588521&before=1523934121&size=1000
# https://www.epochconverter.com/


reddit = praw.Reddit(client_id = client_ID,
                     client_secret = secret_key,
                     password='hg55863656365',
                     user_agent="RyanAPI/hg558636565",
                     username='hg558636565')

# Get post title and other informations.
posts = []
ml_subreddit = reddit.subreddit('wallstreetbets')

# limit could change to 'all'. means get all the post.
for post in ml_subreddit.hot(limit=1000):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, datetime.datetime.fromtimestamp(post.created)])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

# Get Comments
# id value is each post id. you could write a loop to download it.
#submission = reddit.submission(id="likmpp")
#submission.comments.replace_more(limit=0)
#comm = []
#for top_level_comment in submission.comments:
#    comm.append(top_level_comment.body)
    
    
