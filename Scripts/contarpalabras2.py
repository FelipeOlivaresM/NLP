import csv
import re

myData = list()
myData2 = list()

   

with open('datasentimenten.csv') as csvfile:
    with open('datainglesneutral.csv', 'w') as csvfile1:
        fieldnames = ['id','text','screen_name','created_at','retweet_count','favorite_count'\
            ,'friends_count','followers_count','lang','country','polarity']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        i=0
        ii=0
        for row in reader:
            if i==2500:break
            text = row['id']
            text1 = row['text'].split(" ")
            lang = row['lang']
            if text:
                myData.append({'id':row['id'],'text':row['text'],'screen_name':row['screen_name'],'created_at':row['created_at']\
                ,'retweet_count':row['retweet_count'],'favorite_count':row['favorite_count'],'friends_count':row['friends_count'],\
                'followers_count':row['followers_count'],'lang':row['lang'],'country':row['country'],'polarity':"neutral"})
                writer.writerows(myData)
                myData.pop()
                ii+=1
            i+=1 
        
            
                    
print("Tamaño real de la data: {}".format(i))
print("Tamaño data español: {}".format(ii))
print("ReWriting Complete")
#print(myData1)

