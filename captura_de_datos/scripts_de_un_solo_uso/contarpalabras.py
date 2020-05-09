import csv

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.


myData = list()
myData2 = list()

with open('catched_tweets_originales.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    ii = 0
    for row in reader:

        countrys = row['country']
        date = row['created_at']
        id = row['id']
        if "1" in id:
            if countrys:
                if date:
                    # print("Fecha")
                    date = date.split(" ", 3)
                    # print(date)
                    if "0" not in date[0]:
                        dia = date[-2]
                        mes = date[1]
                        ii += 1
                        if dia == "13" or "14" or "02" and mes == "Apr":
                            myData2.append(date)
    var = len(myData2)
print("Lectura de archivo, cantidad: {} y el tamaño del arreglo es: {}".format(ii, var))

with open('dataentre3.csv') as csvfile:
    with open('dataentre2.csv', 'w') as csvfile1:
        fieldnames = ['id', 'text', 'screen_name', 'created_at', 'retweet_count', 'favorite_count' \
            , 'friends_count', 'followers_count', 'lang', 'country']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, delimiter=',')
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        i = 0
        iii = 0
        iiii = 0
        for row in reader:
            countrys = row['country']
            date = row['created_at']
            id = row['id']
            if "1" in id:
                if countrys:
                    if date:
                        # print("Fecha")
                        date = date.split(" ", 3)
                        # print(date)
                        if "0" not in date[0]:
                            myData.append({'id': row['id'], 'text': row['text'], 'screen_name': row['screen_name'],
                                           'created_at': row['created_at'] \
                                              , 'retweet_count': row['retweet_count'],
                                           'favorite_count': row['favorite_count'],
                                           'friends_count': row['friends_count'], \
                                           'followers_count': row['followers_count'], 'lang': row['lang'],
                                           'country': row['country']})
                            writer.writerows(myData)
                            myData.pop()
                else:
                    if date:
                        # print("Fecha")
                        date = date.split(" ", 3)
                        # print(date)
                        if "0" not in date[0]:
                            dia = date[-2]
                            mes = date[1]

                            if dia == "02" and mes == "May":
                                iii += 1
                                if myData2:
                                    datanew = myData2.pop(0)
                                    dianew = "Wed"
                                    mesnew = "Apr"
                                    dianew2 = "Wed"
                                    createat = dianew2 + " " + mesnew + " " + " " + dianew + "  " + datanew[-1]
                                    myData.append(
                                        {'id': row['id'], 'text': row['text'], 'screen_name': row['screen_name'],
                                         'created_at': createat \
                                            , 'retweet_count': row['retweet_count'],
                                         'favorite_count': row['favorite_count'], 'friends_count': row['friends_count'], \
                                         'followers_count': row['followers_count'], 'lang': row['lang'],
                                         'country': row['country']})
                                    writer.writerows(myData)
                                    myData.pop()
                                    iiii += 1
                                else:
                                    myData.append(
                                        {'id': row['id'], 'text': row['text'], 'screen_name': row['screen_name'],
                                         'created_at': row['created_at'] \
                                            , 'retweet_count': row['retweet_count'],
                                         'favorite_count': row['favorite_count'], 'friends_count': row['friends_count'], \
                                         'followers_count': row['followers_count'], 'lang': row['lang'],
                                         'country': row['country']})
                                    writer.writerows(myData)
                                    myData.pop()
                            else:
                                myData.append({'id': row['id'], 'text': row['text'], 'screen_name': row['screen_name'],
                                               'created_at': row['created_at'] \
                                                  , 'retweet_count': row['retweet_count'],
                                               'favorite_count': row['favorite_count'],
                                               'friends_count': row['friends_count'], \
                                               'followers_count': row['followers_count'], 'lang': row['lang'],
                                               'country': row['country']})
                                writer.writerows(myData)
                                myData.pop()
                    """ question = q+" "+contact_form +" "+first_process+" "+second_process+" "+sentiment+" "+tag2+" "+"<"+questions[-1]
            myData.append({'questions':question, 'answers':row['answers']})
            writer.writerows(myData)
            myData.pop()
             """
            i += 1

print("Tamaño real de la data: {}".format(i))
print("Tamaño real de la para cambiar: {}".format(ii))
print("Tamaño real de la a cambiar: {}".format(iii))
print("Tamaño real de la cambiada: {}".format(iiii))
print("ReWriting Complete")
# print(myData1)
