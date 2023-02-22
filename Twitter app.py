import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
from pymongo import MongoClient
import time


 # To connect to MONGODB
 
client = MongoClient("mongodb+srv://Itsmesatheesh123:Itsmesatheesh123@cluster0.amauozb.mongodb.net/test") 
TweetDB = client["Twitter_Database"]  #Creating a New Database in  MongoDB
tweets_df = pd.DataFrame()
df = pd.DataFrame()

st.write("Twitter Scrapping")
option = st.selectbox('How would you like the data to be searched?',('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'Example: #Trending Hashtags')
start = st.date_input("Select the start date", datetime.date(2022, 1, 1),key='d1')
end = st.date_input("Select the end date", datetime.date(2023, 1, 1),key='d2')
tweets = st.slider('How many tweets to scrape', 0, 1000, 5)
tweets_list = []


# Srapping the Data from Twitter
if word:
    if option=='Keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweets:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweets:
                break            
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
else:
    st.warning(option,' cant be empty', icon="⚠️")
    
    
# DOWNLOAD AS CSV
@st.cache 
def convert_df(df):    
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    csv = convert_df(tweets_df)
    st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv',)
    
    
    # DOWNLOAD AS JSON
    json_string = tweets_df.to_json(orient ='records')
    st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string,)
    
     # UPLOAD DATA TO DATABASE
    if st.button('Upload Tweets to Database'):
        coll=word
        coll=coll.replace(' ','_')+'_Tweets'
        mycoll=TweetDB[coll]
        dict=tweets_df.to_dict('records')
        if dict:
            mycoll.insert_many(dict) 
            ts = time.time()
            mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": word+str(ts)}}, upsert=False, array_filters=None)
            st.success('Successfully uploaded to database', icon="✅")
            st.balloons()
        else:
            st.warning('there are no tweets', icon="⚠️")

    # SHOW TWEETS
    if st.button('Show Tweets'):
        st.write(tweets_df)

# SIDEBAR
with st.sidebar:   
    st.write('Uploaded Datasets: ')
    for i in TweetDB.list_collection_names():
        mycollection=TweetDB[i]
        #st.write(i, mycollection.count_documents({}))        
        if st.button(i):            
            df = pd.DataFrame(list(mycollection.find())) 

# DISPLAY THE DOCUMENTS IN THE SELECTED COLLECTION
if not df.empty: 
    st.write( len(df),'Records Found')
    st.write(df) 
