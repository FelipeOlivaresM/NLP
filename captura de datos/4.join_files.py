import pandas as pd
import csv, os

output_path1 = "./twitter data/datos en bruto/catched_tweets_full_data.csv"  # <---- este se conserva.
output_path2 = "./twitter data/datos en bruto/catched_tweets_0.csv"  # <---- este se elimina.

if os.path.exists(output_path1) and os.path.exists(output_path2) and output_path1 != output_path2:
    file = open(output_path1)
    rows_count0 = sum(1 for row in csv.reader(file)) - 1
    file.close()
    file = open(output_path2)
    rows_count2 = sum(1 for row in csv.reader(file)) - 1
    file.close()
    print("\nCargando datos de " + str(output_path2.split("/")[-1]) + " y de " + str(output_path1.split("/")[-1]))
    df1 = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')
    df2 = pd.read_csv(output_path2, encoding='utf8', dtype=str, engine='python')
    print("Uniendo datos de " + str(output_path2.split("/")[-1]) + " a " + str(output_path1.split("/")[-1]))
    df1 = df1.append(df2)
    df1.to_csv(output_path1, index=False, encoding="utf-8")
    print(
        "Archivo " + str(output_path2.split("/")[-1]) + " Exitosamente unido al archivo " +
        str(output_path1.split("/")[-1])
    )
    file = open(output_path1)
    rows_count1 = sum(1 for row in csv.reader(file)) - 1
    file.close()
    del df1
    df1 = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')
    print("\nReporte de resultados union de datos: ")
    print("Tweets finales en el archivo " + str(output_path1.split("/")[-1]) + ": " + str(rows_count1))
    print("Tweets iniciales en el archivo " + str(output_path1.split("/")[-1]) + ": " + str(rows_count0))
    print("Tweets iniciales en el archivo " + str(output_path2.split("/")[-1]) + ": " + str(rows_count2))
    os.remove(output_path2)
    print("\nArchivo " + str(output_path2.split("/")[-1]) + " exitosamente eliminado")
else:
    print("\nAlguno de los archivo no existe o fue borrado")
