import csv
import re

myData = list()
myData2 = list()
i=0
ii=0
with open('DataIngles.csv') as csvfile:
    with open('dataingles.csv', 'w') as csvfile1:
        fieldnames = ['id','text','screen_name','created_at','retweet_count','favorite_count'\
            ,'friends_count','followers_count','lang','country']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        for row in reader:
            text = row['text']
            text1 = text.lower()
            text2 = text1.split(" ")
            i+=1
            if  "pray" in text2 : 
                #print("\n"+text) 
                
                myData.append({'id':row['id'],'text':row['text'],'screen_name':row['screen_name'],'created_at':row['created_at']\
                ,'retweet_count':row['retweet_count'],'favorite_count':row['favorite_count'],'friends_count':row['friends_count'],\
                'followers_count':row['followers_count'],'lang':row['lang'],'country':row['country']})
                writer.writerows(myData)
                myData.pop()
                ii+=1
        
                
print("ReWriting Complete")
print(i)
print(ii)


