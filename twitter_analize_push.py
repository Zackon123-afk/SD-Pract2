import tweepy
from lithops import Storage
import csv
from autenticacion_tweppy import get_auth
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json



def tweepy_scan(word, nom_bucket):
    
    auth = get_auth()
    api = tweepy.API(auth, wait_on_rate_limit=True)

    #create_headercsv(filename)
   
    analyzer = SentimentIntensityAnalyzer()
    qstring=word+" lang=ca OR lang:es"
   
    
    i = 0;
    textos = []
    urls = []
    sentiments = []
    dates = []
    local = []
    source = []
    lenguaje = []
    
    for status in tweepy.Cursor(api.search, q=qstring ,tweet_mode="extended").items(2): #numberOftwets

        print("-------------------------------------------------------------------------------------------------------------------------------")
        textos.append(status.full_text)
        urls.append("https://twitter.com/twitter/statuses/"+str(status.id)+",")
        sentiments.append(str(analyzer.polarity_scores(textos[i])['compound']))
        dates.append(status.created_at.strftime("%m/%d/%Y %H:%M:%S"))
        local.append(str(status.user.location))
        source.append(str(status.source))
        lenguaje.append(str(status.lang))
        i += 1;

       
    
    datos = {
        "Mensaje": textos,
        "url": [urls],
        "sentiment": [sentiments],
        "date": [dates],
        "local": [local],
        "source": [source],
        "lenguaje": [lenguaje]
    }

    storage = Storage()  
    storage.put_object(nom_bucket,"stats"+word+".json",json.dumps(datos))

#----------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    tweepy_scan("covid","2sdpractica")    

