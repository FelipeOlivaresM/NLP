import pandas as pd
import csv, os

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.


output_path1 = "./twitter_data/datos_en_bruto/catched_tweets.csv"  # <---- este se conserva.
output_path2 = "./twitter_data/datos_en_bruto/catched_tweets_5.csv"  # <---- este se elimina.

if os.path.exists(output_path1) and os.path.exists(output_path2) and output_path1 != output_path2:
    print("")
    file = open(output_path1)
    rows_count0 = sum(1 for row in csv.reader(file)) - 1
    file.close()
    file = open(output_path2)
    rows_count2 = sum(1 for row in csv.reader(file)) - 1
    file.close()
    df1 = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')
    df2 = pd.read_csv(output_path2, encoding='utf8', dtype=str, engine='python')
    df1 = df1.append(df2)
    df1.to_csv(output_path1, index=False, encoding="utf-8")
    print(
        "\nArchivo " + str(output_path1.split("/")[-1]) + " Exitosamente unido al archivo " +
        str(output_path2.split("/")[-1])
    )
    file = open(output_path1)
    rows_count1 = sum(1 for row in csv.reader(file)) - 1
    file.close()
    df1 = pd.read_csv(output_path1)
    print("\nTweets finales en el archivo " + str(output_path1.split("/")[-1]) + ": " + str(rows_count1))
    print("Tweets iniciales en el archivo " + str(output_path1.split("/")[-1]) + ": " + str(rows_count0))
    print("Tweets iniciales en el archivo " + str(output_path2.split("/")[-1]) + ": " + str(rows_count2))
    os.remove(output_path2)
    print("\nArchivo " + str(output_path2.split("/")[-1]) + " exitosamente eliminado")
else:
    print("Alguno de los archivo no existe o fue borrado")
