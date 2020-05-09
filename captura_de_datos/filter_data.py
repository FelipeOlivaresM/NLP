from gensim.parsing.porter import PorterStemmer
import pandas as pd
import numpy as np
import sys, csv

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.


numero_muestras = 2500
random_estate = 8

output_path1 = "./twitter_data/datos_en_bruto/catched_tweets_originales.csv"
output_path_m1_en = "./twitter_data/datos_para_tageo_mourning/en_prefiltered_mourning.csv"
output_path_m1_es = "./twitter_data/datos_para_tageo_mourning/es_prefiltered_mourning.csv"
output_path_m2_en = "./twitter_data/datos_para_tageo_mourning/en_prefiltered_not_mourning.csv"
output_path_m2_es = "./twitter_data/datos_para_tageo_mourning/es_prefiltered_not_mourning.csv"

print("\nCargando data frame principal")
df = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')
df['mourning'] = np.nan

porter = PorterStemmer()

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

print("Escribiendo archivos complementarios")

df_template = pd.DataFrame(columns=df.columns)
df_template.to_csv(output_path_m1_en, index=False, encoding="utf-8")
df_template.to_csv(output_path_m1_es, index=False, encoding="utf-8")
df_template.to_csv(output_path_m2_en, index=False, encoding="utf-8")
df_template.to_csv(output_path_m2_es, index=False, encoding="utf-8")

del df_template

csv_m1_en = open(output_path_m1_en, 'a', encoding="utf-8")
csv_m1_es = open(output_path_m1_es, 'a', encoding="utf-8")
csv_m2_en = open(output_path_m2_en, 'a', encoding="utf-8")
csv_m2_es = open(output_path_m2_es, 'a', encoding="utf-8")

writer1 = csv.writer(csv_m1_en)
writer2 = csv.writer(csv_m1_es)
writer3 = csv.writer(csv_m2_en)
writer4 = csv.writer(csv_m2_es)

print("Iniciando proceso de filtrado")
for i, row in df.iterrows():

    sys.stdout.write("\rFiltrado completado al " + str(round(((i + 1) / (df.shape[0])) * 100, 2)) + "%")
    sys.stdout.flush()

    language = df.at[i, 'lang']
    text = porter.stem_sentence(str(df.at[i, 'text']).lower())
    languages_list = ['en', 'es']

    if any(word in text for word in tags_muerte):
        if type(language) is str and language in languages_list:
            df.at[i, 'mourning'] = 1
            if str(language) == 'en':
                writer1.writerow(df.iloc[i])
            elif str(language) == 'es':
                writer2.writerow(df.iloc[i])
    else:
        if type(language) is str and language in languages_list:
            if str(language) == 'en':
                writer3.writerow(df.iloc[i])
            elif str(language) == 'es':
                writer4.writerow(df.iloc[i])

csv_m1_en.close()
csv_m1_es.close()
csv_m2_en.close()
csv_m2_es.close()

print("\nOrdenando datos filtrados")

del df, writer1, writer2


def corregir_tamaño(df, tamaño_mestra):
    while df.shape[0] < tamaño_mestra:
        df = df.append(df)
    return df


df = pd.read_csv(output_path_m1_es, encoding='utf8', dtype=str, engine='python')
df = corregir_tamaño(df, numero_muestras)
df = df.sample(n=numero_muestras, random_state=random_estate)
df.sort_values('id')
df.to_csv(output_path_m1_es, index=False, encoding="utf-8")
del df

df = pd.read_csv(output_path_m1_en, encoding='utf8', dtype=str, engine='python')
df = corregir_tamaño(df, numero_muestras)
df = df.sample(n=numero_muestras, random_state=random_estate)
df.sort_values('id')
df.to_csv(output_path_m1_en, index=False, encoding="utf-8")
del df

df = pd.read_csv(output_path_m2_es, encoding='utf8', dtype=str, engine='python')
df = corregir_tamaño(df, numero_muestras)
df = df.sample(n=numero_muestras, random_state=random_estate)
df.sort_values('id')
df.to_csv(output_path_m2_es, index=False, encoding="utf-8")
del df

df = pd.read_csv(output_path_m2_en, encoding='utf8', dtype=str, engine='python')
df = corregir_tamaño(df, numero_muestras)
df = df.sample(n=numero_muestras, random_state=random_estate)
df.sort_values('id')
df.to_csv(output_path_m2_en, index=False, encoding="utf-8")
del df

print("Filtrado finalizado")
