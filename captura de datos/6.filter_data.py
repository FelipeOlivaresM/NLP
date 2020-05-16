from gensim.utils import any2unicode as unicode
from nltk.stem import SnowballStemmer
import pandas as pd
import sys, csv, os
import unidecode

numero_muestras = 5100

output_path1 = "./twitter data/datos en bruto/catched_tweets_full_data.csv"
output_path_m1_en = "./twitter data/datos para tageo mourning/en_prefiltered_mourning.csv"
output_path_m1_es = "./twitter data/datos para tageo mourning/es_prefiltered_mourning.csv"
output_path_m2_en = "./twitter data/datos para tageo mourning/en_prefiltered_not_mourning.csv"
output_path_m2_es = "./twitter data/datos para tageo mourning/es_prefiltered_not_mourning.csv"

vector_rutas = [output_path_m1_en, output_path_m1_es, output_path_m2_en, output_path_m2_es]

print("\nCargando todos los datos y metadatos necesarios")
df = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')
df['mourning'] = 4

numero_muestras += 1

stemmer_en = SnowballStemmer('english')
stemmer_es = SnowballStemmer('spanish')

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

df_template = pd.DataFrame(columns=df.columns)

for i in range(len(vector_rutas)):
    sys.stdout.write(
        "\rRevision de archivos completada al " + str(round(((i + 1) / (len(vector_rutas))) * 100, 2)) + "%"
    )
    sys.stdout.flush()
    if not os.path.exists(vector_rutas[i]):
        df_template.to_csv(vector_rutas[i], index=False, encoding="utf-8")

print()

del df_template

csv_m1_en = open(output_path_m1_en, 'r', encoding="utf-8")
csv_m1_es = open(output_path_m1_es, 'r', encoding="utf-8")
csv_m2_en = open(output_path_m2_en, 'r', encoding="utf-8")
csv_m2_es = open(output_path_m2_es, 'r', encoding="utf-8")

ids_m1_en = [str(row[0]) for row in csv.reader(csv_m1_en)]
ids_m1_es = [str(row[0]) for row in csv.reader(csv_m1_es)]
ids_m2_en = [str(row[0]) for row in csv.reader(csv_m2_en)]
ids_m2_es = [str(row[0]) for row in csv.reader(csv_m2_es)]

csv_m1_en = open(output_path_m1_en, 'a', encoding="utf-8")
csv_m1_es = open(output_path_m1_es, 'a', encoding="utf-8")
csv_m2_en = open(output_path_m2_en, 'a', encoding="utf-8")
csv_m2_es = open(output_path_m2_es, 'a', encoding="utf-8")

writer1 = csv.writer(csv_m1_en)
writer2 = csv.writer(csv_m1_es)
writer3 = csv.writer(csv_m2_en)
writer4 = csv.writer(csv_m2_es)

for i, row in df.iterrows():

    sys.stdout.write("\rDatos en los data set de salida al " +
                     str(round(
                         ((len(ids_m2_es) + len(ids_m2_en) + len(ids_m1_es) + len(ids_m1_en)) /
                          ((numero_muestras * 4))) * 100, 2)
                     ) + "%" + " lectura del archivo completada al " +
                     str(round((i / df.shape[0]) * 100, 2)) + "%"
                     )

    sys.stdout.flush()

    text = df.at[i, 'text']
    id = str(df.at[i, 'id'])
    language = df.at[i, 'lang']
    languages_list = ['en', 'es']

    if len(ids_m2_es) + len(ids_m2_en) + len(ids_m1_es) + len(ids_m1_en) == ((numero_muestras * 4)): break

    if type(text) is str and language == 'es':
        text = stemmer_es.stem(unidecode.unidecode(unicode(text.lower(), "utf-8")))
    elif type(text) is str and language == 'en':
        text = stemmer_en.stem(unidecode.unidecode(unicode(text.lower(), "utf-8")))

    if type(text) is str and any(word in text for word in tags_muerte):
        if type(language) is str and language in languages_list:
            if str(language) == 'en' and id not in ids_m1_en and len(ids_m1_en) < numero_muestras:
                writer1.writerow(df.iloc[i])
                ids_m1_en.append(id)
            elif str(language) == 'es' and id not in ids_m1_es and len(ids_m1_es) < numero_muestras:
                writer2.writerow(df.iloc[i])
                ids_m1_es.append(id)
    else:
        if type(language) is str and language in languages_list:
            if str(language) == 'en' and id not in ids_m2_en and len(ids_m2_en) < numero_muestras:
                writer3.writerow(df.iloc[i])
                ids_m2_en.append(id)
            elif str(language) == 'es' and id not in ids_m2_es and len(ids_m2_es) < numero_muestras:
                writer4.writerow(df.iloc[i])
                ids_m2_es.append(id)

csv_m1_en.close()
csv_m1_es.close()
csv_m2_en.close()
csv_m2_es.close()

del df, writer1, writer2, writer3, writer4
print()

for i in range(len(vector_rutas)):
    sys.stdout.write(
        "\rPreparacion de muestras completada al " + str(round(((i + 1) / (len(vector_rutas))) * 100, 2)) + "%"
    )
    sys.stdout.flush()
    df = pd.read_csv(vector_rutas[i], encoding='utf8', dtype=str, engine='python')
    df.drop_duplicates(subset=['id', 'text'], inplace=True)
    df.sort_values(['mourning', 'id'], inplace=True, ascending=True)
    df.to_csv(vector_rutas[i], index=False, encoding="utf-8")
    del df

print("\n")

numero_muestras -= 1

for i in vector_rutas:
    file = open(i)
    rows_count = sum(1 for row in csv.reader(file)) - 1
    file.close()
    print("Datos en " + str(i.split("/")[-1]) + " : " + str(rows_count) + " | " + str(numero_muestras) + " (" + str(
        round((rows_count / numero_muestras), 2) * 100) + "%)")
