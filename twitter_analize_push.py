import tweepy
import pandas as pd
from lithops import Storage
import csv
from autenticacion_tweppy import get_auth
import os



'''
Codigo para la creación de el fichero
'''
def create_headercsv(filename):
    csvFile = open(filename, 'w', newline='')
    csvWriter = csv.writer(csvFile)
    
    cabecera=['Fecha_creación','Texto','Fuente','Localización','URL','Idioma']

    csvWriter.writerow(cabecera)
    csvFile.close()
    print("File and header created correctly") 


'''
Codigo para recoger la informacion del tweet y guardarlo en un csv
'''
def process_status(status,filename):
    csvFile = open(filename, 'a', newline='', encoding="utf-8")
    csvWriter = csv.writer(csvFile)
    if status is not False:
        texto = status.full_text
        print(texto)
        url = "https://twitter.com/twitter/statuses/"+str(status.id)
        linea = [status.created_at, texto, status.source, status.user.location,url ,status.lang]
        csvWriter.writerow(linea)
    print("Almacenamos Tweet")
    csvFile.close()
    print("fin")

    return linea;


def tweepy_scan_csv(word ,filename, nom_bucket):
    
    auth = get_auth()
    api = tweepy.API(auth)

    create_headercsv(filename)

    cabecera=['Fecha_creación','Texto','Fuente','Localización','URL','Idioma']
    datos = str(cabecera)+"\n"
    print(datos)

    qstring=word+" lang=ca OR lang:es"
    for status in tweepy.Cursor(api.search, q=qstring ,tweet_mode="extended").items(1): #numberOftwets
        datos += str(process_status(status,filename))+ "\n"
    print("-------------------------------------------------------------------------------------------------------------------------------")
     
    print(datos)
    storage = Storage()
    storage.put_object(nom_bucket,"twitter_analize.csv", datos)

if __name__ == '__main__':
    tweepy_scan_csv("covid","prova.csv","2sdpractica")    

