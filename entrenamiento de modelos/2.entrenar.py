from cargar_df import get_mourning_df
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

# ---------------- Lectura de los datos.
df = pd.DataFrame(get_mourning_df(0, 1))

# ---------------- Separacion en data y labels de entrnamiento.
data_train, data_test, label_train, label_test = train_test_split(df['text'], df['mourning'], random_state=1)

# ---------------- construccion de modelo de bolsa de palabras.
count_vector = CountVectorizer()
training_data = count_vector.fit_transform(data_train)
testing_data = count_vector.transform(data_test)

# ---------------- entrenamiento del modelo.
naive_bayes = MultinomialNB()
naive_bayes.fit(training_data, label_train)

# ---------------- implementacion del modelo.
predictions = naive_bayes.predict(testing_data)

# ---------------- Resultados.
print("\nResultados:\n")
print(confusion_matrix(label_test, predictions))
print("")
print(classification_report(label_test, predictions))
