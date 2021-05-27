from datetime import datetime
from lithops import Storage
from lithops.multiprocessing import Pool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import tweepy

import pandas as pd
import matplotlib.pyplot as plt
import collections

BUCKET="2sdpractica"

def get_auth():
    auth = tweepy.OAuthHandler("G7oVPMZP776iDbfLW6KRIlvg6", "MnH3qXuRHfoJXSzXSPdtneAvLCJ2MslvKskHHq0qvrAdNiUyox")
    auth.set_access_token("1059931089999945729-AAimzlFRpPy6RSQqESCM1XJJZAmtbn", "4Sq5Ga0aLC2PIgdzWWIp5ISY4iNFg6cRshJJpQUv12j9u")
    return auth

def tweepy_scan(word):
    global BUCKET

    auth = get_auth()
    api = tweepy.API(auth, wait_on_rate_limit=True)
   
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
    
    for status in tweepy.Cursor(api.search, q=qstring ,tweet_mode="extended").items(500): #numberOftwets

        #print("-------------------------------------------------------------------------------------------------------------------------------" + str(i))
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
        "url": urls,
        "sentiment": sentiments,
        "date": dates,
        "local": local,
        "source": source,
        "lenguaje": lenguaje
    }
    
    now = datetime.now()
    data = now.strftime("%m/%d/%Y")

    storage = Storage()  
    storage.put_object(BUCKET,data+"-"+word+".json",json.dumps(datos))

def grafic_twitter(word):
    global BUCKET
    
    print("wtf")
    now = datetime.now()
    data = now.strftime("%m/%d/%Y")
    key= data +"-"+ word +'.json'

    storage = Storage()
    json_read = storage.get_object(BUCKET,key)
    data_analize = json.loads(json_read)
    df = pd.DataFrame.from_dict(data_analize,orient='columns')
    df["sentiment"]=df["sentiment"].astype(float)

    sent_pos=len(df[df["sentiment"] >= 0])
    sent_neg=len(df[df["sentiment"] < 0])
    sents=[sent_pos,sent_neg]
    noms=['Positiu','Negatiu']
   
    ###############################################################################
    
    llista=list(df["sentiment"].astype(float))
    ocurrences = collections.Counter(llista)
    dictionary = ocurrences.items()
    dfa= pd.DataFrame.from_dict(dictionary,orient='columns')
    dfa.columns = ['value','quantity']
    dfa['quantity']= dfa['quantity'].astype(float)
    x_value=list(dfa["value"])
    y_value=list(dfa["quantity"])

    fig, (axs1, axs2)= plt.subplots(1,2)

    axs1.bar(noms,sents)
    axs1.set_title('Diferencia del sentiment')
    axs2.bar(x_value,y_value)
    axs2.set_title('Concentració del sentiment')
    fig.suptitle('Estudi de la paraula:'+word)
    # plt.bar(x_value,y_value)



if __name__ == '__main__':
 
    #with Pool() as pool:
        #pool.map(tweepy_scan,  [ "covid", "moderna"])
        #pool.map(tweepy_scan,  [ "pfizer", "astrazeneca"])
        #pool.map(tweepy_scan,  [ "sputnik v", "janssen"])
        #pool.map(grafic_twitter, [ "covid", "moderna"])#, "pfizer", "astrazeneca", "sputnik v","janssen"])
    

    grafic_twitter("covid")
    grafic_twitter("moderna")
    grafic_twitter("pfizer")
    grafic_twitter("astrazeneca")
    grafic_twitter("sputnik v")
    grafic_twitter("janssen")
    

    
