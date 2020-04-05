import json
import xmltodict
import dicttoxml
import progressbar
from tweepy import Stream
import lxml.etree as etree
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


class Listener(StreamListener):
    def __init__(self, tweets_buffer_size=10, tweets_buffer=dict()):
        self.tweets_buffer_size = tweets_buffer_size
        self.tweets_buffer = tweets_buffer

    def on_data(self, data):
        tweet = json.loads(data)
        if 'place' in [k for k in tweet] and tweet['place'] is not None and tweet['retweet_count'] is 0:
            self.add_tweet_to_buffer(tweet)
            return

        if len([k for k in self.tweets_buffer]) == self.tweets_buffer_size:
            self.add_tweets_to_xml_file()
            return False

    def add_tweet_to_buffer(self, tweet):
        tweet_id = str(tweet['id'])
        self.tweets_buffer[tweet_id] = {
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

    def add_tweets_to_xml_file(self):
        xml_output = dicttoxml.dicttoxml(self.tweets_buffer, custom_root='tweets', attr_type=False)
        tree = etree.fromstring(xml_output)
        tree.getroottree().write("catched_tweets.xml", pretty_print=True)

    def on_error(self, status):
        print("Error ", status)
        return False


# --------------------------------------------------------------------------------
# Declare variables that contains the user credentials to access Twitter API.
# --------------------------------------------------------------------------------
aToken = "341230963-Du5BiLLtrs1UFRqBZnJrv3SqUcrA49ogfhiwiB59"
aTokenSecret = "V5LpcL3762uBpq7EeTuNbSN1qpDc7RKrj9jktFg2oh3s4"
cKey = "8Jco2vpYtvvuj2UjeK75aQRWA"
cSecret = "JsB5NFUFXueV5I2Oy2uPTuVpkMXFQV06XpIV1dpHQmNilWplMj"

# --------------------------------------------------------------------------------
# Get current tweet ids in the xml file.
# --------------------------------------------------------------------------------
current_xmlf = open('catched_tweets.xml', 'rb')
current_data_ids = [k for k in dict(xmltodict.parse(current_xmlf)['tweets'])]
current_xmlf.close()

# --------------------------------------------------------------------------------
# Parameters for the listener.
# --------------------------------------------------------------------------------
listener = Listener()
listener.tweets_buffer_size = 2

# --------------------------------------------------------------------------------
# Executing the program.
# --------------------------------------------------------------------------------
authenticator = OAuthHandler(cKey, cSecret)
authenticator.set_access_token(aToken, aTokenSecret)
stream = Stream(authenticator, listener)
stream.filter(languages=['en', 'es'], track=['Coronavirus', 'coronavirus', 'covid-19', 'COVID-19'])
