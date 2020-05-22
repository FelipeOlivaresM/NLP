import pickle, sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# ---------------- Rutas de los datos para etiquetar.
datos_para_etiquetar = './dataset etiquetado modelos/tweets_sample.csv'
datos_etiquetados = './dataset etiquetado modelos/taged_tweets_sample.csv'

# ---------------- Rutas de los modelos.
ruta_modelo_mourning = './modelos/DecisionTreeClassifier_Mourning.sav'
ruta_modelo_sentiment = './modelos/DecisionTreeClassifier_Sentiment.sav'

# ---------------- Cargar modelos.
print("\nCargando modelos")
modelo_mourning = pickle.load(open(ruta_modelo_mourning, 'rb'))
modelo_sentiment = pickle.load(open(ruta_modelo_sentiment, 'rb'))

# ---------------- Cargar datos.
print("Cargando datos")
df = pd.read_csv(datos_para_etiquetar, encoding='utf8', dtype=str, engine='python')
df = df.filter(['text', 'lang'])

# ---------------- Vectorizar datos cargando vocabularios.
print("Vectorizando datos")
vocabulary_m = pickle.load(open("./vocabularios/vocabulario_mourning.pkl", "rb"))
vocabulary_s = pickle.load(open("./vocabularios/vocabulario_sentiment.pkl", "rb"))
vectorizer_m = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=vocabulary_m)
vectorizer_s = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=vocabulary_s)
m_data = vectorizer_m.fit_transform(df['text'])
s_data = vectorizer_s.fit_transform(df['text'])

# ---------------- Clasificar usando modelos.
print("Clasificando datos con modelos")
mourning_predictions = modelo_mourning.predict(m_data)
sentiment_predictions = modelo_sentiment.predict(s_data)

# ---------------- Agregar predicciones a los datos.
print("Agregando datos de predicciones al dataset de salida")
df['mourning'] = mourning_predictions
df['sentiment'] = sentiment_predictions

# ---------------- Contar df de salida.
df['sello'] = ""
df.reset_index(drop=True, inplace=True)

for i, row in df.iterrows():
    sys.stdout.write(
        "\rCreando sellos " +
        str(round(((i + 1) / (df.shape[0])) * 100, 2))
        + "%"
    )
    sys.stdout.flush()
    df.at[i, 'sello'] = str(df.at[i, 'lang']) + '_' + str(df.at[i, 'mourning']) + '_' + str(df.at[i, 'sentiment'])

print("")

# ---------------- Resultados de usar el modelo para clasificar datos.
print("\nResultados de la clasificacion\n")
print(df['sello'].value_counts())
print("\nEliminando sellos")
del df['sello']

# ---------------- Guardar datos tageados.
print("Guardando dataset de salida")
df.to_csv(datos_etiquetados, index=False, encoding="utf-8")
