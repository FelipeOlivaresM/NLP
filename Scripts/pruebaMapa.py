import csv
import re

myData = list()
counts = dict()  # diccionario de pares { <country>: <count> } 
   
i=0
ii=0
with open('catched_tweets_full_data_taged.csv') as csvfile:
    with open('pais.csv', 'w') as csvfile1:
        fieldnames = ['pais','cantidad']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            #if i == 15: break
            obj = row['country']
            if obj == "Estados Unidos":
                #print(obj)
                obj = "United States"
                
            polarity = int(row['sentiment'])
            #print(obj,"\n")
            #print(polarity)
            if obj:
#                if polarity==1:
                    
                if obj in counts:
                    
                    counts[obj] += 1 #Adiciona 1 a una entrada existente
                else:
                    counts[obj] = 1 #Crea un nuevo indice/palabra en el diccionario.
                i+=1 
        for obj1,obj2 in counts.items():
            myData.append({'pais':obj1,'cantidad':obj2})
            writer.writerows(myData)
            myData.pop()
            ii+=1
        
            
                    
print("Tamaño real de la data: {}".format(i))
print("Tamaño data con pais: {}".format(ii))
print("ReWriting Complete \n")
print(counts)

#print(myData1)

