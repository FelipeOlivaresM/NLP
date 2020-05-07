import re
import pandas as pd

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.


output_path = "./twitter_data/datos_en_bruto/catched_tweets_originales.csv"
df = pd.read_csv(output_path, encoding='utf8', dtype=str, engine='python')
datos_en_el_archivo = 0
datos_eliminados = 0
datos_reparados = 0

print("\nDatos eliminados: ")
for i, row in df.iterrows():
    datos_en_el_archivo += 1
    texto_anterior = str(df.at[i, 'text'])
    texto_nuevo = (re.sub(' +', ' ', re.sub("http\S+", "", str(df.at[i, 'text']).replace("\n", " ")))).strip()
    if texto_anterior != texto_nuevo:
        df.at[i, 'text'] = texto_nuevo
        datos_reparados += 1
    if str(df.at[i, 'text']).endswith('…'):
        datos_eliminados += 1
        print(df.at[i, 'id'], ' - ', df.at[i, 'text'])
        df = df.drop([i])

df.drop_duplicates(subset=['id', 'text'], inplace=True)
df.sort_values('id')
df.to_csv(output_path, index=False, encoding="utf-8")
datos_eliminados += (datos_en_el_archivo - int(df.shape[0]))
print("\nDatos en los que se reparo la sintaxis: " + str(datos_reparados))
print("Datos limpios en el archivo: " + str(datos_en_el_archivo - datos_eliminados))
print("Datos eliminados: " + str(datos_eliminados) + "\n")
