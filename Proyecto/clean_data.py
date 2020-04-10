import re
import pandas as pd

output_path = "./twitter_data/catched_tweets_1.csv"
df = pd.read_csv(output_path)
datos_en_el_archivo = 0
datos_eliminados = 0
datos_reparados = 0

print("Datos eliminados")
for i, row in df.iterrows():
    texto_anterior = df.at[i, 'text']
    texto_nuevo = (re.sub(' +', ' ', re.sub("http\S+", "", str(row['text']).replace("\n", " ")))).strip()
    df.at[i, 'text'] = texto_nuevo
    datos_en_el_archivo += 1
    if texto_anterior != texto_nuevo:
        datos_reparados += 1
    if df.at[i, 'text'].endswith('…'):
        datos_eliminados += 1
        print(df.at[i, 'id'], df.at[i, 'text'])
        df = df.drop([i])

df.to_csv(output_path, index=False, encoding="utf-8")
print("\nDatos en los que se reparo la sintaxis: " + str(datos_reparados))
print("Datos limpios en el archivo: " + str(datos_en_el_archivo - datos_eliminados))
print("Datos eliminados: " + str(datos_eliminados) + "\n")
