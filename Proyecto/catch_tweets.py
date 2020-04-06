import json
import dicttoxml
import progressbar
from tweepy import Stream
import lxml.etree as etree
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

output_path = 'catched_tweets'
number_of_tweets_for_catch = 4  # <----- Numero de tweets en total.
tweets_buffer = dict()
tweets_per_file = 1  # <----- Numero de tweets por archivo.
writed_tweets = 0
num_file = 0

widget_parameters = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]
bar = progressbar.ProgressBar(maxval=number_of_tweets_for_catch, widgets=widget_parameters)


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
    global num_file
    global bar

    if 'place' in [k for k in tweet] and tweet['place'] is not None and tweet['retweet_count'] is 0:
        add_tweet_to_buffer(tweet)
        writed_tweets += 1

        if writed_tweets == number_of_tweets_for_catch:
            add_tweets_to_xml_file()
            tweets_buffer.clear()
            return False

        elif len([k for k in tweets_buffer]) == tweets_per_file:
            add_tweets_to_xml_file()
            tweets_buffer.clear()
            num_file += 1
            return


def add_tweet_to_buffer(tweet):
    global tweets_buffer

    tweet_id = str(tweet['id'])
    tweets_buffer[tweet_id] = {
        'text': tweet['text'],
        'screen_name': tweet['user']['screen_name'],
        'created_at': tweet['created_at'],
        'retweet_count': tweet['retweet_count'],
        'favorite_count': tweet['favorite_count'],
        'friends_count': tweet['user']['friends_count'],
        'followers_count': tweet['user']['followers_count'],
        'lang': tweet['lang'],
        'country': tweet['place']['country']
    }


def add_tweets_to_xml_file():
    global tweets_buffer
    global output_path
    global num_file

    print("Escribiendo archivo " + str(num_file))
    xml_output = dicttoxml.dicttoxml(tweets_buffer, custom_root='tweets', attr_type=False)
    tree = etree.fromstring(xml_output)
    path = str(output_path) + "_" + str(num_file) + ".xml"
    tree.getroottree().write(path, pretty_print=True, encoding='UTF-8')
    print("Archivo " + str(num_file) + " terminado")


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
stream = Stream(authenticator, Listener())
stream.filter(languages=['en', 'es'], track=['Coronavirus', 'coronavirus', 'covid-19', 'COVID-19'])
