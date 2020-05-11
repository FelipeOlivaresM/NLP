from gensim.parsing.porter import PorterStemmer
import pandas as pd
import sys, csv, os

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.


numero_muestras = 2500

output_path1 = "./twitter_data/datos_en_bruto/catched_tweets_full_data.csv"
output_path_m1_en = "./twitter_data/datos_para_tageo_mourning/en_prefiltered_mourning.csv"
output_path_m1_es = "./twitter_data/datos_para_tageo_mourning/es_prefiltered_mourning.csv"
output_path_m2_en = "./twitter_data/datos_para_tageo_mourning/en_prefiltered_not_mourning.csv"
output_path_m2_es = "./twitter_data/datos_para_tageo_mourning/es_prefiltered_not_mourning.csv"

vector_rutas = [output_path_m1_en, output_path_m1_es, output_path_m2_en, output_path_m2_es]

print("\nCargando todos los datos y metadatos necesarios")
df = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')
df['mourning'] = 4

porter = PorterStemmer()
numero_muestras += 1

tags_muerte = [
    'mourning', 'rest in peace', 'glory of god', 'cry for the departure', 'luto', 'descansa en paz',
    'gloria de dios', 'lloran por la pertida', 'llorar por la partida', 'god be with you', 'que dios esté contigo',
    'sorry for your absence', 'lamento tu ausencia', 'no te preocupes por las lágrimas que derramas en su nombre',
    'lágrimas de dolor', 'tears of pain', 'rezo porque estés en el reino de dios',
    'i pray for you to be in the kingdom of god',
    'nos veremos de nuevo en el reino de dios', 'en el reino de dios',
    'i will see you again in the kingdom of god', 'the kingdom of god',
    'santa gloria', 'holy glory', 'en paz descanse', 'en paz descansa',
    'lamentamos la muerte', 'lamento la muerte', 'regret death',
    'mourned the loss', 'lloró la pérdida', 'lloramos la pérdida', 'lloro la perdida', 'lloramos la perdida',
    'lamentamos la pérdida', 'lamento la pérdida', 'lamentamos la perdida', 'lamento la perdida',
    'lamentamos su muerte', 'lamento su muerte', 'regret her death', 'regret his death',
    'mourned his loss', 'mourned her loss', 'lloró su pérdida', 'lloramos su pérdida', 'lloro su perdida',
    'lloramos la perdida',
    'lamentamos su pérdida', 'lamento su pérdida', 'lamentamos su perdida', 'lamento su perdida',
]

tags_muerte = list(porter.stem_documents(tags_muerte))
tags_muerte.append(' rip ')
tags_muerte.append(' qdep ')
tags_muerte.append(' r.i.p ')
tags_muerte.append(' q.d.e.p ')

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

    id = str(df.at[i, 'id'])
    language = df.at[i, 'lang']
    text = porter.stem_sentence(str(df.at[i, 'text']).lower())
    languages_list = ['en', 'es']

    if len(ids_m2_es) + len(ids_m2_en) + len(ids_m1_es) + len(ids_m1_en) == ((numero_muestras * 4)): break

    if any(word in text for word in tags_muerte):
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
