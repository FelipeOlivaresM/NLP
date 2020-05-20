import unidecode
import pandas as pd
from colour import Color
import matplotlib.pyplot as plt
from nltk.stem import SnowballStemmer
import os, sys, math, datetime, collections
from gensim.utils import any2unicode as unicode

usar_muestra = 0

stemmer_en = SnowballStemmer('english')
stemmer_es = SnowballStemmer('spanish')

output_path1 = "./twitter data/datos en bruto/catched_tweets_full_data.csv"
output_path2 = "./twitter data/datos en bruto/catched_tweets_sample.csv"

tags_español = [
    'no te preocupes por las lágrimas que derramas en su nombre',
    'nos veremos de nuevo en el reino de dios',
    'rezo porque estés en el reino de dios',
    'paz a su alma',
    'lloran por la pertida',
    'llorar por la partida',
    'que dios esté contigo',
    'lamento tu ausencia',
    'lágrimas de dolor',
    'en el reino de dios',
    'en paz descanse',
    'en paz descansa',
    'lamentamos la muerte',
    'lamento la muerte',
    'lloró la pérdida',
    'lloramos la pérdida',
    'lloro la perdida',
    'lloramos la perdida',
    'lamentamos la pérdida',
    'lamento la pérdida',
    'lamentamos la perdida',
    'lamento la perdida',
    'lamentamos su muerte',
    'lamento su muerte',
    'lloró su pérdida',
    'lloramos su pérdida',
    'lloro su perdida',
    'lloramos la perdida',
    'lamentamos su pérdida',
    'lamento su pérdida',
    'lamentamos su perdida',
    'lamento su perdida',
    'descansa en paz',
    'gloria de dios',
    'santa gloria',
    ' luto ',
    ' dolor ',
    ' aflicción ',
    ' pena ',
    ' pesar '
]

tags_español = [stemmer_es.stem(unidecode.unidecode(unicode(w, "utf-8"))).lower() for w in (tags_español)]

tags_ingles = [
    'We must never forget every one of the heroes',
    'i pray for you to be in the kingdom of god',
    'i will see you again in the kingdom of god',
    'you will live on forever',
    'sorry for your absence',
    'cry for the departure',
    'the kingdom of god',
    'mourned the loss',
    'regret her death',
    'regret his death',
    'mourned his loss',
    'mourned her loss',
    'god be with you',
    'rest in peace',
    'tears of pain',
    'glory of god',
    'regret death',
    'im sorry',
    'i care about you',
    'she will be dearly missed',
    'he will be dearly missed',
    'she is in my thoughts and prayers',
    'he is in my thoughts and prayers',
    'you and your family are in my thoughts and prayers',
    'you are important to me',
    'my condolences',
    'i hope you find some peace today',
    'i am saddened to hear about',
    'holy glory',
    ' mourning ',
    ' grieving ',
    ' condolences ',
    'she is in a better place',
    'he is in a better place',
    'you have an angel in heaven',
    'she is no longer suffering',
    'he is no longer suffering',
    'she is with god now',
    'he is with god now',
    'they are with god now',
    ' lamentation ',
    ' lament ',
    ' keening ',
    ' wailing ',
    ' weeping ',
    ' sorrow '
]

tags_ingles = [stemmer_en.stem(unidecode.unidecode(unicode(w, "utf-8"))).lower() for w in (tags_ingles)]

tags_abreviaciones = [
    ' #RIP ', ' #QDEP ', ' #restinpeace ', ' #descanzaenpas ', ' #restinpeace ', ' #luto ',
    ' q.d.e.p ', ' r.i.p ', ' qdep ', ' rip ', ' #Luto ', ' #LUTO ', ' #duelo ', ' #Duelo ',
    ' #DUELO ', ' #lutonacional '
]

emojis = []

tags_abreviaciones1 = [stemmer_es.stem(unidecode.unidecode(unicode(w, "utf-8"))).lower() for w in (tags_abreviaciones)]
tags_abreviaciones2 = [stemmer_en.stem(unidecode.unidecode(unicode(w, "utf-8"))).lower() for w in (tags_abreviaciones)]

tags_muerte = set(tags_español + tags_ingles + tags_abreviaciones1 + tags_abreviaciones2 + emojis)

