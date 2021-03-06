import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle, os

# ---------------- Rutas de los datos y modelos.
ruta_datos = './dataset etiquetado modelos/por etiquetar'
ruta_resultados = './dataset etiquetado modelos/resultados'
ruta_modelos = './modelos'

files_path, subfolders, files_list = list(os.walk(ruta_datos))[0]
files_list.sort()
print("\nLista de archivos por etiquetar: " + str(files_list))

models_path, subfolders, models_list = list(os.walk(ruta_modelos))[0]
models_list.sort()
print("Lista de modelos disponibles: " + str(models_list))

for file in files_list:

    file_ext = str(file).split(".")[-1]
    if file_ext == "csv":

        # ---------------- Cargar datos.
        print("\nCargando df desde " + file)
        df = pd.read_csv(files_path + "/" + file, encoding='utf8', dtype=str, engine='python')

        for model in models_list:
            # ---------------- Cargar modelo.
            nombre_modelo = str(model).split(".")[0]
            print("\nCargando modelo " + nombre_modelo + "\n")
            tipo_modelo = str(model).split("_")[-2].split(".")[0].lower()
            modelo = pickle.load(open(models_path + "/" + model, 'rb'))
            idioma = nombre_modelo.split("_")[-1]

            if idioma in ['es', 'en']:
                print("Idioma del modelo validado: " + idioma)

                df_act = df[df.lang == idioma]
                df_aux = df[df.lang != idioma]
                del df

                # ---------------- Vectorizar datos cargando vocabularios.
                print("Vectorizando con el vocabulario de " + "vocabulario_" + tipo_modelo + "_" + idioma + ".pkl")
                vocabulary = pickle.load(
                    open("./vocabularios/vocabulario_" + tipo_modelo + "_" + idioma + ".pkl", "rb"))
                vectorizer = TfidfVectorizer(use_idf=True, decode_error="replace", vocabulary=vocabulary)
                data = vectorizer.fit_transform(df_act['text'])

                # ---------------- Clasificar usando modelos.
                print("Clasificando datos con " + nombre_modelo)
                predictions = modelo.predict(data)

                # ---------------- Agregar predicciones a los datos.
                print("Agregando clasificaciones del modelo " + nombre_modelo + " al archivo de salida")
                df_act[nombre_modelo] = predictions
                df_aux[nombre_modelo] = ""

                df = pd.concat([df_act, df_aux])

        # ---------------- Guardar datos tageados.
        print("\nGuardando df de salida en " + ruta_resultados + "/" + file)
        df.to_csv(ruta_resultados + "/" + file, index=False, encoding="utf-8")
