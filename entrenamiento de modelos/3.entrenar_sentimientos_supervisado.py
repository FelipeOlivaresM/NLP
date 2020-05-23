from cargar_datos import get_feelings_df
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import pandas as pd
import pickle, os

print("")
usar_datos_incrementados = 1

modelos = {
    'GBT': AdaBoostClassifier(DecisionTreeClassifier(max_depth=16), n_estimators=8),
    'RF': RandomForestClassifier(n_estimators=34, max_depth=48),
    'NN': MLPClassifier(hidden_layer_sizes=(4, 4)),
    'DT': DecisionTreeClassifier(max_depth=84),
    'NB': MultinomialNB()
}

# ---------------- Asignacion de los modelos.
modelo = modelos['DT']
vectorizer = TfidfVectorizer(use_idf=True)

if usar_datos_incrementados == 1:
    print("Usando datos incrementados para entrenar\n")
    df_entrenamiento = pd.DataFrame(get_feelings_df(0, 0, 1, 1))
    df_testeo = pd.DataFrame(get_feelings_df(0, 0, 1, 0))

    data_train = df_entrenamiento['text']
    data_test = df_testeo['text']
    label_train = df_entrenamiento['sentiment']
    label_test = df_testeo['sentiment']

    # ---------------- vectorizacion de los textos.
    training_data = vectorizer.fit_transform(data_train)
    testing_data = vectorizer.transform(data_test)

    # ---------------- almacenamiento de los vocabularios.
    ruta_vocabulario = "./vocabularios/vocabulario_sentiment.pkl"
    if os.path.exists(ruta_vocabulario):
        os.remove(ruta_vocabulario)
    pickle.dump(vectorizer.vocabulary_, open(ruta_vocabulario, "wb"))

    # ---------------- entrenamiento y guardado de los modelos.
    modelo.fit(training_data, label_train)
    pickle.dump(modelo, open('./modelos/' + str(type(modelo).__name__) + '_Sentiment.sav', 'wb'))

    # ---------------- implementacion de los modelos.
    predictions = modelo.predict(testing_data)

    # ---------------- Resultados de los modelos.
    print("\nResultados " + str(type(modelo).__name__) + ":\n")
    print(classification_report(label_test, predictions))

elif usar_datos_incrementados == 0:
    print("Usando datos certificados para entrenar\n")
    # ---------------- Lectura y separacion de datos.
    df = pd.DataFrame(get_feelings_df(0, 1, 1, 0))

    # ---------------- Separacion en data y labels de entrenamiento.
    data_train, data_test, label_train, label_test = train_test_split(
        df['text'], df['sentiment']
    )

    # ---------------- vectorizacion de los textos.
    training_data = vectorizer.fit_transform(data_train)
    testing_data = vectorizer.transform(data_test)

    # ---------------- almacenamiento de los vocabularios.
    ruta_vocabulario = "./vocabularios/vocabulario_sentiment.pkl"
    if os.path.exists(ruta_vocabulario):
        os.remove(ruta_vocabulario)
    pickle.dump(vectorizer.vocabulary_, open(ruta_vocabulario, "wb"))

    # ---------------- entrenamiento y guardado de los modelos.
    modelo.fit(training_data, label_train)
    pickle.dump(modelo, open('./modelos/' + str(type(modelo).__name__) + '_Sentiment.sav', 'wb'))

    # ---------------- implementacion de los modelos.
    predictions = modelo.predict(testing_data)

    # ---------------- Resultados de los modelos.
    print("\nResultados " + str(type(modelo).__name__) + ":\n")
    print(classification_report(label_test, predictions))