if usar_muestra == 1:
    if os.path.exists(output_path2) == True:
        print("\nCargando muestra de datos")
        df = pd.read_csv(output_path2, encoding='utf8', dtype=str, engine='python')
    elif os.path.exists(output_path2) == False:
        print("\nCreando muestra de datos")
        df = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python').sample(n=80000, random_state=8)
        df.to_csv(output_path2, index=False, encoding="utf-8")
        del df
        df = pd.read_csv(output_path2, encoding='utf8', dtype=str, engine='python')
elif usar_muestra == 0:
    print("\nCargando datos")
    df = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')

global_count = 0
matched_mourning_tweets = 0
country_count = dict()
tweets_per_day = dict()
languages_count = dict()
languages_count_mourning = dict()
mourning_matches_pre_count = dict()

cifras_significativas = 8

for i, row in df.iterrows():

    sys.stdout.write("\rAnalisis de datos completado al " + str(round(((i + 1) / (df.shape[0])) * 100, 2)) + "%")
    sys.stdout.flush()

    global_count += 1
    text = df.at[i, 'text']
    country = df.at[i, 'country']
    date_str = df.at[i, 'created_at']
    language = df.at[i, 'lang']

    if type(text) is str and language == 'es':
        text = stemmer_es.stem(unidecode.unidecode(unicode(text.lower(), "utf-8")))
    elif type(text) is str and language == 'en':
        text = stemmer_en.stem(unidecode.unidecode(unicode(text.lower(), "utf-8")))

    languages_list = ['en', 'es']
    if type(language) is str and language in languages_list:
        if language in languages_count:
            languages_count[language] += 1
        elif language not in languages_count:
            languages_count[language] = 1
    elif type(language) is not str or language not in languages_list:
        language = 'Desconocido'
        if language in languages_count:
            languages_count[language] += 1
        elif language not in languages_count:
            languages_count[language] = 1

    if type(text) is str and any(word in text for word in tags_muerte):
        key = 'Tweets con match'
        matched_mourning_tweets += 1
        if key in mourning_matches_pre_count:
            mourning_matches_pre_count[key] += 1
        elif key not in mourning_matches_pre_count:
            mourning_matches_pre_count[key] = 1
        if type(language) is str and language in languages_list:
            if language in languages_count_mourning:
                languages_count_mourning[language] += 1
            elif language not in languages_count_mourning:
                languages_count_mourning[language] = 1
        elif type(language) is not str or language not in languages_list:
            key = "Desconocido"
            if language in languages_count_mourning:
                languages_count_mourning[key] += 1
            elif language not in languages_count_mourning:
                languages_count_mourning[key] = 1
    else:
        key = 'Tweets sin match'
        if key in mourning_matches_pre_count:
            mourning_matches_pre_count[key] += 1
        elif key not in mourning_matches_pre_count:
            mourning_matches_pre_count[key] = 1

    if type(date_str) is str and date_str != '0':
        date_time_obj = datetime.datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')
        date = date_time_obj.date().strftime("%m-%d")
        if date in tweets_per_day:
            tweets_per_day[date] += 1
        elif date not in tweets_per_day:
            tweets_per_day[date] = 1
    elif type(date_str) is not str or date_str == '0':
        key = 'Desc'
        if key in tweets_per_day:
            tweets_per_day[key] += 1
        elif key not in tweets_per_day:
            tweets_per_day[key] = 1

    if type(country) is str:
        key = 'Pais conocido'
        if key in country_count:
            country_count[key] += 1
        elif key not in country_count:
            country_count[key] = 1
    elif type(country) is not str and math.isnan(country) == True:
        key = 'Desconocido'
        if key in country_count:
            country_count[key] += 1
        elif key not in country_count:
            country_count[key] = 1

print("\nCargando datos a vectores")

mourning_matches_pre_count_col = collections.OrderedDict(sorted(mourning_matches_pre_count.items()))
vector_etiquetas_m = [str(element[0]) for element in mourning_matches_pre_count_col.items()]
vector_conteo_m = [int(element[-1]) for element in mourning_matches_pre_count_col.items()]

lang_col = collections.OrderedDict(sorted(languages_count.items()))
vector_idiomas_global = [str(element[0]) for element in lang_col.items()]
vector_conteo_idiomas_global = [int(element[-1]) for element in lang_col.items()]

mourning_matches_pre_count_lang_col = collections.OrderedDict(sorted(languages_count_mourning.items()))
vector_idiomas = [str(element[0]) for element in mourning_matches_pre_count_lang_col.items()]
vector_conteo_idiomas = [int(element[-1]) for element in mourning_matches_pre_count_lang_col.items()]

