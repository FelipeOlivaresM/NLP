import csv

myData = list()

with open('./data/Data1BytlyLinks.csv') as csvfile:
    with open('./data/linksfromdatabase.csv', 'w') as csvfile1:
        fieldnames = ['row ID', 'Short', 'LINK']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            if row['Short'] == row['LINK']:
                myData.append({'row ID':row['row ID'], 'Short':row['Short'], 'LINK':'none'})
            else:
                myData.append({'row ID':row['row ID'], 'Short':row['Short'], 'LINK':row['LINK']})
            writer.writerows(myData)
            myData.pop()                                      
print("ReWriting Complete")