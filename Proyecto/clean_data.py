import re
import pandas as pd

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.

<<<<<<< HEAD
output_path = "./twitter_data/datos_en_bruto/catched_tweets_8.csv"
=======
output_path = "./twitter_data/datos_en_bruto/catched_tweets_7.csv"
>>>>>>> 103b2d55e5b239339d64f16dfead47775024c238
df = pd.read_csv(output_path)
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

df.to_csv(output_path, index=False, encoding="utf-8")
print("\nDatos en los que se reparo la sintaxis: " + str(datos_reparados))
print("Datos limpios en el archivo: " + str(datos_en_el_archivo - datos_eliminados))
print("Datos eliminados: " + str(datos_eliminados) + "\n")
