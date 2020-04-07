import csv
import json
import time
import walk

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

tags = [
    'coronavirus', 'covid-19', 'covid19', 'covid 19',
    'Coronavirus', 'Covid-19', 'Covid19', 'Covid 19',
    'CORONAVIRUS', 'COVID-19', 'COVID19', 'COVID 19',
    'CoronaVirus', 'SARSCoV2', 'SARS-CoV2', 'SARS-CoV-2'
]

start_time = time.time()
number_of_tweets_for_catch = 2  # <----- Numero de tweets en total.
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
        return False


def process_incoming_data(tweet):
    global number_of_tweets_for_catch
    global writed_tweets
    global tags

    if 'place' in [k for k in tweet] and tweet['place'] is not None and not tweet['retweeted']:
        if 'RT @' not in tweet['text'] and any(tag in tweet['text'] for tag in tags):
            tweet_to_list(tweet)
            add_tweets_to_csv_file()
            writed_tweets += 1

            print(
                " Tweets capturados: " +
                str(writed_tweets) + " de " +
                str(number_of_tweets_for_catch) +
                " - Tiempo de ejecucion: " + str(int((time.time() - start_time) / 60)) +
                " minutos."
            )


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
    path_output = "catched_tweets_1.csv"
    path_1, subfolders, files_list = list(walk('./'))
    if path_output not in files_list:
        csv_file = open(path_output, 'a', encoding="utf-8")
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
    if path_output in files_list:
        csv_file = open(path_output, 'a', encoding="utf-8")
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
while writed_tweets <= number_of_tweets_for_catch:
    print("Reinicinando")
    try:
        stream = Stream(authenticator, Listener())
        stream.filter(languages=['en', 'es'], track=tags)
    except:
        print("\nConexion cerrada, limite de lectura superado, esperando para reconectar.")
        time.sleep(60)
        print("Reconectando.\n")
