import csv
import json
import time

from os import path
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError
from requests.exceptions import Timeout, ConnectionError

tags = [
    'coronavirus', 'covid-19', 'covid19', 'covid 19',
    'Coronavirus', 'Covid-19', 'Covid19', 'Covid 19',
    'CORONAVIRUS', 'COVID-19', 'COVID19', 'COVID 19',
    'CoronaVirus', 'SARSCoV2', 'SARS-CoV2', 'SARS-CoV-2'
]

output_path = "./twitter_data/catched_tweets_1.csv"  # <----- Ruta de salida para el archivo.
number_of_tweets_for_catch = 1000  # <----- Numero de tweets en total.
start_time = time.time()
tweet_as_list = list()
writed_tweets = 0


class Listener(StreamListener):
    def on_data(self, data):
        process_incoming_data(json.loads(data))
        if writed_tweets == number_of_tweets_for_catch:
            return False
        else:
            return

    def on_error(self, status):
        print(status)
        return False


def process_incoming_data(tweet):
    global number_of_tweets_for_catch
    global output_path
    global writed_tweets
    global tags

    if 'place' in [k for k in tweet] and tweet['place'] is not None and not tweet['retweeted']:
        if 'RT @' not in tweet['text'] and any(tag in tweet['text'] for tag in tags):
            tweet_to_list(tweet)
            add_tweets_to_csv_file()
            writed_tweets += 1

            file = open(output_path)

            print(
                "Tweets capturados: " +
                str(writed_tweets) + " de " +
                str(number_of_tweets_for_catch) +
                " - Tiempo de ejecucion: " + str(int((time.time() - start_time) / 60)) +
                " minutos - Tweets en el archivo: " + str(sum(1 for row in csv.reader(file)) - 1)
            )

            file.close()


def tweet_to_list(tweet):
    global tweet_as_list
    tweet_as_list = [
        tweet['id'],
        tweet['text'].strip().replace("\n", " "),
        tweet['user']['screen_name'],
        tweet['created_at'],
        tweet['retweet_count'],
        tweet['favorite_count'],
        tweet['user']['friends_count'],
        tweet['user']['followers_count'],
        tweet['lang'],
        tweet['place']['country']
    ]


def add_tweets_to_csv_file():
    global tweet_as_list
    global output_path
    if path.isfile(output_path) is False:
        csv_file = open(output_path, 'a', encoding="utf-8")
        writer = csv.writer(csv_file)
        writer.writerow(
            ['id',
             'text',
             'screen_name',
             'created_at',
             'retweet_count',
             'favorite_count',
             'friends_count',
             'followers_count',
             'lang',
             'country'
             ]
        )
        csv_file.close()
    if path.isfile(output_path) is True:
        csv_file = open(output_path, 'a', encoding="utf-8")
        writer = csv.writer(csv_file)
        writer.writerow(tweet_as_list)
        csv_file.close()


# --------------------------------------------------------------------------------
# Declare variables that contains the user credentials to access Twitter API.
# --------------------------------------------------------------------------------
aToken = "341230963-Du5BiLLtrs1UFRqBZnJrv3SqUcrA49ogfhiwiB59"
aTokenSecret = "V5LpcL3762uBpq7EeTuNbSN1qpDc7RKrj9jktFg2oh3s4"
cKey = "8Jco2vpYtvvuj2UjeK75aQRWA"
cSecret = "JsB5NFUFXueV5I2Oy2uPTuVpkMXFQV06XpIV1dpHQmNilWplMj"

# --------------------------------------------------------------------------------
# Executing the program.
# --------------------------------------------------------------------------------
authenticator = OAuthHandler(cKey, cSecret)
authenticator.set_access_token(aToken, aTokenSecret)

print("")
while writed_tweets != number_of_tweets_for_catch:
    stream = Stream(authenticator, Listener())
    try:
        stream.filter(languages=['en', 'es'], track=tags)
    except (Timeout, ConnectionError, ProtocolError):
        stream.disconnect()
        print("\nConexion cerrada, limite de lectura superado, esperando para reconectar.")
        time.sleep(20)
        print("Reconectando... \n")
