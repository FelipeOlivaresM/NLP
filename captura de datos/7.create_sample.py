import datetime
import pandas as pd
from sklearn.utils import resample

now = datetime.date.today()
now = now.strftime('%d-%m-%Y')
output_path1 = "./twitter data/datos en bruto/catched_tweets_full_data.csv"
output_path2 = "./twitter data/datos en bruto/muestras/catched_tweets_sample_" + str(now) + ".csv"

sample_size = 2500
print("\nCargando datos")
df = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')
print("Muestreando datos a partes iguales")
df_es = resample(df[df.lang == 'es'], replace=False, n_samples=sample_size, random_state=1)
df_en = resample(df[df.lang == 'en'], replace=False, n_samples=sample_size, random_state=1)
df = pd.concat([df_en, df_es])

print("Proceso terminado")
df.to_csv(output_path2, index=False, encoding="utf-8")
