import json
import time
from datetime import datetime

import pandas as pd
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

tags = [
    'coronavirus', 'covid-19', 'covid19', 'covid 19',
    'Coronavirus', 'Covid-19', 'Covid19', 'Covid 19',
    'CORONAVIRUS', 'COVID-19', 'COVID19', 'COVID 19',
    'CoronaVirus', 'SARSCoV2', 'SARS-CoV2', 'SARS-CoV-2'
]

tweets_buffer = pd.DataFrame(columns=[
    'id', 'text', 'screen_name', 'created_at', 'retweet_count',
    'favorite_count', 'friends_count', 'followers_count', 'lang',
    'country'
])

number_of_tweets_for_catch = 2000  # <----- Numero de tweets en total.
tweets_per_file = 500  # <----- Numero de tweets por archivo.
writed_tweets = 0

start_time = time.time()


class Listener(StreamListener):
    def on_data(self, data):
        return process_incoming_data(json.loads(data))

    def on_error(self, status):
        return False


def process_incoming_data(tweet):
    global number_of_tweets_for_catch
    global tweets_per_file
    global tweets_buffer
    global writed_tweets
    global tags

    if 'place' in [k for k in tweet] and tweet['place'] is not None and not tweet['retweeted']:
        if 'RT @' not in tweet['text'] and any(tag in tweet['text'] for tag in tags):

            add_tweet_to_buffer(tweet)
            writed_tweets += 1

            files_in_buffer = len(tweets_buffer.index)

            print(
                "Tweets en el buffer: " +
                str(files_in_buffer) + " de " +
                str(tweets_per_file) +
                " - Tweets capturados: " +
                str(writed_tweets) + " de " +
                str(number_of_tweets_for_catch) +
                " - Tiempo de ejecucion: " + str(int((time.time() - start_time) / 60)) +
                " minutos."
            )

            if writed_tweets == number_of_tweets_for_catch:
                add_tweets_to_csv_file()
                tweets_buffer = tweets_buffer.drop([0])
                print("Proceso terminado.\n")
                return False

            elif files_in_buffer == tweets_per_file:
                add_tweets_to_csv_file()
                tweets_buffer = tweets_buffer.drop([0])
                print("Buffer reiniciado.\n")
                return


def add_tweet_to_buffer(tweet):
    global tweets_buffer
    tweets_buffer = tweets_buffer.append(pd.DataFrame({
        'id': [tweet['id']],
        'text': [tweet['text'].strip().replace("\n", " ")],
        'screen_name': [tweet['user']['screen_name']],
        'created_at': [tweet['created_at']],
        'retweet_count': [tweet['retweet_count']],
        'favorite_count': [tweet['favorite_count']],
        'friends_count': [tweet['user']['friends_count']],
        'followers_count': [tweet['user']['followers_count']],
        'lang': [tweet['lang']],
        'country': [tweet['place']['country']]
    }))


def add_tweets_to_csv_file():
    global tweets_buffer
    path = str(len(tweets_buffer.index)) + "_catched_tweets_(" + str(
        datetime.now().strftime("%H:%M:%S - %d-%m-%Y")) + ").csv"
    tweets_buffer.to_csv(path, encoding='utf-8', index=False)
    print("\nEscritura del archivo " + path + " terminada.")


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
while writed_tweets is not number_of_tweets_for_catch:
    try:
        stream = Stream(authenticator, Listener())
        stream.filter(languages=['en', 'es'], track=tags)
    except ValueError as valerr:
        print("\nConexion cerrada, limite de lectura superado, esperando para reconectar.")
        time.sleep(60)
        print("Reconectando.\n")
