import pandas as pd
from colour import Color
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import collections, datetime, pickle, sys, os

ruta_resultados = './dataset etiquetado modelos/resultados/catched_tweets_full_data_taged.csv'
print("")

if os.path.exists(ruta_resultados) == False:
    # ---------------- Rutas de los datos, modelos y vocabularios.
    ruta_datos = './dataset etiquetado modelos/por etiquetar/catched_tweets_full_data.csv'

    ruta_modelo_mour_en = './modelos/DecisionTreeClassifier_Mourning_en.sav'
    ruta_modelo_mour_es = './modelos/DecisionTreeClassifier_Mourning_es.sav'
    ruta_modelo_sent_en = './modelos/DecisionTreeClassifier_Sentiment_en.sav'
    ruta_modelo_sent_es = './modelos/DecisionTreeClassifier_Sentiment_es.sav'

    ruta_voc_mour_en = './vocabularios/vocabulario_mourning_en.pkl'
    ruta_voc_mour_es = './vocabularios/vocabulario_mourning_es.pkl'
    ruta_voc_sent_en = './vocabularios/vocabulario_sentiment_en.pkl'
    ruta_voc_sent_es = './vocabularios/vocabulario_sentiment_es.pkl'

    # ---------------- Carga de los datos, modelos y vocabularios.
    df = pd.read_csv(ruta_datos, encoding='utf8', dtype=str, engine='python')
    df_es = df[df.lang == 'es']
    df_en = df[df.lang == 'en']
    del df

    modelo_mour_en = pickle.load(open(ruta_modelo_mour_en, 'rb'))
    modelo_mour_es = pickle.load(open(ruta_modelo_mour_es, 'rb'))
    modelo_sent_en = pickle.load(open(ruta_modelo_sent_en, 'rb'))
    modelo_sent_es = pickle.load(open(ruta_modelo_sent_es, 'rb'))

    voc_mour_en = pickle.load(open(ruta_voc_mour_en, "rb"))
    voc_mour_es = pickle.load(open(ruta_voc_mour_es, "rb"))
    voc_sent_en = pickle.load(open(ruta_voc_sent_en, "rb"))
    voc_sent_es = pickle.load(open(ruta_voc_sent_es, "rb"))

    # ---------------- Vectorizacion de datos.
    print("Vectorizando datos")
    vectorizer1 = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=voc_mour_en)
    vectorizer2 = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=voc_mour_es)
    vectorizer3 = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=voc_sent_en)
    vectorizer4 = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=voc_sent_es)

    data_mour_es = vectorizer2.fit_transform(df_es['text'])
    data_sent_es = vectorizer4.fit_transform(df_es['text'])
    data_mour_en = vectorizer1.fit_transform(df_en['text'])
    data_sent_en = vectorizer3.fit_transform(df_en['text'])

    # ---------------- Clasificacion de datos con los modelos.
    print("Clasificando datos con modelos")
    df_es['mourning'] = modelo_mour_es.predict(data_mour_es)
    df_en['mourning'] = modelo_mour_en.predict(data_mour_en)
    df_es['sentiment'] = modelo_sent_es.predict(data_sent_es)
    df_en['sentiment'] = modelo_sent_en.predict(data_sent_en)

    # ---------------- Union y guardado del df.
    df = pd.concat([df_es, df_en])
    df.to_csv(ruta_resultados, index=False, encoding="utf-8")
    del df

print("Cargando datos")
df = pd.read_csv(ruta_resultados, encoding='utf8', dtype=str, engine='python')

global_count = 0
sent_count = dict()
mour_count = dict()
dates_count_mour_0 = dict()
dates_count_mour_1 = dict()
dates_count_sent_0 = dict()
dates_count_sent_1 = dict()
dates_count_sent_2 = dict()

for i, row in df.iterrows():
    sys.stdout.write("\rAnalisis de datos completado al " + str(round(((i + 1) / (df.shape[0])) * 100, 2)) + "%")
    sys.stdout.flush()

    global_count += 1

    date_str = df.at[i, 'created_at']
    sentiment = df.at[i, 'sentiment']
    mourning = df.at[i, 'mourning']
    language = df.at[i, 'lang']

    if type(date_str) is str and date_str != '0':
        date_time_obj = datetime.datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')
        date = date_time_obj.date().strftime("%m-%d")

        if date not in dates_count_sent_0:
            dates_count_sent_0[date] = 0
        elif date in dates_count_sent_0 and int(sentiment) == 0:
            dates_count_sent_0[date] += 1

        if date not in dates_count_sent_1:
            dates_count_sent_1[date] = 0
        elif date in dates_count_sent_1 and int(sentiment) == 1:
            dates_count_sent_1[date] += 1

        if date not in dates_count_sent_2:
            dates_count_sent_2[date] = 0
        elif date in dates_count_sent_2 and int(sentiment) == 2:
            dates_count_sent_2[date] += 1

        if date not in dates_count_mour_0:
            dates_count_mour_0[date] = 0
        elif date in dates_count_mour_0 and int(mourning) == 0:
            dates_count_mour_0[date] += 1

        if date not in dates_count_mour_1:
            dates_count_mour_1[date] = 0
        elif date in dates_count_mour_0 and int(mourning) == 1:
            dates_count_mour_1[date] += 1

    key1 = language + '_' + mourning
    if key1 in mour_count:
        mour_count[key1] += 1
    elif key1 not in mour_count:
        mour_count[key1] = 1

    key2 = language + '_' + sentiment
    if key2 in sent_count:
        sent_count[key2] += 1
    elif key2 not in sent_count:
        sent_count[key2] = 1

