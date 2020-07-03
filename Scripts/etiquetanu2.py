import csv

myData = list()

with open('./data.csv') as csvfile:
    with open('./datadabase.csv', 'w') as csvfile1:
        fieldnames = ['row ID','LINK']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
print("ReWriting Complete")