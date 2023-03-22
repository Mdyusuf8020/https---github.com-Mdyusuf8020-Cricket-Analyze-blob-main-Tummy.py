import streamlit as st
import snscrape.modules.twitter as sntwitter
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import pymongo

# -------------------------------- Page Title --------------------------------------------
st.set_page_config(page_title = 'Twitter Scrape')

# -------------------------------- Add BackGround image  --------------------------------------------
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://www.scraperapi.com/wp-content/uploads/scrape-twitter-python.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

# -------------------------------- lottie bird animation -------------------------------------------- 

st.markdown("<h1 style='text-align: center; color: White;'>Twitter Scrape</h1>", unsafe_allow_html=True)

def load_lottieURl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_bird = load_lottieURl("https://assets9.lottiefiles.com/packages/lf20_7jyje5gv.json")

st_lottie(lottie_bird, height=300, width=700, key='bird')

# -------------------------------- Streamlit Setups -------------------------------------------- 
st.header("Scrape Details")

keyword = st.text_input("Enter Scrape Keyword")
start_date = st.date_input(" Start Date")
end_date = st.date_input("End Date")
No_of_Tweets = st.number_input("No of tweets")

# -------------------------------------- Scrape --------------------------------------------
def scraping(keyword,start_date,end_date,No_of_Tweets):
    #scrapper = sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date}")
    scraped_tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date}").get_items()):
        if i > No_of_Tweets-1:
            break
        scraped_data = [tweet.date,
                        tweet.id,
                        tweet.url,
                        tweet.content,
                        tweet.user.username,
                        tweet.replyCount,
                        tweet.retweetCount,
                        tweet.lang,
                        tweet.source,
                        tweet.likeCount]
        scraped_tweets.append(scraped_data)
    
    #Create DataFrame
    tweets = pd.DataFrame(scraped_tweets,columns=['Date', 'ID', 'URL', 'Content','UserName', 
                                            'ReplyCount', 'ReTweetCount','Language', 
                                            'Source', 'LikeCount'])
    return tweets    


# --------------------------------------- MongoDB ------------------------------------------

def mongodb(df_srape):
    # MDB Connection
    connection = pymongo.MongoClient("mongodb://mdyusuf2528:guvi2022@ac-zay3g4s-shard-00-00.bqzotcy.mongodb.net:27017,ac-zay3g4s-shard-00-01.bqzotcy.mongodb.net:27017,ac-zay3g4s-shard-00-02.bqzotcy.mongodb.net:27017/?ssl=true&replicaSet=atlas-z8t1pm-shard-0&authSource=admin&retryWrites=true&w=majority")
    Tweets = connection["Twitter_Scrape"]
    Tweet_Datas = Tweets["Tweets"]
    
    tweet_dict = df_srape.to_dict("records")
    Tweet_Datas.insert_many(tweet_dict)

# -------------------------------------- Buttons --------------------------------------------

scrape = st.button("Scrape")

if scrape:
    df_srape = scraping(keyword, start_date, end_date, No_of_Tweets)
    st.dataframe(df_srape)


MDB, csv, Json = st.columns([1,0.8,0.6])

with MDB:
    
    st.markdown(
        """
        <button class="button-with-logo">
            <img src="https://www.know-bi.be/hubfs/images/logos/platforms/mongodb.svg" alt="Logo" width="140" height="70">  
        </button>
        """
        , unsafe_allow_html=True
    )
    if st.button("Upload to MongoDB"):
        df_srape = scraping(keyword, start_date, end_date, No_of_Tweets)
        mongodb(df_srape)
        st.success("!Successfully updated into DataBase!")
        
with csv:

    st.markdown(
        """
        <button class="button-with-logo">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/CSV_Logo.svg/1200px-CSV_Logo.svg.png?20110315021805" alt="Logo" width="105" height="70">  
        </button>
        """
        , unsafe_allow_html=True)
    
    
    if st.button("Download CSV"):
        df_srape = scraping(keyword, start_date, end_date, No_of_Tweets)
        st.download_button(
                    label='Download CSV',
                    data=df_srape.to_csv().encode('utf-8'),
                    file_name = keyword+'.csv',
                    mime='text/csv')
        st.success("!Your CSV File is Ready!")

with Json:

    st.markdown(
        """
        <button class="button-with-logo">
            <img src="https://www.seekpng.com/png/full/353-3530209_logo-json.png" alt="Logo" width="110" height="70">  
        </button>
        """
        , unsafe_allow_html=True)
        
    if st.button("Download Json"):
        df_srape = scraping(keyword, start_date, end_date, No_of_Tweets)
        st.download_button(
                    label='Download JSON',
                    data=df_srape.to_json().encode('utf-8'),
                    file_name = keyword+'.json',
                    mime='application/json'
                )
        st.success("!Your Json File is ready!")

