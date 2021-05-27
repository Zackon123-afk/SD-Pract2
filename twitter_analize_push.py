from datetime import datetime
from lithops import Storage
from lithops.multiprocessing import Pool
from autenticacion_tweppy import get_auth
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import tweepy


def get_auth():
    auth = tweepy.OAuthHandler("G7oVPMZP776iDbfLW6KRIlvg6", "MnH3qXuRHfoJXSzXSPdtneAvLCJ2MslvKskHHq0qvrAdNiUyox")
    auth.set_access_token("1059931089999945729-AAimzlFRpPy6RSQqESCM1XJJZAmtbn", "4Sq5Ga0aLC2PIgdzWWIp5ISY4iNFg6cRshJJpQUv12j9u")
    return auth

def tweepy_scan(word, nom_bucket):
    

    storage = Storage()
    storage.put_object('2sdpractica','testxd.txt','jajajjaa')
    
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
    
    for status in tweepy.Cursor(api.search, q=qstring ,tweet_mode="extended").items(500): #numberOftwets

        print("-------------------------------------------------------------------------------------------------------------------------------" + str(i))

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
    storage.put_object(nom_bucket,data+"-"+word+".json",json.dumps(datos))




if __name__ == '__main__':
 
    
   
    
    with Pool() as pool:
        result = pool.starmap(tweepy_scan, [("covid","2sdpractica"),("moderna","2sdpractica")] )
    
       


#("pfizer","2sdpractica"), ("moderna","2sdpractica"), ("astrazeneca","2sdpractica"), ("sputnik v","2sdpractica"), ("janssen","2sdpractica")])

