import csv
import re

myData = list()
myData1 = list()
myData2 = list()


with open('pruebaTAGS1.csv') as csvfile2:
    print("Inicio")
    reader = csv.DictReader(csvfile2)
    ii=0
    for row in reader:
        id = row['OwnerId']
        print("Row Etiqueta: {}".format(id))
        name = row['Name']
        myData.append(id)
        myData1.append(name)
        ii+=1
    print("\nCantidad de etiquetas: {}".format(ii))


with open('pruebaTAGS.csv') as csvfile:
    with open('Etiqueta1.csv', 'w') as csvfile1:
        fieldnames = ["row ID","OwnerId","Name","CreatedDate","ParentId","Headline","Content","Posted","Provider","Handle",\
            "MediaType","MediaProvider","Sentiment","Status","StatusMessage","Recipient","RecipientType","MessageType","TopicType",\
                "TopicProfileName","CreationDateSalesforce__c","CaseNumber","Origin","Subject","ClosedDate","Intention__c",\
                    "EscalationDateTime__c","Language__c","AviancaSpecificReason__c","createdByKeeper__c","Proceso 1","Tipo2__c",\
                        "Ifscaling__c","SocialPost__c","Base__c","DetalleBase__c","Etiqueta__c","Proceso 2","Proceso 3","Proceso 4",\
                            "keeperManagement__c","FlightNumber2__c","Routes__c","Category__c","TipificacionMass__c",\
                                "FechaCreacionPublicacion__c","Count(OwnerId)","TYPE","DEJAR","LINK","etiqueta_nombre"]
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        i=0
        
        for row in reader:
            #if i==10:break
            obj = row['OwnerId']
            #print(obj)
            if obj in myData:
                index = myData.index(obj)
                #print(index)
            myData2.append({"row ID":row['row ID'],"OwnerId":row['OwnerId'],"Name":row['Name'],"CreatedDate":row['CreatedDate'],"ParentId":row['ParentId'],\
            "Headline":row['Headline'],"Content":row['Content'],"Posted":row['Posted'],"Provider":row['Provider'],"Handle":row['Handle'],\
            "MediaType":row['MediaType'],"MediaProvider":row['MediaProvider'],"Sentiment":row['Sentiment'],"Status":row['Status'],\
            "StatusMessage":row['StatusMessage'],"Recipient":row['Recipient'],"RecipientType":row['RecipientType'],"MessageType":row['MessageType'],"TopicType":row['TopicType'],\
            "TopicProfileName":row['TopicProfileName'],"CreationDateSalesforce__c":row['CreationDateSalesforce__c'],"CaseNumber":row['CaseNumber'],"Origin":row['Origin'],\
            "Subject":row['Subject'],"ClosedDate":row['ClosedDate'],"Intention__c":row['Intention__c'],\
            "EscalationDateTime__c":row['EscalationDateTime__c'],"Language__c":row['Language__c'],"AviancaSpecificReason__c":row['AviancaSpecificReason__c'],\
            "createdByKeeper__c":row['createdByKeeper__c'],"Proceso 1":row['Proceso 1'],"Tipo2__c":row['Tipo2__c'],\
            "Ifscaling__c":row['Ifscaling__c'],"SocialPost__c":row['SocialPost__c'],"Base__c":row['Base__c'],"DetalleBase__c":row['DetalleBase__c'],\
            "Etiqueta__c":row['Etiqueta__c'],"Proceso 2":row['Proceso 2'],"Proceso 3":row['Proceso 3'],"Proceso 4":row['Proceso 4'],\
            "keeperManagement__c":row['keeperManagement__c'],"FlightNumber2__c":row['FlightNumber2__c'],"Routes__c":row['Routes__c'],"Category__c":row['Category__c'],\
            "TipificacionMass__c":row['TipificacionMass__c'],\
            "FechaCreacionPublicacion__c":row['FechaCreacionPublicacion__c'],"Count(OwnerId)":row['Count(OwnerId)'],"TYPE":row['TYPE'],"DEJAR":row['DEJAR'],\
            "LINK":row['LINK'],"etiqueta_nombre":myData1[index]})
            writer.writerows(myData2)
            myData2.pop()
            i+=1
print("ReWriting Complete")
print(i)        
#print(myData)