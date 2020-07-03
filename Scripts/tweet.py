""" install pip install tweepy
 """
import json
import pandas as pd
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pandas.io import sql
from pandas.io.json import json_normalize
import csv

print("Iniciamos")

#Declare variables that contains the user credentials to access Twitter API
#You can get your own keys in https://apps.twitter.com/
#--------------------------------------------------------------------------------
aToken =       "341230963-TZcim2NWHj9KLE2RrLp9YIehW7j6PB4iZqnRDYeA"
aTokenSecret = "x3pYbRJT3djpad4voodrepw3mN2VmLxNX45ktV0foqkKh"
cKey =         "8Jco2vpYtvvuj2UjeK75aQRWA"
cSecret =      "JsB5NFUFXueV5I2Oy2uPTuVpkMXFQV06XpIV1dpHQmNilWplMj"


print("Definir arreglo para guardar la data")

bufferSize=30
twittsBuffer = []

tData = list()

def AddTwittToBuffer(twitt):
    
    global twittsBuffer
    twittsBuffer.append(twitt)
    
    if (len(twittsBuffer) == bufferSize):
        AddTwittsTo(twittsBuffer)
    return 

def AddTwittsTo(twitts):
    with open('./prueba.csv', 'w') as csvfile:
        fieldnames = ['id','text','screen_name','created_at','retweet_count',\
            'favorite_count','friends_count','followers_count','lang','country']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for t in twitts:
            if t['place'] != None :
                tData.append({'id':t['id'],\
                    'text':t['text'],\
                    'screen_name':t['user']['screen_name'],\
                    'created_at':t['created_at'],\
                    'retweet_count':t['retweet_count'],\
                    'favorite_count':t['favorite_count'],\
                    'friends_count':t['user']['friends_count'],\
                    'followers_count':t['user']['followers_count'],\
                    'lang':t['lang'],\
                    'country':t['place']['country']
                    })
                writer.writerows(tData)
                tData.pop()                                       
            else :
                tData.append({'id':t['id'],\
                    'text':t['text'],\
                    'screen_name':t['user']['screen_name'],\
                    'created_at':t['created_at'],\
                    'retweet_count':t['retweet_count'],\
                    'favorite_count':t['favorite_count'],\
                    'friends_count':t['user']['friends_count'],\
                    'followers_count':t['user']['followers_count'],\
                    'lang':t['lang'],\
                    'country':'None'
                    })
            print("\n")
            print("Data")
            print(tData)
            writer.writerows(tData)
            print("\n")
            tData.pop()                                       
            
        
        print("\n GUARDANDO LA DATA CRACK")
        
        return False


#--------------------------------------------------------------------------------
#Create a listener class that process received tweets
#On error print status
#--------------------------------------------------------------------------------
class StdOutListener(StreamListener):
    def on_data(self, data):
        t= json.loads(data)
        AddTwittToBuffer(t)
        return 
    def on_error(self, status):
        print(status)
if __name__ == '__main__':
    myListener = StdOutListener()
    authenticator = OAuthHandler(cKey, cSecret)
    authenticator.set_access_token(aToken, aTokenSecret)
    stream = Stream(authenticator, myListener)
    stream.filter(languages=['en','es'],track=['Coronavirus','coronavirus','covid-19','COVID-19'])
    