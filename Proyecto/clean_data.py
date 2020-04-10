import re
import pandas as pd

output_path = "./twitter_data/catched_tweets_1.csv"
df = pd.read_csv(output_path)
datos_eliminados = 0

for i, row in df.iterrows():
    df.at[i, 'text'] = re.sub(' +', ' ', re.sub("http\S+", "", str(row['text']).replace("\n", " "))).strip()
    if df.at[i, 'text'].endswith('…'):
        datos_eliminados += 1
        df = df.drop([i])

df.to_csv(output_path, index=False, encoding="utf-8")
print("\nDatos eliminados: " + str(datos_eliminados) + "\n")
