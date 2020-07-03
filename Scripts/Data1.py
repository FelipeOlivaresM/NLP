import csv
import re

myData = list()


with open('dataentre8.csv') as csvfile:
    with open('dataentre6.csv', 'w') as csvfile1:
        fieldnames = ['questions','answers','links','first_process','second_process','sentiment','contact_form','tag']
        #,'links','first_process','second_process','sentiment','contact_form','tag'
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        i= 0
        CwordT= 0
        for row in reader:
            #if i==10:break
            q = row['questions'].split(" ")
            tag = row['tag'].split("-")
            #print(len(q))
            if q and len(q)>7:
                myData.append({'questions':row['questions'], 'answers':row['answers'],'links':row['links'],\
                'first_process':row['first_process'],'second_process':row['second_process'],\
                'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag[0],})
                CwordT+=1
                writer.writerows(myData)
                myData.pop()     

            """ ,'links':row['links'],\
                'first_process':row['first_process'],'second_process':row['second_process'],\
                'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag2,'wordCantQues':wordcant,'wordCantAnsw':wordcantans """
                   
            i+=1 
                    
print("Tamaño real de la data: {}".format(i))
print("Tamaño de la data luego de primer procesamiento: {}".format(CwordT))
print("ReWriting Complete")
#print(myData1)