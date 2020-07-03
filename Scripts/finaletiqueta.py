import csv

myData = list()
myData2 = list()
myData3 = list()

with open('./data/etiquetastrainernuevo.csv') as csvfile2:
    reader = csv.DictReader(csvfile2)
    for row in reader:
        etiqueta2 = row['BITLY OFICIAL']
        etiqueta3 = row['URL']
        myData2.append(etiqueta2)
        myData3.append(etiqueta3)
    
with open('./data/linksfromdatabase.csv') as csvfile:
    with open('./data/etiquetaslinksdabase.csv', 'w') as csvfile1:
        fieldnames = ['row ID', 'Short', 'LINK','Etiqueta']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        for row in reader:
            etiqueta = row['LINK']
            if etiqueta in myData3:
                numero = myData3.index(etiqueta)
                myData.append({'row ID':row['row ID'], 'Short':row['Short'], 'LINK':row['LINK'],'Etiqueta':str(myData2[numero])})
                writer.writerows(myData)
                myData.pop()
            else:
                myData.append({'row ID':row['row ID'], 'Short':row['Short'], 'LINK':row['LINK'],'Etiqueta':'none'})
                writer.writerows(myData)
                myData.pop()
print("ReWriting Complete")