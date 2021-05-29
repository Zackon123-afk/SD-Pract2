#from urllib.request import urlopen
from lithops import Storage
import json
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *

nom_bucket="2sdpractica"
key="quotes-COVID19.html"
storage = Storage()

def eliminateNaNs(list) :
    i = 0
    for x in list :
        if str(x) == 'nan':
            list[i] = 0
        i+=1
    return list

#Treatment of json to pandas
nom_bucket="2sdpractica"
key= '05/27/2021-web.json'
storage = Storage()
json_read = storage.get_object(nom_bucket,key)
data_analize = json.loads(json_read)
df = pd.DataFrame.from_dict(data_analize,orient='columns')
df["likes"]=df["likes"].astype(int)


# average likes about key words
likesSARS=df[df["titol"].str.contains("SARS-CoV")].mean()["likes"]
likesModerna=df[df["titol"].str.contains("Moderna")].mean()["likes"]
likesPfizer=df[df["titol"].str.contains("Pfizer")].mean()["likes"]
likesAstra=df[df["titol"].str.contains("AstraZeneca")].mean()["likes"]

name = ['SARS','Moderna','Pfizer','AstraZeneca']
allLikes = [likesSARS,likesModerna,likesPfizer,likesAstra]
allLikes = eliminateNaNs(allLikes)

plt.bar(name,allLikes)
plt.show()

