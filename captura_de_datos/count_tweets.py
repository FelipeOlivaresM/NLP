import csv

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.


output_path = "./twitter_data/datos_en_bruto/catched_tweets_originales.csv"

file = open(output_path)
rows_count = sum(1 for row in csv.reader(file)) - 1
file.close()

print("\nTweets finales en el archivo " + str(output_path.split("/")[-1]) + ": " + str(rows_count))