del df

dates_sent_col_0 = collections.OrderedDict(sorted(dates_count_sent_0.items()))
dates_sent_col_1 = collections.OrderedDict(sorted(dates_count_sent_1.items()))
dates_sent_col_2 = collections.OrderedDict(sorted(dates_count_sent_2.items()))
vector_fechas_00 = [str(element[0]) for element in dates_sent_col_0.items()]
vector_fechas_01 = [str(element[0]) for element in dates_sent_col_1.items()]
vector_fechas_02 = [str(element[0]) for element in dates_sent_col_2.items()]
vector_conteo_00 = [int(element[-1]) for element in dates_sent_col_0.items()]
vector_conteo_01 = [int(element[-1]) for element in dates_sent_col_1.items()]
vector_conteo_02 = [int(element[-1]) for element in dates_sent_col_2.items()]

dates_mour_col_0 = collections.OrderedDict(sorted(dates_count_mour_0.items()))
dates_mour_col_1 = collections.OrderedDict(sorted(dates_count_mour_1.items()))
vector_fechas_0 = [str(element[0]) for element in dates_mour_col_0.items()]
vector_fechas_1 = [str(element[0]) for element in dates_mour_col_1.items()]
vector_conteo_0 = [int(element[-1]) for element in dates_mour_col_0.items()]
vector_conteo_1 = [int(element[-1]) for element in dates_mour_col_1.items()]

mour_col = collections.OrderedDict(sorted(mour_count.items()))
vector_tags_mour = [str(element[0]) for element in mour_col.items()]
vector_conteo_mour = [int(element[-1]) for element in mour_col.items()]

sent_col = collections.OrderedDict(sorted(sent_count.items()))
vector_tags_sent = [str(element[0]) for element in sent_col.items()]
vector_conteo_sent = [int(element[-1]) for element in sent_col.items()]


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{v:d} ({p:.2f}%)'.format(p=pct, v=val)

    return my_autopct


print("\nGenerando graficas")

red = Color("orangered")
colors = list(red.range_to(Color("orange"), len(vector_conteo_mour)))
colors = [color.rgb for color in colors]

plt.pie(vector_conteo_mour, labels=vector_tags_mour, shadow=True,
        autopct=make_autopct(vector_conteo_mour), colors=colors)
plt.title('Conteo de mourning usando ' + str(global_count) + ' Tweets')
plt.gcf().set_size_inches(10, 8)
plt.savefig('./graficas datos/analisis_mourning.png')
plt.clf()

red = Color("orangered")
colors = list(red.range_to(Color("orange"), len(vector_conteo_sent)))
colors = [color.rgb for color in colors]

plt.pie(vector_conteo_sent, labels=vector_tags_sent, shadow=True,
        autopct=make_autopct(vector_conteo_sent), colors=colors)
plt.title('Conteo de sentimientos usando ' + str(global_count) + ' Tweets')
plt.gcf().set_size_inches(10, 8)
plt.savefig('./graficas datos/analisis_sentiments.png')
plt.clf()

width = 0.35
plt.bar(vector_fechas_0, vector_conteo_0, width, label='No Mourning')
plt.bar(vector_fechas_1, vector_conteo_1, width, label='Mourning')
plt.title('Conteo de luto usando ' + str(global_count) + ' Tweets por dias')
plt.ylabel('Conteo de tweets')
plt.xticks(rotation='vertical')
plt.legend()
plt.gcf().set_size_inches(16, 10)
plt.savefig('./graficas datos/analisis_mourning_tiempo.png')
plt.clf()

width = 0.35
plt.bar(vector_fechas_00, vector_conteo_00, width, label='Positivo')
plt.bar(vector_fechas_01, vector_conteo_01, width, label='Negativo')
plt.bar(vector_fechas_02, vector_conteo_02, width, label='Neutral')
plt.title('Conteo de sentimientos usando ' + str(global_count) + ' Tweets por dias')
plt.ylabel('Conteo de tweets')
plt.xticks(rotation='vertical')
plt.legend()
plt.gcf().set_size_inches(16, 10)
plt.savefig('./graficas datos/analisis_sentiments_tiempo.png')
plt.clf()

print("Proceso finalizado, las garficas fueron guardads en la carpeta graficas_datos")
