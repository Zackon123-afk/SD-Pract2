from lithops import Storage
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
import json

nom_bucket="2sdpractica"
now = datetime.now()
data = now.strftime("%m/%d/%Y")
word = 'covid'
key= '05/17/2021 21:26:11-covid.json'

storage = Storage()
json_read = storage.get_object(nom_bucket,key)
data_analize = json.loads(json_read)


print(data_analize['Mensaje'][2])

datos=