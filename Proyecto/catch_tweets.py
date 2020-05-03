from os import path
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError
from requests.exceptions import Timeout, ConnectionError
import re, csv, sys, json, time, threading

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.

output_path = "./twitter_data/datos_en_bruto/catched_tweets_1.csv"  # <----- Ruta de salida para el archivo, el archivo 4 es para pruebas.
number_of_tweets_for_catch = 400000  # <----- Numero de tweets en total.
start_time = time.time()
lock = threading.Lock()
readed_tweets = 0
writed_tweets = 0

file = open(output_path)
rows_count = sum(1 for row in csv.reader(file)) - 1
file.close()

print("")
print("Tweets iniciales en el archivo " + str(output_path.split("/")[-1]) + ": " + str(rows_count))
time.sleep(6)

tags = [
    'covid-19', 'covid19', 'Covid-19', 'Covid19', 'COVID-19', 'COVID19', 'CoVid-19', 'CoVid19', 'COVIDー19',
    'pandemic', 'Pandemic', 'covidpandemic', 'Covidpandemic', 'CovidPandemic', 'COVIDpandemic',
    'CORONAVIRUS', 'coronavirus', 'coronaVirus', 'Coronavirus', 'CoronaVirus', 'COVID__19',
    'CuarentenaTotal', 'CuarentenaCoronavirus', 'Covid_19', 'SARSCoV2',
    'Cuarentena', 'CuarentenaInteligente', 'AislamientoObligatorio',
    'CuarentenaCoronaVirus', 'CuarentenaPositiva', 'MeQuedoEnCasa',
    'pandemia', 'Pandemia', 'TrumpLiesAboutCoronavirus'
]


class Listener(StreamListener):
    def on_data(self, data):
        threading.Thread(target=process_incoming_data, kwargs={'tweet': json.loads(data)}).start()
        lock.acquire()
        if writed_tweets == number_of_tweets_for_catch:
            lock.release()
            return False
        else:
            lock.release()
            return

    def on_error(self, status):
        print("Error: " + str(status))
        return False


def process_incoming_data(**thread_data):
    global number_of_tweets_for_catch
    global writed_tweets
    global readed_tweets
    global rows_count
    global tags

    lock.acquire()
    readed_tweets += 1
    lock.release()

    tweet = thread_data['tweet']
    if 'place' in [k for k in tweet]:  # and tweet['place'] is not None <----- restriccion de lugar.
        if 'RT @' not in tweet['text'] and not tweet['retweeted']:
            add_tweets_to_csv_file(tweet_to_list(tweet))
            lock.acquire()
            writed_tweets += 1
            rows_count += 1
            lock.release()
            print(
                "Capturados: " +
                str(writed_tweets) + " de " +
                str(number_of_tweets_for_catch) +
                " - tiempo: " + str(int((time.time() - start_time) / 60)) +
                " minutos - tweets en el archivo " + output_path.split("/")[-1] +
                ": " + str(rows_count) +
                " - hilo: " + str(threading.current_thread().name) +
                " - tweets revisados: " + str(readed_tweets)
            )
        return


def tweet_to_list(tweet):
    if 'extended_tweet' in [k for k in tweet]:
        text = (
            re.sub(' +', ' ', re.sub("http\S+", "", str(tweet['extended_tweet']['full_text']).replace("\n", " ")))
        ).strip()
    else:
        text = (re.sub(' +', ' ', re.sub("http\S+", "", str(tweet['text']).replace("\n", " ")))).strip()
    if tweet['place'] is not None:
        country = tweet['place']['country']
    elif tweet['place'] is None:
        country = None
    return [
        tweet['id'],
        text,
        tweet['user']['screen_name'],
        tweet['created_at'],
        tweet['retweet_count'],
        tweet['favorite_count'],
        tweet['user']['friends_count'],
        tweet['user']['followers_count'],
        tweet['lang'],
        country
    ]


def add_tweets_to_csv_file(tweet_as_list):
    if path.isfile(output_path) is False:
        lock.acquire()
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
        lock.release()
    if path.isfile(output_path) is True:
        lock.acquire()
        csv_file = open(output_path, 'a', encoding="utf-8")
        writer = csv.writer(csv_file)
        writer.writerow(tweet_as_list)
        csv_file.close()
        lock.release()


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
    except (KeyboardInterrupt, SystemExit):
        stream.disconnect()
        print("\nTweets capturados: " + str(writed_tweets) + "\n")
        sys.exit()

print("\nTweets capturados: " + str(writed_tweets) + "\n")
sys.exit()
