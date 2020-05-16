import pandas as pd
import re, sys

print("\nCargando datos")
output_path = "./twitter data/datos en bruto/catched_tweets_full_data.csv"
df = pd.read_csv(output_path, encoding='utf8', dtype=str, engine='python')
datos_en_el_archivo = 0
datos_eliminados = 0
datos_reparados = 0

for i, row in df.iterrows():

    sys.stdout.write("\rLimpieza de datos completada al " + str(round(((i + 1) / (df.shape[0])) * 100, 2)) + "%")
    sys.stdout.flush()

    datos_en_el_archivo += 1
    texto_anterior = str(df.at[i, 'text'])
    texto_nuevo = (re.sub(' +', ' ', re.sub("http\S+", "", str(df.at[i, 'text']).replace("\n", " ")))).strip()

    if texto_anterior != texto_nuevo:
        df.at[i, 'text'] = texto_nuevo
        datos_reparados += 1

    if str(df.at[i, 'text']).endswith('…'):
        datos_eliminados += 1
        df = df.drop([i])

df.drop_duplicates(subset=['id', 'text'], inplace=True)
df.sort_values('id', inplace=True)
print("\nLimpieza finalizada")
print("\nReporte de resultados limpieza: ")
df.to_csv(output_path, index=False, encoding="utf-8")
datos_eliminados += (datos_en_el_archivo - int(df.shape[0]))
print("Datos en los que se reparo la sintaxis: " + str(datos_reparados))
print("Datos limpios en el archivo: " + str(datos_en_el_archivo - datos_eliminados))
print("Datos eliminados: " + str(datos_eliminados) + "\n")
