import csv,sys
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

myData = list()

stop_words = set(stopwords.words('spanish')) 

with open('datadiez.csv') as csvfile:
    with open('dataonce.csv', 'w') as csvfile1:
        fieldnames = ['questions','answers','links','first_process','second_process',\
        'sentiment','contact_form','tag','wordCantQues','wordCantAnsw']
        #,'links','first_process','second_process','sentiment','contact_form','tag'
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        i=0
        ii=0
        countwordsrep=0
        for row in reader:
            q = row['questions']
            answq = row['answers']
            textrep = re.search(r"^\b_TWITTER_", answq)
            
            if not textrep:
                #if i==6:break
                signpoint = re.search(r"\¿.*?\?", answq)
                respuestasinsignos = answq
                if not signpoint:
                    respuestasinsignos = re.sub("\?", "", answq)
                
                word_tokens = word_tokenize(q)  
                filtered_sentence = [w for w in word_tokens if not w in stop_words] 
                filtered_sentence = [] 
                for w in word_tokens: 
                    if w not in stop_words: 
                        filtered_sentence.append(w)
                text = (' '.join(filtered_sentence))
                text1 = re.sub(r"([?.¡:!,¿()])", "", text)
                text1 = text1.strip()
                wordcant = len(text1.split(" "))
                answerCant = row['answers'].split(" ")
                answerCant = len(answerCant)
                contact_form = row['contact_form']
                first_process = row['first_process']
                second_process = row['second_process']
                sentiment = row['sentiment']
                links = row['links']
                if not links: links="none"
                tag = row['tag']
                if not tag: tag = "none"

                links = links.strip()
                if answerCant<65 and wordcant<65 and answerCant>8 :
                    myData.append({'questions':text1, 'answers':respuestasinsignos,'links':links,\
                        'first_process':row['first_process'],'second_process':row['second_process'],\
                        'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag,\
                        'wordCantQues':wordcant,'wordCantAnsw':answerCant})
                    """ ,'links':row['links'],\
                        'first_process':row['first_process'],'second_process':row['second_process'],\
                        'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag2,'wordCantQues':wordcant,'wordCantAnsw':wordcantans """
                    writer.writerows(myData)
                    myData.pop()         
                    ii+=1   
                i+=1
            else: 
                #if i==6:break
                signpoint1 = re.search(r"\¿.*?\?", answq)
                awq = answq.split(" ",1)
                palabra1 = "_TWITTER_"
                if not signpoint1:
                    respuestasinsignos = re.sub("\?", "", awq[-1])
                else: respuestasinsignos = awq[-1]
                awq = palabra1 +" "+ respuestasinsignos
                countwordsrep +=1
                word_tokens = word_tokenize(q)  
                filtered_sentence = [w for w in word_tokens if not w in stop_words] 
                filtered_sentence = [] 
                for w in word_tokens: 
                    if w not in stop_words: 
                        filtered_sentence.append(w)
                text = (' '.join(filtered_sentence))
                text1 = re.sub(r"([?.¡:!,¿()])", "", text)
                text1 = text1.strip()
                wordcant = len(text1.split(" "))
                answerCant = row['answers'].split(" ")
                answerCant = len(answerCant)
                contact_form = row['contact_form']
                first_process = row['first_process']
                second_process = row['second_process']
                sentiment = row['sentiment']
                links = row['links']
                if not links: links="none"
                tag = row['tag']
                if not tag: tag = "none"
                links = links.strip()
                if answerCant<65 and wordcant<65 and answerCant>8 :
                    myData.append({'questions':text1, 'answers':awq,'links':links,\
                        'first_process':row['first_process'],'second_process':row['second_process'],\
                        'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag,\
                        'wordCantQues':wordcant,'wordCantAnsw':answerCant})
                    """ ,'links':row['links'],\
                        'first_process':row['first_process'],'second_process':row['second_process'],\
                        'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag2,'wordCantQues':wordcant,'wordCantAnsw':wordcantans """
                    writer.writerows(myData)
                    myData.pop()         
                    ii+=1   
                i+=1







                    
print("Tamaño real de la data: {}".format(i))
print("Tamaño real de la data escrita con limitaciones de palabras: {}".format(ii))
print("Cantidad de data con la palabra a buscar: {}".format(countwordsrep))

print("ReWriting Complete")
#print(myData1)