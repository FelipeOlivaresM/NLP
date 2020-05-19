from cargar_df import get_mourning_df
import matplotlib.pyplot as plt
import pandas as pd
import sys, collections

balanceado = 0
df = pd.DataFrame(get_mourning_df(0, balanceado))

conteo_categorias = dict()
for i, row in df.iterrows():
    sys.stdout.write("\rAnalisis de datos completado al " + str(round(((i + 1) / (df.shape[0])) * 100, 2)) + "%")
    sys.stdout.flush()
    lenguaje = str(df.at[i, 'lang'])
    mourning = str(df.at[i, 'mourning'])
    key = lenguaje + "_" + mourning
    if key in conteo_categorias:
        conteo_categorias[key] += 1
    elif key not in conteo_categorias:
        conteo_categorias[key] = 1

print("")

col_categorias = collections.OrderedDict(sorted(conteo_categorias.items()))
vector_etiquetas = [str(element[0]) for element in col_categorias.items()]
vector_conteo = [int(element[-1]) for element in col_categorias.items()]


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{v:d} ({p:.2f}%)'.format(p=pct, v=val)

    return my_autopct


plt.pie(vector_conteo, labels=vector_etiquetas, shadow=True, autopct=make_autopct(vector_conteo))
plt.title('Numero de datos usados para entrenar los modelos: ' + str(df.shape[0]))
plt.gcf().set_size_inches(14, 8)
plt.savefig('./graficas datos/' + str(balanceado) + '_distribucion_datos_entrenamiento.png')
plt.clf()

print("Proceso finalizado, las garficas fueron guardads en la carpeta graficas datos")
