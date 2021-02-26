from requests_html import HTMLSession
import pandas as pd
import datetime
import json
import praw
import time
import numpy as np

# https://api.pushshift.io/reddit/search/submission/?subreddit=wallstreetbets&sort=desc&sort_type=created_utc&after=1523588521&before=1523934121&size=1000
client_ID = 'jRRw9hMnJBVXfQ'
secret_key = 'nkFXjrzRGLMf54iwJOjsdvnWQDbyMQ'
reddit = praw.Reddit(client_id = client_ID,
                     client_secret = secret_key,
                     password='hg55863656365',
                     user_agent="RyanAPI/hg558636565",
                     username='hg558636565')

title = []
full_links = []
sub_id = []
date = []
self_text = []
num_comments = []
Top_comments = []
datedata = pd.read_excel("time3.xlsx")
search = "wallstreetbets"

data = pd.DataFrame({"Time":date,
                          "title":title,
                          "Links":full_links,
                          "ID":sub_id,
                          "num_comments":num_comments})

for d in range(len(datedata)-1):
    after = str(datedata.iloc[d,1])
    before = str(datedata.iloc[d,3])
    link = "https://api.pushshift.io/reddit/search/submission/?subreddit="+search+"&sort=desc&sort_type=created_utc&after="+after+"&before="+before+"&size=1000"
    session = HTMLSession()
    r = session.get(link)
    y = json.loads(r.text)
    
    for each in range(len(y['data'])):
        temp = y['data'][each]
        title.append(temp["title"])
        full_links.append(temp["full_link"])
        sub_id.append(temp["id"])
        date.append(datetime.datetime.fromtimestamp(temp["created_utc"]) + datetime.timedelta(hours=6))
        num_comments.append(temp["num_comments"])
        
        #submission = reddit.submission(id=temp["id"])
        #submission.comments.replace_more(limit=0)
        #comm = []
        #num = 1
        #for top_level_comment in submission.comments:
        #    if num < 50: 
        #        if top_level_comment != "[deleted]":
        #            comm.append(top_level_comment.body) # each.created
        #    else:
        #        break;
        #Top_comments.append(comm)
    print(datedata.iloc[d,0])
    time.sleep(np.random.uniform(3,5))
    temp_data = pd.DataFrame({"Time":date,
                              "title":title,
                              "Links":full_links,
                              "ID":sub_id,
                              "num_comments":num_comments})
    data = pd.concat([data, temp_data])
        
#data = pd.DataFrame({"Time":date,
#                    "title":title,
#                     "Links":full_links,
#                     "ID":sub_id,
#                     "num_comments":num_comments,
#                     "raw":raw,
#                     "Top_comments": Top_comments})


#data.to_csv("data.csv")


#data.iloc[0:int(15304268/10),:].to_csv("data1.csv")
#data.iloc[0:int(15304268/10*2),:].to_csv("data2.csv")
#data.iloc[0:int(15304268/10*3),:].to_csv("data3.csv")
#data.iloc[0:int(15304268/10*4),:].to_csv("data4.csv")
#data.iloc[0:int(15304268/10*5),:].to_csv("data5.csv")
#data.iloc[0:int(15304268/10*6),:].to_csv("data6.csv")
#data.iloc[0:int(15304268/10*7),:].to_csv("data7.csv")
#data.iloc[0:int(15304268/10*8),:].to_csv("data8.csv")
#data.iloc[0:int(15304268/10*9),:].to_csv("data9.csv")
#data.iloc[0:int(15304268/10*10),:].to_csv("data10.csv")
#data.iloc[0:int(3311350/2),:].to_csv("data11.csv")
#data.iloc[0:int(3311350/2*2),:].to_csv("data12.csv")

# Drop Duplicated post.
data = pd.DataFrame()
for each in range(1,13):
    temp = pd.read_csv("data" + str(each) + '.csv')
    temp = temp.drop_duplicates('ID')
    data = pd.concat([data, temp])
data = data.drop_duplicates('ID')

# Get "GME" post or "GameStop", "gameStop", "Gamestop", "gamestop"
data['GME'] = data["title"].str.find("GME")
data['GameStop'] = data["title"].str.find("GameStop")
data["gameStop"] = data["title"].str.find("gameStop")
data["Gamestop"] = data["title"].str.find("Gamestop")
data["gamestop"] = data["title"].str.find("gamestop")
data = data[(data['GME'] != -1) 
            | (data['GameStop'] != -1)
            | (data["gameStop"] != -1)
            | (data["Gamestop"] != -1)
            | (data["gamestop"] != -1)]
data = data.sort_values(by = ['Time'])

# Read comments.
Top_comments = []
for each in range(8324,len(data)):
    temp = data.iloc[each, :] 
    submission = reddit.submission(id=temp["ID"])
    submission.comments.replace_more(limit=0)
    comm = []
    num = 1
    for top_level_comment in submission.comments:
        if num < 50: 
            if top_level_comment != "[deleted]":
                comm.append([top_level_comment.body,datetime.datetime.fromtimestamp(top_level_comment.created)])
        else:
            break;
    Top_comments.append(comm)
data['Top_comments'] = Top_comments


# Merge GME and Post data.
post = pd.read_csv("C:\\Users\\qxu5\\Desktop\\reddit\\data_GME.csv")
data60 = pd.read_csv("C:\\Users\\qxu5\\Desktop\\reddit\\GME_60min.csv")
data60['return'] = data60['close'].pct_change()

ll = pd.merge(post,data60, on = ['year', 'month', 'day', 'hour'], how='left')
del ll['min']
del ll['pre']





















