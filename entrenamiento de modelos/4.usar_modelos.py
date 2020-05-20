import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# ---------------- Rutas de los datos para etiquetar.
datos_para_etiquetar = './dataset etiquetado modelos/catched_tweets_sample_20-05-2020.csv'
datos_etiquetados = './dataset etiquetado modelos/taged_tweets_sample_20-05-2020.csv'

# ---------------- Rutas de los modelos.
ruta_modelo_mourning_español = './modelos/MultinomialNB_Español_Mourning.sav'
ruta_modelo_mourning_ingles = './modelos/MultinomialNB_Ingles_Mourning.sav'
ruta_modelo_sentiment_español = './modelos/MultinomialNB_Español_Sentiment.sav'
ruta_modelo_sentiment_ingles = './modelos/MultinomialNB_Ingles_Sentiment.sav'

# ---------------- Cargar modelos.
modelo_mourning_español = pickle.load(open(ruta_modelo_mourning_español, 'rb'))
modelo_mourning_ingles = pickle.load(open(ruta_modelo_mourning_ingles, 'rb'))
modelo_sentiment_español = pickle.load(open(ruta_modelo_sentiment_español, 'rb'))
modelo_sentiment_ingles = pickle.load(open(ruta_modelo_sentiment_ingles, 'rb'))

# ---------------- Cargar datos.
df = pd.read_csv(datos_para_etiquetar, encoding='utf8', dtype=str, engine='python')
df = df.filter(['text', 'lang'])
df_es = df[df.lang == 'es']
df_en = df[df.lang == 'en']

# ---------------- Vectorizar datos.
count_vector = TfidfVectorizer()
es_data = count_vector.transform(df_es['text'])
en_data = count_vector.transform(df_en['text'])

# ---------------- Clasificar usando modelos.
mourning_predictions_es = modelo_mourning_español.predict(es_data)
mourning_predictions_en = modelo_mourning_ingles.predict(en_data)
sentiment_predictions_es = modelo_sentiment_español.predict(es_data)
sentiment_predictions_en = modelo_sentiment_ingles.predict(en_data)

# ---------------- Guardar datos tageados.
df.to_csv(datos_etiquetados, index=False, encoding="utf-8")
