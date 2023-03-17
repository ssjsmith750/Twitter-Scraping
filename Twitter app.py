import snscrape.modules.twitter as sntwitter
import pandas as pd
from pymongo import MongoClient
import streamlit as st
import datetime
from PIL import Image
import time

# To connect to Mongodb

client = MongoClient("mongodb+srv://Itsme*******:<password>@cluster0.amauozb.mongodb.net/test") 
TwitterScrape = client["Twitter_Database"]  #Creating a New Database in  MongoDB
tweets_df = pd.DataFrame()
df = pd.DataFrame()

########################## Creating a background image #############################################


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2016/09/13/19/31/texture-1668079_960_720.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 


st.header("Twitter Scrapping")

st.markdown("## Using 'snscrape','streamlit'")

option = st.selectbox('How do you like to Scrape the Data',('Keyword','Hastag'))
word = st.text_input ('please enter a'+option,'Example: #Trending Hashtag')
start_date = st.date_input("Select the start date",datetime.date(2023,1,1,),key='d1')
end_date = st.date_input("Select the End date", datetime.date(2023,3,1),key='d2')
tweets = st.slider('How Many tweets to scrape',0 , 1000,50)
tweets_list = []


if word:
    if option == 'Keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start_date} until:{end_date}').get_items()):
            if i >tweets:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.content, tweet.lang, tweet.username, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.source, tweet.url])

        tweets_df = pd.DataFrame(tweets_list,columns=['ID','Data','Content','Language','Username','Replycount', 'Retweetcount', 'Likecount', 'Source','Url'])

    else:
        for i, tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start_date} until:{end_date}').get_items()):
            if i >tweets:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.content, tweet.lang, tweet.username, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.source, tweet.url])

        tweets_df = pd.DataFrame(tweets_list,columns=['ID','Data','Content','Language','Username','Replycount', 'Retweetount', 'Likecount', 'Source','Url'])

else:
    st.warning(option,'cant be empty', icon = "⚠️")



button = st.button("show tweets")

if button:
    st.write(tweets_df)

else:
    st.warning(":black[Give Keywords or Hashtag and Number of tweets and Press show Tweets button]")



############################# Download as csv ############################


@st.cache_data

def convert_df(df):
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    csv = convert_df(tweets_df)
    st.download_button(label="Dowbload the Data as CSV",data = csv,file_name='Twitter_data.csv',mime='text/csv',)



############################## Download as Json ##########################

    json_str = df.to_json()
    json_bytes = json_str.encode('utf-8')
    st.download_button(
        label='Download JSON',
        data=json_bytes,
        file_name='data.json',
        mime='application/json'
    )


############################## Upload Data to MongoDB Database ###########

    if st.button('Upload to Database'):
        coll = word
        coll = coll.replace(' ','_')+'_Tweets'
        mycoll = TwitterScrape[coll]
        dict = tweets_df.to_dict('records')

        if dict:
            mycoll.insert_many(dict)
            Time = time.time()
            mycoll.update_many({},{"$set":{"Keyword_or_Hashtag": word + str(Time)}}, upsert = False, array_filters=None)
            st.success('Succesfully uploaded to database')
            st.spinner('Please wait Your Data is Being uploaded to the Database')
        
        else:
            st.warning('No Tweets Found',icon = "⚠️")



############################ Delete from the Database ##################################

if st.button('Delete from Database'):
        coll = word
        coll = coll.replace(' ','_')+'_Tweets'
        mycoll = TwitterScrape[coll]
        
        if mycoll.count_documents({}) == 0:
            st.warning('No data found in the database', icon="⚠️")
        else:
            confirmation = st.checkbox('I want to delete all data from the database')
            if confirmation:
                mycoll.delete_many({})
                st.success('All data has been deleted from the database')

############################ Sidebar #################################################

with st.sidebar:
    st.write("Uploaded Tweets: ")

    for i in TwitterScrape.list_collection_names():
        mycollection = TwitterScrape[i]

        if st.button(i):
            df = pd.DataFrame(list(mycollection.find()))

################################## To Display the Uploaded Tweets ####################
