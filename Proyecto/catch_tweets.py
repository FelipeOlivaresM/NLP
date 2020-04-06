import json
import dicttoxml
import xmltodict
import progressbar
from tweepy import Stream
import lxml.etree as etree
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

'''current_xmlf = open('catched_tweets.xml', 'rb')
current_data_ids = [k for k in dict(xmltodict.parse(current_xmlf)['tweets'])]
current_xmlf.close()'''


class Listener(StreamListener):
    def __init__(self, tweets_buffer_size=100, tweets_per_file=100):
        self.bar = progressbar.ProgressBar(maxval=tweets_buffer_size,
                                           widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        self.tweets_buffer_size = tweets_buffer_size
        self.tweets_per_file = tweets_per_file
        self.output_path = 'catched_tweets'
        self.tweets_buffer = dict()
        self.writed_tweets = 0
        self.num_file = 0
        self.bar.start()

    def on_data(self, data):
        tweet = json.loads(data)
        if 'place' in [k for k in tweet] and tweet['place'] is not None and tweet['retweet_count'] is 0:
            self.add_tweet_to_buffer(tweet)
            self.writed_tweets += 1
            self.bar.update(self.writed_tweets)

            if self.writed_tweets == self.tweets_buffer_size:
                self.add_tweets_to_xml_file()
                self.tweets_buffer.clear()
                self.bar.finish()
                return False

            elif len([k for k in self.tweets_buffer]) == self.tweets_per_file:
                self.add_tweets_to_xml_file()
                self.tweets_buffer.clear()
                self.num_file += 1

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
        path = str(self.output_path) + "_" + str(self.num_file) + ".xml"
        tree.getroottree().write(path, pretty_print=True, encoding='UTF-8')

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
# Parameters for the listener.

# tweets_per_file = number of tweets that are going to be written in one xml file,
#                   this number is also the number of tweets that the ram memory
#                   need to handle while writing them in the disc,if you have
#                   problems with the ram memory space maybe by decreasing this
#                   number could solve it.

# tweets_buffer_size = number of tweets that ar going to be catched.
# --------------------------------------------------------------------------------
listener = Listener()
listener.tweets_per_file = 2
listener.tweets_buffer_size = 2

# --------------------------------------------------------------------------------
# Executing the program.
# --------------------------------------------------------------------------------
authenticator = OAuthHandler(cKey, cSecret)
authenticator.set_access_token(aToken, aTokenSecret)
stream = Stream(authenticator, listener)
stream.filter(languages=['en', 'es'], track=['Coronavirus', 'coronavirus', 'covid-19', 'COVID-19'])
