import csv,sys
import re
import math

myData = list()

with open('data15.csv') as csvfile:
    with open('data17.csv', 'w') as csvfile1:
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
            #if i==10:break
            q = row['questions']
            answq = row['answers']
            contact_form = row['contact_form']
            first_process = row['first_process']
            second_process = row['second_process']
            sentiment = row['sentiment']
            links = row['links']
            tag = row['tag'].split("#")
            tag = tag[-1]
            wordCantQues = int(row['wordCantQues'])
            wordCantAnsw = row['wordCantAnsw']
            valordiv = 0
            q1 = q.split(" ")
            valq = len(q1)
            ques = ""
            """ respuestasinsignos = answq
            if valordiv>2:
                resultdiv = abs(valordiv - valq)
                resultdiv1 = round(resultdiv/2)
                if valq - valordiv==1:
                    q1.pop(0)
                    len1 = len(q1)
                    ques = " ".join(q1)
                else: 
                    for ina in range(resultdiv1): q1.pop(0) and q1.pop()
                    len1 = len(q1)
                    ques = " ".join(q1)
                    if len1>valordiv:
                        q1.pop(0)
                        len1 = len(q1)
                        ques = " ".join(q1)
                myData.append({'questions':ques, 'answers':respuestasinsignos,'links':links,\
                    'first_process':row['first_process'],'second_process':row['second_process'],\
                    'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag,\
                    'wordCantQues':len(ques.split(" ")),'wordCantAnsw':row['wordCantAnsw']})
                #print("hola")
                writer.writerows(myData)
                myData.pop()         
                i+=1
 """
            #lse:
            signpoint = re.search(r"Zuzanne|Zunilda|Zulymar|Zully|Zoraida|Zinai|Zharon|Zelay|Zednanreh|\
            Zayra|Zayda|Zary|Zamy|Zahimis|Zael|Yuyu|Yuyi|Yuvely|Yusmary|Yurika|Yureivis|Yunke|Yulianis|\
            Yujuma|Yudith|Yudi|Yudely|Yovg|Yovanny|Yovani|Yosmeidis|Yoseph|Yosari|Yorvani|Yorlene|Yordan|\
            Yoojung|Yonnier|Yonier|Yomilys|Yoma|Yolys|Yolie|Yoliana|Yolan|Yoeimar|Yobaina|Yoav|Yoandy|\
            Yitsy|Yiseth|Yirs|Yiro|Yiris|Yiramile|Yiralmile|Yilibeth|Yhossue|Yetzabel|Yess|Yesmin|Yesly|\
            Yesika|Yesidd|Yesi|Yerigel|Yenimar|Yeniferth|Yenifer|Yendry|Yemaya|Yelesm|Yelangel|Yeini|\
            Yeimmy|Yeco|Yeanine|Yaz|Yayii|Yatzi|Yassin|Yasser|Yasid|Yaser|Yasenia|Yas|Yarol|Yárol|Yaqui|\
            Yanpier|Yanni|Yann|Yanky|Yanet|Yanessi|Yanela|Yan|Yamila|Yamil|Yaki|Yair|Yahoska|Yahir|Yadyss|\
            Yadi|Yaciel|Xuezhi|Xiomi|Xime|Xilena|Woody|Wiston|Wilma|Willie|Willi|Willem|Wili|Wilfried|Wilches\
            Wilchel|Wil|Wens|Wendolyne|Wendis|Weiner|Weimar|Wayne|Wayman|Wan|Wal|Waira|Vladi|Vivís|Viro|\
            Virguit|Virgilio|Virgelina|Vinscent|Vinny|Viko|Viki|Vielka|Vicencio|Vic|Vialy|Vhania|Veve|\
            Versys|Veriix|Verenice|Venus|Venerio|Vasty|Varina|Vanina|Vani|Vallery|Valerin|Valería|Valentino|\
            Valdès|Ulysses|Ucleilyn|Ubaldina|Tulo|Tulita|Tulio|Tulasi|Tuco|Trizia|Trini|Trine|\
            Toya|Toto|Toti|Tomoyo|Tiziana|Tirsa|Tiny|Tina|Tilico|Tiky|Tifani|Tibisay|Tibaide|Thamara|Thaliana|\
            Thalia|Tersi|Tereza|Tere|Teofilo|Teodolinda|Telma|Tefi|Tedis|Tebylu|JuanPa|Jacb|Tannia|Taluz|Sylas|\
            Suzan|Susset|Susanne|Susanitha|Sujeimar|Steffano|Stefani|Sonilú|Soniberth|Simaduse", answq)
            respuestasinsignos = answq
            if signpoint:
                respuestasinsignos = re.sub(r"Zuzanne|Zunilda|Zulymar|Zully|Zoraida|Zinai|Zharon|Zelay|Zednanreh|\
                Zayra|Zayda|Zary|Zamy|Zahimis|Zael|Yuyu|Yuyi|Yuvely|Yusmary|Yurika|Yureivis|Yunke|Yulianis|\
                Yujuma|Yudith|Yudi|Yudely|Yovg|Yovanny|Yovani|Yosmeidis|Yoseph|Yosari|Yorvani|Yorlene|Yordan|\
                Yoojung|Yonnier|Yonier|Yomilys|Yoma|Yolys|Yolie|Yoliana|Yolan|Yoeimar|Yobaina|Yoav|Yoandy|\
                Yitsy|Yiseth|Yirs|Yiro|Yiris|Yiramile|Yiralmile|Yilibeth|Yhossue|Yetzabel|Yess|Yesmin|Yesly|\
                Yesika|Yesidd|Yesi|Yerigel|Yenimar|Yeniferth|Yenifer|Yendry|Yemaya|Yelesm|Yelangel|Yeini|\
                Yeimmy|Yeco|Yeanine|Yaz|Yayii|Yatzi|Yassin|Yasser|Yasid|Yaser|Yasenia|Yas|Yarol|Yárol|Yaqui|\
                Yanpier|Yanni|Yann|Yanky|Yanet|Yanessi|Yanela|Yan|Yamila|Yamil|Yaki|Yair|Yahoska|Yahir|Yadyss|\
                Yadi|Yaciel|Xuezhi|Xiomi|Xime|Xilena|Woody|Wiston|Wilma|Willie|Willi|Willem|Wili|Wilfried|Wilches\
                Wilchel|Wil|Wens|Wendolyne|Wendis|Weiner|Weimar|Wayne|Wayman|Wan|Wal|Waira|Vladi|Vivís|Viro|\
                Virguit|Virgilio|Virgelina|Vinscent|Vinny|Viko|Viki|Vielka|Vicencio|Vic|Vialy|Vhania|Veve|\
                Versys|Veriix|Verenice|Venus|Venerio|Vasty|Varina|Vanina|Vani|Vallery|Valerin|Valería|Valentino|\
                Valdès|Ulysses|Ucleilyn|Ubaldina|Tulo|Tulita|Tulio|Tulasi|Tuco|Trizia|Trini|Trine|\
                Toya|Toto|Toti|Tomoyo|Tiziana|Tirsa|Tiny|Tina|Tilico|Tiky|Tifani|Tibisay|Tibaide|Thamara|Thaliana|\
                Thalia|Tersi|Tereza|Tere|Teofilo|Teodolinda|Telma|Tefi|Tedis|Tebylu|JuanPa|Jacb|Tannia|Taluz|Sylas|\
                Suzan|Susset|Susanne|Susanitha|Sujeimar|Steffano|Stefani|Sonilú|Soniberth|Simaduse|Joyma", "_NOMBRE_", answq)
                
                ii+=1   
            
            myData.append({'questions':q, 'answers':respuestasinsignos,'links':links,\
                'first_process':row['first_process'],'second_process':row['second_process'],\
                'sentiment':row['sentiment'],'contact_form':row['contact_form'],'tag':tag,\
                'wordCantQues':row['wordCantQues'],'wordCantAnsw':row['wordCantAnsw']})
            writer.writerows(myData)
            myData.pop()         
            i+=1
                
                        
print("Tamaño real de la data: {}".format(i))
print("Tamaño real de la data escrita con limitaciones de palabras: {}".format(ii))
#print("Cantidad de data con la palabra a buscar: {}".format(countwordsrep))

print("ReWriting Complete")
#print(myData1)