from cargar_datos import get_feelings_df
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle

print("")

# ---------------- Asignacion de los modelos.
modelo = MultinomialNB()
modelo_es = MultinomialNB()
modelo_en = MultinomialNB()
count_vector = TfidfVectorizer()

# ---------------- Lectura y separacion de datos.
df = pd.DataFrame(get_feelings_df(0, 1, 1))
df_es = df[df.lang == 'es']
df_en = df[df.lang == 'en']

# ---------------- Separacion en data y labels de entrenamiento.
data_train, data_test, label_train, label_test = train_test_split(
    df['text'], df['sentiment'],
    random_state=1
)
data_train_es, data_test_es, label_train_es, label_test_es = train_test_split(
    df_es['text'], df_es['sentiment'],
    random_state=1
)
data_train_en, data_test_en, label_train_en, label_test_en = train_test_split(
    df_en['text'], df_en['sentiment'],
    random_state=1
)

# ---------------- vectorizacion de los textos.
training_data = count_vector.fit_transform(data_train)
testing_data = count_vector.transform(data_test)
training_data_es = count_vector.fit_transform(data_train_es)
testing_data_es = count_vector.transform(data_test_es)
training_data_en = count_vector.fit_transform(data_train_en)
testing_data_en = count_vector.transform(data_test_en)

# ---------------- entrenamiento y guardado de los modelos.
modelo.fit(training_data, label_train)
pickle.dump(modelo, open('./modelos/' + str(type(modelo).__name__) + '_Completo.sav', 'wb'))
modelo_es.fit(training_data_es, label_train_es)
pickle.dump(modelo_es, open('./modelos/' + str(type(modelo_es).__name__) + '_Español.sav', 'wb'))
modelo_en.fit(training_data_en, label_train_en)
pickle.dump(modelo_en, open('./modelos/' + str(type(modelo_en).__name__) + '_Ingles.sav', 'wb'))

# ---------------- implementacion de los modelos.
predictions = modelo.predict(testing_data)
predictions_es = modelo_es.predict(testing_data_es)
predictions_en = modelo_en.predict(testing_data_en)

# ---------------- Resultados de los modelos.
print("\nResultados " + str(type(modelo).__name__) + "_Completo:\n")
reporte1 = classification_report(label_test, predictions)
print(reporte1)
print("\nResultados " + str(type(modelo_es).__name__) + "_Español:\n")
reporte2 = classification_report(label_test_es, predictions_es)
print(reporte2)
print("\nResultados " + str(type(modelo_en).__name__) + "_Ingles:\n")
reporte3 = classification_report(label_test_en, predictions_en)
print(reporte3)
