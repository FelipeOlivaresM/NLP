from cargar_datos import get_mourning_df, get_feelings_df
import matplotlib.pyplot as plt
import pandas as pd
import sys, collections
from colour import Color

print("")
balanceado = 1
entrenamiento = 0
df_mourning = pd.DataFrame(get_mourning_df(0, balanceado, 0, entrenamiento))
df_sentiments = pd.DataFrame(get_feelings_df(0, balanceado, 0, entrenamiento))

conteo_categorias1 = dict()
for i, row in df_mourning.iterrows():
    sys.stdout.write(
        "\rAnalisis de datos luto completado al " + str(round(((i + 1) / (df_mourning.shape[0])) * 100, 2)) + "%"
    )
    sys.stdout.flush()
    lenguaje = str(df_mourning.at[i, 'lang'])
    mourning = str(df_mourning.at[i, 'mourning'])
    key = lenguaje + "_" + mourning
    if key in conteo_categorias1:
        conteo_categorias1[key] += 1
    elif key not in conteo_categorias1:
        conteo_categorias1[key] = 1

print("")

conteo_categorias2 = dict()
for i, row in df_sentiments.iterrows():
    sys.stdout.write(
        "\rAnalisis de datos sentimientos completado al " +
        str(round(((i + 1) / (df_sentiments.shape[0])) * 100, 2)) + "%"
    )
    sys.stdout.flush()
    lenguaje = str(df_sentiments.at[i, 'lang'])
    mourning = str(df_sentiments.at[i, 'sentiment'])
    key = lenguaje + "_" + mourning
    if key in conteo_categorias2:
        conteo_categorias2[key] += 1
    elif key not in conteo_categorias2:
        conteo_categorias2[key] = 1

print("")

col_categorias1 = collections.OrderedDict(sorted(conteo_categorias1.items()))
vector_etiquetas1 = [str(element[0]) for element in col_categorias1.items()]
vector_conteo1 = [int(element[-1]) for element in col_categorias1.items()]

col_categorias2 = collections.OrderedDict(sorted(conteo_categorias2.items()))
vector_etiquetas2 = [str(element[0]) for element in col_categorias2.items()]
vector_conteo2 = [int(element[-1]) for element in col_categorias2.items()]


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{v:d} ({p:.2f}%)'.format(p=pct, v=val)

    return my_autopct


red = Color("orangered")
colors = list(red.range_to(Color("orange"), len(vector_conteo1)))
colors = [color.rgb for color in colors]

plt.pie(vector_conteo1, labels=vector_etiquetas1, shadow=True, autopct=make_autopct(vector_conteo1),
        colors=colors)
plt.title('Numero de datos usados para entrenar los modelos de luto: ' + str(df_mourning.shape[0]))
plt.gcf().set_size_inches(10, 8)
plt.savefig('./graficas datos/distribucion_datos_mourning_c' + str(balanceado) + str(entrenamiento) + '.png')
plt.clf()

red = Color("orangered")
colors = list(red.range_to(Color("orange"), len(vector_conteo2)))
colors = [color.rgb for color in colors]

plt.pie(vector_conteo2, labels=vector_etiquetas2, shadow=True, autopct=make_autopct(vector_conteo2),
        colors=colors)
plt.title('Numero de datos usados para entrenar los modelos de sentimientos: ' + str(df_sentiments.shape[0]))
plt.gcf().set_size_inches(10, 8)
plt.savefig('./graficas datos/distribucion_datos_sentiments_c' + str(balanceado) + str(entrenamiento) + '.png')
plt.clf()

print("Proceso finalizado, las graficas fueron guardads en la carpeta graficas datos")
