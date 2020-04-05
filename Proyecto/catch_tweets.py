import json
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

tweets_buffer_size = 40
tweets_buffer = list()


# --------------------------------------------------------------------------------
# Create a listener class that process received tweets.
# On error print status.
# --------------------------------------------------------------------------------
class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        add_tweets_to_buffer(tweet)

        return

    def on_error(self, status):
        print(status)


# --------------------------------------------------------------------------------
# Add tweets to a buffer used to write them in a csv file.
# --------------------------------------------------------------------------------
def add_tweets_to_buffer(tweet):
    global tweets_buffer
    if 'place' in [k for k in tweet] and tweet['place'] is not None:
        tweets_buffer.append(tweet)
    if len(tweets_buffer) == tweets_buffer_size:
        add_tweets_to_xml_file(tweets_buffer)

    return


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

    return


my_listener = StdOutListener()
authenticator = OAuthHandler(cKey, cSecret)
authenticator.set_access_token(aToken, aTokenSecret)
stream = Stream(authenticator, my_listener)
stream.filter(languages=['en', 'es'], track=['Coronavirus', 'coronavirus', 'covid-19', 'COVID-19'])
