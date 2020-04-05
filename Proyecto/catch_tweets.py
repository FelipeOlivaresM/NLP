import csv
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# --------------------------------------------------------------------------------
# Declare variables that contains the user credentials to access Twitter API.
# --------------------------------------------------------------------------------
aToken = "341230963-Du5BiLLtrs1UFRqBZnJrv3SqUcrA49ogfhiwiB59"
aTokenSecret = "V5LpcL3762uBpq7EeTuNbSN1qpDc7RKrj9jktFg2oh3s4"
cKey = "8Jco2vpYtvvuj2UjeK75aQRWA"
cSecret = "JsB5NFUFXueV5I2Oy2uPTuVpkMXFQV06XpIV1dpHQmNilWplMj"

tweet_data = list()
tweets_buffer = list()
tweets_buffer_size = 30


# --------------------------------------------------------------------------------
# Create a listener class that process received tweets.
# On error print status.
# --------------------------------------------------------------------------------
class StdOutListener(StreamListener):
    def on_data(self, data):
        t = json.loads(data)
        add_tweets_to_buffer(t)

        return

    def on_error(self, status):
        print(status)


# --------------------------------------------------------------------------------
# Add tweets to a buffer used to write them in a csv file.
# --------------------------------------------------------------------------------
def add_tweets_to_buffer(tweet):
    global tweets_buffer
    tweets_buffer.append(tweet)
    if (len(tweets_buffer) == tweets_buffer_size):
        add_tweets_to_csv_file(tweets_buffer)

    return


# --------------------------------------------------------------------------------
# Write the captured tweets in a csv file called captured_tweets.csv
# --------------------------------------------------------------------------------
def add_tweets_to_csv_file(tweets):
    with open('./catched_tweets.csv', 'w') as csvfile:
        fieldnames = [
            'id',
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
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for tweet in tweets:
            if tweet['place'] is not None:
                tweet_data.append({
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'screen_name': tweet['user']['screen_name'],
                    'created_at': tweet['created_at'],
                    'retweet_count': tweet['retweet_count'],
                    'favorite_count': tweet['favorite_count'],
                    'friends_count': tweet['user']['friends_count'],
                    'followers_count': tweet['user']['followers_count'],
                    'lang': tweet['lang'],
                    'country': tweet['place']['country']
                })
                writer.writerows(tweet_data)
                tweet_data.pop()
            else:
                tweet_data.append({
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'screen_name': tweet['user']['screen_name'],
                    'created_at': tweet['created_at'],
                    'retweet_count': tweet['retweet_count'],
                    'favorite_count': tweet['favorite_count'],
                    'friends_count': tweet['user']['friends_count'],
                    'followers_count': tweet['user']['followers_count'],
                    'lang': tweet['lang'],
                    'country': 'None'
                })
            writer.writerows(tweet_data)
            tweet_data.pop()

        return False


my_listener = StdOutListener()
authenticator = OAuthHandler(cKey, cSecret)
authenticator.set_access_token(aToken, aTokenSecret)
stream = Stream(authenticator, my_listener)
stream.filter(languages=['en', 'es'], track=['Coronavirus', 'coronavirus', 'covid-19', 'COVID-19'])
