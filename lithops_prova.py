from lithops import Storage
from lithops.multiprocessing import Pool
import tweepy


storage = Storage()

storage.put_object('2sdpractica','test.txt','jajaj xd')

def double(i):
    return i * 2

with Pool() as pool:
    result = pool.map(double, [1, 2, 3, 4, 5])
    print(result)



