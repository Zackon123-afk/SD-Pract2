from re import A
from lithops import Storage
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
import json
import numpy as np
import collections

nom_bucket="2sdpractica"
key= '05/26/2021-covid.json'

storage = Storage()
json_read = storage.get_object(nom_bucket,key)
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
fig.suptitle('Estudi de la paraula')
# plt.bar(x_value,y_value)

