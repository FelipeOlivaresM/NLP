import csv
import re

myData = list()
myData2 = list()

with open('dataentre2.csv') as csvfile:
    with open('dataentre1.csv', 'w') as csvfile1:
        with open('dataentre12.csv', 'w') as csvfile2:
            fieldnames = ['id','text','screen_name','created_at','retweet_count','favorite_count'\
                ,'friends_count','followers_count','lang','country']
            writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
            writer.writeheader()
            writer1 = csv.DictWriter(csvfile2, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
            writer1.writeheader()
            reader = csv.DictReader(csvfile)
            for row in reader:
                lang = row['lang']
                if lang == "es":

                    myData.append({'id':row['id'],'text':row['text'],'screen_name':row['screen_name'],'created_at':row['created_at']\
                    ,'retweet_count':row['retweet_count'],'favorite_count':row['favorite_count'],'friends_count':row['friends_count'],\
                    'followers_count':row['followers_count'],'lang':row['lang'],'country':row['country']})
                    writer.writerows(myData)
                    myData.pop()
                else:
                    myData.append({'id':row['id'],'text':row['text'],'screen_name':row['screen_name'],'created_at':row['created_at']\
                    ,'retweet_count':row['retweet_count'],'favorite_count':row['favorite_count'],'friends_count':row['friends_count'],\
                    'followers_count':row['followers_count'],'lang':row['lang'],'country':row['country']})
                    writer1.writerows(myData)
                    myData.pop()
                
print("ReWriting Complete")