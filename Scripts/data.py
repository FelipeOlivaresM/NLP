import csv
import re

myData = list()

i=0
with open('datanuevalimpia.csv') as csvfile:
    with open('dataentre7.csv', 'w') as csvfile1:
        fieldnames = ['QUESTION','ANSWER','LINK','Proceso 1','Proceso 2','Proceso 3','Proceso 4','Sentiment','CreatedDate','Provider','Name','tag','Language__c']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        for row in reader:
            myData.append({'QUESTION':row['QUESTION'], 'ANSWER':row['ANSWER'],'LINK':row['LINK'],\
                'Proceso 1':row['Proceso 1'],'Proceso 2':row['Proceso 2'],'Proceso 3':row['Proceso 3'],'Proceso 4':row['Proceso 4'],\
                'Sentiment':row['Sentiment'],'CreatedDate':row['CreatedDate'],'Provider':row['Provider'],'Name':row['Name'],'tag':row['tag'],'Language__c':row['Language__c']})
            """ ,'links':row['links'],\
                'first_process':row['first_process'],'  second_process':row['second_process'],\
                'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag2,'wordCantQues':wordcant,'wordCantAnsw':wordcantans """
            writer.writerows(myData)
            myData.pop()            
            i+=1 

print("Tamaño real de la data: {}".format(i))
print("ReWriting Complete")
#print(myData1)