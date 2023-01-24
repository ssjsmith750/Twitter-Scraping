# Twitter-Scraping

pip install snscrape # Installing library social networking services.

import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(from:elonmusk) until:2023-01-20 since:2022-10-01"
tweets = []
limit = 1000

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
  if len(tweets) ==limit:
    break
    #(date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.
  else:
        tweets.append([tweet.id,tweet.url,tweet.user.username,tweet.content,tweet.date,tweet.source,tweet.retweetCount,tweet.likeCount,tweet.replyCount])
      
tweets_df = pd.DataFrame(tweets,columns=['Tweeter_ID', 'Url', "Account_Name", 'Content', 'Datetime','Source','Number_Retweets', 'Number_Likes', 'Number_Comments']) 

print(tweets_df)


tweets_df = tweets_df.to_csv("Tweeter_scraping") # converting dataframe to csv file.



pip install pymongo # installing mongo db library

!python --version

from pymongo import MongoClient # Importing Mongo db cloud server library

Tweet = MongoClient("mongodb://Itsmesatheesh123:Itsmesatheesh123@ac-wpuz2t4-shard-00-00.amauozb.mongodb.net:27017,ac-wpuz2t4-shard-00-01.amauozb.mongodb.net:27017,ac-wpuz2t4-shard-00-02.amauozb.mongodb.net:27017/?ssl=true&replicaSet=atlas-lqxz0q-shard-0&authSource=admin&retryWrites=true&w=majority")

Tweeterscraping = Tweet["Tweeter_task"] # creating a database in Mongodb server
Tweets = Tweeterscraping["Elon_Task"]

import pandas as pd # importing pandas library

Tweet = pd.read_csv("/content/Tweeter_scraping")  # Importing the converted Twetterscraping csv file
print(Tweet)

Tweet=Tweet.to_dict("records") #Converting datas to a dictionary

Tweets = Tweeterscraping["Twetter_scrapingDB"] #importing all the datas to the mongodb server
Tweets.insert_many(Tweet)
