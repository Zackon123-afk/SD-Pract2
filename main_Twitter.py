from datetime import datetime
import string
from lithops import Storage
from lithops.multiprocessing import Pool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import mtranslate
import json
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import collections

BUCKET="2sdpractica"

def get_auth():
    
    return auth

def tweepy_scan(word):
    global BUCKET
   
    auth = get_auth()
    api = tweepy.API(auth, wait_on_rate_limit=True)
   
    analyzer = SentimentIntensityAnalyzer()
   
    datos = {
        "Mensaje": [],
        "url": [],
        "sentiment": [],
        "date": [],
        "local":[],
    }
    
    for status in tweepy.Cursor(api.search, q=word, lang="es", tweet_mode="extended").items(250): #numberOftwets
        datos["Mensaje"].append(status.full_text)
        datos["url"].append("https://twitter.com/twitter/statuses/"+str(status.id)+",")
        datos["date"].append(status.created_at.strftime("%m/%d/%Y %H:%M:%S"))
        datos["local"].append(str(status.user.location))
        print(status.full_text)
        print("---------------------------------------------------------------------------------")

    for text in datos["Mensaje"]:
        string_twi = mtranslate.translate(str(text),"en", "auto")
        datos["sentiment"].append(str(analyzer.polarity_scores(string_twi)['compound']))

    now = datetime.now()
    data = now.strftime("%m/%d/%Y")

    storage = Storage()  
    storage.put_object(BUCKET,data+"-"+word+".json",json.dumps(datos))

def datos_twitter(word):
    global BUCKET

    datos_grafi = {
        "sent_pos" : 0,
        "sent_neg" : 0,
        "mitjana": 0.0,
        "sent_hist": [],
        "word": word,
        "location_count": { 
        }
    }

    now = datetime.now()
    data = now.strftime("%m/%d/%Y")
    key= data+"-"+ word +'.json'

    storage = Storage()
    json_read = storage.get_object(BUCKET,key)
    data = json.loads(json_read)

    mitjana = 0
    for sent in data["sentiment"]:
        sent = float(sent)
        if sent >= 0:
            datos_grafi["sent_pos"] += 1
        else:
            datos_grafi["sent_neg"] += 1
        
        mitjana += sent
        datos_grafi["sent_hist"].append(round(sent, 1))
        
        datos_grafi["mitjana"] = (mitjana/len(data["sentiment"]))
    
    for loc in data["local"]:
        if loc in datos_grafi["location_count"]:
            datos_grafi["location_count"][loc] += 1
        else:
            datos_grafi["location_count"][loc] = 1

    return datos_grafi


def grafic_Sentiment(datos):
    
    plt.figure(figsize=(6,8))
    eje_x = ['Positivo', 'Negativo']
    eje_y = [datos["sent_pos"], datos["sent_neg"]]
    
    ## Creamos Gráfica
    plt.bar(eje_x, eje_y, color = "b", width=0.60)

    ## Legenda en el eje y
    plt.ylabel('Nº Tweets')
    
    ## Título de Gráfica
    plt.title("Sentimiento de los Tweets sobre: " + datos["word"])
    
    ## Mostramos Gráfica
    plt.show()
 



if __name__ == '__main__':
    

    with Pool() as pool: # Comentar que aqui ho fem de 2 en 2 perque el lithops va molt lent i supera el temps de 10 min
        # pool.map(tweepy_scan, [ "covid", "moderna"])
        # pool.map(tweepy_scan,  [ "pfizer", "astrazeneca"])
        # pool.map(tweepy_scan,  [ "sputnik v", "janssen"])
        datos = pool.map( datos_twitter, [ "covid", "moderna", "pfizer", "astrazeneca","sputnik v", "janssen"] )
    
    print(datos[0])
    

    grafic_twitter(datos[0])
    '''
    grafic_twitter("moderna")
    grafic_twitter("pfizer")
    grafic_twitter("astrazeneca")
    grafic_twitter("sputnik v")
    grafic_twitter("janssen")'''
    

    
