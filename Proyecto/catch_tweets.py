import json
import progressbar
from tweepy import Stream
import lxml.etree as etree
from tweepy import OAuthHandler
from dicttoxml import dicttoxml
from tweepy.streaming import StreamListener

# --------------------------------------------------------------------------------
# Declare variables that contains the user credentials to access Twitter API.
# --------------------------------------------------------------------------------
aToken = "341230963-Du5BiLLtrs1UFRqBZnJrv3SqUcrA49ogfhiwiB59"
aTokenSecret = "V5LpcL3762uBpq7EeTuNbSN1qpDc7RKrj9jktFg2oh3s4"
cKey = "8Jco2vpYtvvuj2UjeK75aQRWA"
cSecret = "JsB5NFUFXueV5I2Oy2uPTuVpkMXFQV06XpIV1dpHQmNilWplMj"

tweets_buffer_size = 4
tweets_buffer = list()

bar = progressbar.ProgressBar(maxval=tweets_buffer_size,
                              widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])


# --------------------------------------------------------------------------------
# Create a listener class that process received tweets.
# On error print status.
# --------------------------------------------------------------------------------
class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        return add_tweets_to_buffer(tweet)

    def on_error(self, status):
        print(status)


# --------------------------------------------------------------------------------
# Add tweets to a buffer used to write them in a xml file.
# --------------------------------------------------------------------------------
def add_tweets_to_buffer(tweet):
    global bar
    global tweets_buffer
    if 'place' in [k for k in tweet] and tweet['place'] is not None and tweet['retweet_count'] is 0:
        tweets_buffer.append(tweet)
        bar.update(len(tweets_buffer))
        return

    if len(tweets_buffer) == tweets_buffer_size:
        add_tweets_to_xml_file(tweets_buffer)
        return False


# --------------------------------------------------------------------------------
# Write the captured tweets in a xml file called captured_tweets.xml
# --------------------------------------------------------------------------------
def add_tweets_to_xml_file(tweets):
    tweet_data = dict()

    for tweet in tweets:
        tweet_id = str(tweet['id'])
        if tweet_id not in tweet_data:
            tweet_data[tweet_id] = {
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

    xml_output = dicttoxml(tweet_data, custom_root='tweets', attr_type=False)
    tree = etree.fromstring(xml_output)
    tree.getroottree().write("catched_tweets.xml", pretty_print=True)


authenticator = OAuthHandler(cKey, cSecret)
authenticator.set_access_token(aToken, aTokenSecret)
stream = Stream(authenticator, StdOutListener())
bar.start()
stream.filter(languages=['en', 'es'], track=['Coronavirus', 'coronavirus', 'covid-19', 'COVID-19'])
bar.finish()
