def entrenar_modelos_mourning_supervisados(modelo_entr, df_balanceado, df_lematizado):
    from nltk.corpus import stopwords
    from cargar_datos import get_mourning_df
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
    import pandas as pd
    import pickle, os, nltk

    modelos_es = {
        'GBT': AdaBoostClassifier(DecisionTreeClassifier(max_depth=6), n_estimators=4),
        'RF': RandomForestClassifier(n_estimators=14, max_depth=28),
        'NN': MLPClassifier(hidden_layer_sizes=(30, 2), max_iter=400),
        'DT': DecisionTreeClassifier(max_depth=16),
        'NB': MultinomialNB()
    }

    modelos_en = {
        'GBT': AdaBoostClassifier(DecisionTreeClassifier(max_depth=6), n_estimators=4),
        'RF': RandomForestClassifier(n_estimators=14, max_depth=28),
        'NN': MLPClassifier(hidden_layer_sizes=(30, 2), max_iter=400),
        'DT': DecisionTreeClassifier(max_depth=16),
        'NB': MultinomialNB()
    }

    if modelo_entr in modelos_es and modelo_entr in modelos_en and 0 <= df_balanceado <= 1 and 0 <= df_lematizado <= 1:

        print("")
        nltk.download('stopwords')

        # ---------------- Asignacion de los modelos y vectorizadores.
        # -------- Español.
        modelo_es = modelos_es[modelo_entr]
        vectorizer_es = TfidfVectorizer(use_idf=True, stop_words=stopwords.words('spanish'))
        # -------- Ingles.
        modelo_en = modelos_en[modelo_entr]
        vectorizer_en = TfidfVectorizer(use_idf=True, stop_words=stopwords.words('english'))

        # ---------------- Lectura y separacion de datos.
        df = pd.DataFrame(get_mourning_df(df_balanceado, df_lematizado))
        # -------- Español.
        df_es = df[df.lang == 'es']
        # -------- Ingles.
        df_en = df[df.lang == 'en']
        del df
        print("Separacion de datos por idioma terminada")

        # ---------------- Separacion en data y labels de entrenamiento.
        # -------- Español.
        data_train_es, data_test_es, label_train_es, label_test_es = train_test_split(
            df_es['text'], df_es['mourning'], random_state=1
        )
        del df_es
        # -------- Ingles.
        data_train_en, data_test_en, label_train_en, label_test_en = train_test_split(
            df_en['text'], df_en['mourning'], random_state=1
        )
        print("Division de datos terminada")
        del df_en

        # ---------------- vectorizacion de los textos.
        # -------- Español.
        training_data_es = vectorizer_es.fit_transform(data_train_es)
        testing_data_es = vectorizer_es.transform(data_test_es)
        del data_train_es, data_test_es
        print("Vectorizacion en español terminada")
        # -------- Ingles.
        training_data_en = vectorizer_en.fit_transform(data_train_en)
        testing_data_en = vectorizer_en.transform(data_test_en)
        del data_test_en, data_train_en
        print("Vectorizacion en ingles terminada")

        # ---------------- almacenamiento de los vocabularios.
        # -------- Español.
        ruta_vocabulario_es = "./vocabularios/vocabulario_mourning_es.pkl"
        if os.path.exists(ruta_vocabulario_es):
            os.remove(ruta_vocabulario_es)
        pickle.dump(vectorizer_es.vocabulary_, open(ruta_vocabulario_es, "wb"))
        print("Vocabulario para español almacenado en " + ruta_vocabulario_es)
        # -------- Ingles.
        ruta_vocabulario_en = "./vocabularios/vocabulario_mourning_en.pkl"
        if os.path.exists(ruta_vocabulario_en):
            os.remove(ruta_vocabulario_en)
        pickle.dump(vectorizer_en.vocabulary_, open(ruta_vocabulario_en, "wb"))
        print("Vocabulario para ingles almacenado en " + ruta_vocabulario_en)

        # ---------------- entrenamiento y guardado de los modelos.
        # -------- Español.
        ruta_modelo_es = './modelos/' + str(type(modelo_es).__name__) + '_Mourning_es.sav'
        modelo_es.fit(training_data_es, label_train_es)
        pickle.dump(modelo_es, open(ruta_modelo_es, 'wb'))
        print("Modelo de " + str(type(modelo_es).__name__) + " en español guardado en " + ruta_modelo_es)
        # -------- Ingles.
        ruta_modelo_en = './modelos/' + str(type(modelo_en).__name__) + '_Mourning_en.sav'
        modelo_en.fit(training_data_en, label_train_en)
        pickle.dump(modelo_en, open(ruta_modelo_en, 'wb'))
        print("Modelo de " + str(type(modelo_en).__name__) + " en ingles guardado en " + ruta_modelo_en)

        # ---------------- implementacion de los modelos.
        # -------- Español.
        predictions_es = modelo_es.predict(testing_data_es)
        # -------- Ingles.
        predictions_en = modelo_en.predict(testing_data_en)
        print("Predicciones terminadas")

        # ---------------- Resultados de los modelos.
        # -------- Español.
        print("\nResultados " + str(type(modelo_es).__name__) + " Español:\n")
        print(classification_report(label_test_es, predictions_es))
        # -------- Ingles.
        print("\nResultados " + str(type(modelo_en).__name__) + " Ingles:\n")
        print(classification_report(label_test_en, predictions_en))

    elif modelo_entr not in modelos_es or modelo_entr not in modelos_en or df_balanceado > 1 or df_balanceado < 0 or df_lematizado > 1 or df_lematizado < 0:

        print("Parametros incorrectos para entrenar modelo")


entrenar_modelos_mourning_supervisados("GBT", 1, 1)
