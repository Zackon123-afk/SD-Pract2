import tweepy
from lithops import Storage
import csv
from autenticacion_tweppy import get_auth
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



'''
Codigo para la creación de el fichero
'''
def create_headercsv(filename):
    csvFile = open(filename, 'w', newline='')
    csvWriter = csv.writer(csvFile)
    
    cabecera=['Fecha_creación','Texto','Fuente','Localización','URL','Idioma','Sentimiento']

    csvWriter.writerow(cabecera)
    csvFile.close()
    print("File and header created correctly") 

#----------------------------------------------------------------------------------------------------------------------------------------
'''
Codigo para recoger la informacion del tweet y guardarlo en un csv
'''
def process_statusCsv(status,filename):
    csvFile = open(filename, 'a', newline='', encoding="utf-8")
    csvWriter = csv.writer(csvFile)
    
    if status is not False:
        texto = status.full_text
        url = "https://twitter.com/twitter/statuses/"+str(status.id)
        
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(texto)
        data = status.created_at.strftime("%m/%d/%Y %H:%M:%S")
        linea = data+","+texto+"," +status.source+","+ status.user.location+","+url +","+status.lang+","+str(vs['compound'])

        lineacsv = [status.created_at, texto, status.source, status.user.location,url ,status.lang, vs['compound']]
        csvWriter.writerow(lineacsv)

    csvFile.close()
    
   
    return linea;

#----------------------------------------------------------------------------------------------------------------------------------------
def tweepy_scan_csv(word ,filename, nom_bucket):
    
    auth = get_auth()
    api = tweepy.API(auth)

    create_headercsv(filename)

    cabecera="Fecha_creación,Texto,Fuente,Localización,URL,Idioma,Sentimiento"
    datos = str(cabecera)+"\n"
    print(datos)

    qstring=word+" lang=ca OR lang:es"
    for status in tweepy.Cursor(api.search, q=qstring ,tweet_mode="extended").items(1): #numberOftwets
        datos += process_statusCsv(status,filename)+ "\n"
    print("-------------------------------------------------------------------------------------------------------------------------------")
     
    print(datos)
    storage = Storage()
    storage.put_object(nom_bucket,"twitter_analize.csv", datos)
#----------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    tweepy_scan_csv("covid","prova.csv","2sdpractica")    

