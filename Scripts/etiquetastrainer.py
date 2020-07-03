import csv


def linkscarlos():
    
    myData = list()

    with open('./data/etiquetastrainerantiguas.csv') as csvfile:
        with open('./data/etiquetastrainernuevo.csv', 'w') as csvfile1:
            fieldnames = ['URL', 'PAIS', 'BITLY OFICIAL']
            writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
            writer.writeheader()
            reader = csv.DictReader(csvfile)
            for row in reader:
                etiqueta = row['BITLY OFICIAL']
                text = etiqueta.split("/")
                text1 = "#"+text.pop()
                myData.append({'URL':row['URL'], 'PAIS':row['PAIS'], 'BITLY OFICIAL':text1})
                writer.writerows(myData)
                myData.pop()                                      
    return print("ReWriting Complete")


    
myData = list()

with open('./data.csv') as csvfile:
    with open('./data1.csv', 'w') as csvfile1:

        fieldnames = ["row ID","Short","LINK","Etiqueta"]
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            etiqueta = row['LINK']
            text = etiqueta.split("/")
            text1 = text.pop()
            text2 = "#"+"co"+text.pop()
            if "?" or "." in text1:
                text3 = text1.split("?")
                if text3[0]:
                    valor1="#"+"co"+text3[0]
                    myData.append({'row ID':row['row ID'],'Short':row['Short'],'LINK':row['LINK'],'Etiqueta':valor1})
                    writer.writerows(myData)
                    myData.pop()                                      
                else:
                    valor2=text2
                    myData.append({'row ID':row['row ID'],'Short':row['Short'],'LINK':row['LINK'],'Etiqueta':valor2})
                    writer.writerows(myData)
                    myData.pop()                                      

print("ReWriting Complete")