country_count_col = collections.OrderedDict(sorted(country_count.items()))
vector_etiquetas = [str(element[0]) for element in country_count.items()]
vector_conteo = [int(element[-1]) for element in country_count.items()]

tweets_per_day_col = collections.OrderedDict(sorted(tweets_per_day.items()))
vector_fechas = [str(element[0]) for element in tweets_per_day_col.items()]
vector_tweets = [int(element[-1]) for element in tweets_per_day_col.items()]

vector_tweets2 = [sum(vector_tweets[:i]) for i in range(len(vector_tweets))]

del country_count, lang_col, languages_count, country_count_col, tweets_per_day, tweets_per_day_col, mourning_matches_pre_count, mourning_matches_pre_count_col, languages_count_mourning, mourning_matches_pre_count_lang_col


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{v:d} ({p:.2f}%)'.format(p=pct, v=val)

    return my_autopct


print("Generando graficas")

red = Color("orangered")
colors = list(red.range_to(Color("orange"), len(vector_conteo_idiomas_global)))
colors = [color.rgb for color in colors]

plt.pie(vector_conteo_idiomas_global, labels=vector_idiomas_global, shadow=True,
        autopct=make_autopct(vector_conteo_idiomas_global), colors=colors)
plt.title('Numero de datos en total: ' + str(global_count))
plt.gcf().set_size_inches(14, 8)
plt.savefig('./graficas datos/' + str(usar_muestra) + '_analisis_idiomas.png')
plt.clf()

del vector_conteo_idiomas_global, vector_idiomas_global

red = Color("orangered")
colors = list(red.range_to(Color("orange"), len(vector_conteo_m)))
colors = [color.rgb for color in colors]

plt.pie(vector_conteo_m, labels=vector_etiquetas_m, shadow=True, autopct=make_autopct(vector_conteo_m), colors=colors)
plt.title('Numero de datos usados para realizar el preconteo: ' + str(global_count))
plt.gcf().set_size_inches(14, 8)
plt.savefig('./graficas datos/' + str(usar_muestra) + '_analisis_preconteo_mourning.png')
plt.clf()

del vector_etiquetas_m, vector_conteo_m

red = Color("orangered")
colors = list(red.range_to(Color("orange"), len(vector_conteo_idiomas)))
colors = [color.rgb for color in colors]

plt.pie(vector_conteo_idiomas, labels=vector_idiomas, shadow=True, autopct=make_autopct(vector_conteo_idiomas),
        colors=colors)
plt.title('Numero de datos con cincidencia en el preconteo: ' + str(matched_mourning_tweets))
plt.gcf().set_size_inches(14, 8)
plt.savefig('./graficas datos/' + str(usar_muestra) + '_analisis_idiomas_preconteo_mourning.png')
plt.clf()

del vector_idiomas, vector_conteo_idiomas

red = Color("orangered")
colors = list(red.range_to(Color("orange"), len(vector_conteo)))
colors = [color.rgb for color in colors]

plt.pie(vector_conteo, labels=vector_etiquetas, shadow=True, autopct=make_autopct(vector_conteo), colors=colors)
plt.title('Numero de datos en total: ' + str(global_count))
plt.gcf().set_size_inches(14, 8)
plt.savefig('./graficas datos/' + str(usar_muestra) + '_analisis_paises.png')
plt.clf()

del vector_conteo, vector_etiquetas

plt.plot(vector_fechas, vector_tweets, 'bo-', linewidth=1.4, color='red', label='Tweets por dia')
plt.title('Numero de datos en total: ' + str(global_count))
plt.xticks(rotation='vertical')
plt.ylabel('Numero de tweets capturados')
plt.legend()
plt.gcf().set_size_inches(16, 10)
plt.savefig('./graficas datos/' + str(usar_muestra) + '_analisis_fechas_dia_a_dia.png')
plt.clf()

del vector_tweets

plt.plot(vector_fechas, vector_tweets2, 'bo-', linewidth=1.4, color='red', label='Tweets por dia')
plt.title('Numero de datos en total: ' + str(global_count))
plt.xticks(rotation='vertical')
plt.ylabel('Numero de tweets capturados')
plt.legend()
plt.gcf().set_size_inches(16, 10)
plt.savefig('./graficas datos/' + str(usar_muestra) + '_analisis_fechas_acomulativo.png')
plt.clf()

del vector_fechas, vector_tweets2

print("Proceso finalizado, las garficas fueron guardads en la carpeta graficas_datos")
