import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# ---------------- Rutas de los datos para etiquetar.
datos_para_etiquetar = './dataset etiquetado modelos/21-05-2020_catched_tweets_sample.csv'
datos_etiquetados = './dataset etiquetado modelos/21-05-2020_taged_tweets_sample.csv'

# ---------------- Rutas de los modelos.
ruta_modelo_mourning = './modelos/DecisionTreeClassifier_Mourning.sav'
ruta_modelo_sentiment = './modelos/DecisionTreeClassifier_Sentiment.sav'

# ---------------- Cargar modelos.
modelo_mourning = pickle.load(open(ruta_modelo_mourning, 'rb'))
modelo_sentiment = pickle.load(open(ruta_modelo_sentiment, 'rb'))

# ---------------- Cargar datos.
df = pd.read_csv(datos_para_etiquetar, encoding='utf8', dtype=str, engine='python')
df = df.filter(['text', 'lang'])

# ---------------- Vectorizar datos cargando vocabularios.
vocabulary_m = pickle.load(open("./vocabularios/vocabulario_mourning.pkl", "rb"))
vocabulary_s = pickle.load(open("./vocabularios/vocabulario_sentiment.pkl", "rb"))
vectorizer_m = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=vocabulary_m)
vectorizer_s = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=vocabulary_s)
m_data = vectorizer_m.fit_transform(df['text'])
s_data = vectorizer_s.fit_transform(df['text'])

# ---------------- Clasificar usando modelos.
mourning_predictions = modelo_mourning.predict(m_data)
sentiment_predictions = modelo_sentiment.predict(s_data)

# ---------------- Agregar predicciones a los datos.
df['mourning'] = mourning_predictions
df['sentiment'] = sentiment_predictions

# ---------------- Resultados de usar el modelo para clasificar datos.
print("\nResultados de mourning en el dataset:\n")
print(df['mourning'].value_counts())
print("\nResultados de sentiment en el dataset:\n")
print(df['sentiment'].value_counts())

# ---------------- Guardar datos tageados.
df.to_csv(datos_etiquetados, index=False, encoding="utf-8")
