import tweepy
import pandas as pd

auth = tweepy.OAuthHandler("G7oVPMZP776iDbfLW6KRIlvg6", "MnH3qXuRHfoJXSzXSPdtneAvLCJ2MslvKskHHq0qvrAdNiUyox")
auth.set_access_token("1059931089999945729-AAimzlFRpPy6RSQqESCM1XJJZAmtbn", "4Sq5Ga0aLC2PIgdzWWIp5ISY4iNFg6cRshJJpQUv12j9u")

api = tweepy.API(auth)

numberOfTweets=20
cursor = tweepy.Cursor(api.search, q="covid-19 lang=ca OR lang:es",tweet_mode="extended").items(numberOfTweets)
tweets=[]
likes=[]
time=[]

for i in cursor:
    tweets.append(i.full_text)
    likes.append(i.favorite_count)
    time.append(i.created_at)

df = pd.DataFrame({'tweets':tweets,'likes':likes,'time':time})
df = df[~df.tweets.str.contains("RT")]
df = df.reset_index(drop=True)
df

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)