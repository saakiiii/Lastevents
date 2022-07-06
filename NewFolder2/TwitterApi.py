import tweepy

CONSUMER_KEY = 'vVieA34hl3FO2zm54680dVjQ8'
CONSUMER_SECRET = 'LvyTVBUBj1YVlE1EVAB21dGnTrJpMPK4IwGrrBFFVq2qlNT89F'
ACCESS_TOKEN = '1542852249122406401-Dor6nrmZxUqSUbfcQIIlXcZLMiCSKS'
ACCESS_TOKEN_SECRET = 'cMNgtmZFnAY8mZS0YZJ1jXwOr8XjWJOSs7yhsw9E6m8dK' 
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAPeqeQEAAAAAViYCt1QoSsAbiUbOd34HBeq0cdo%3DeWyUbKm0mb44BoaTnIjSEfoeKzT5jPnaybZqNNILIMS2xqZfmi' 
 
class TwitterApi:
    
    def __init__(self):
        self.twitterapi  = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)

    def Tweet(self, text=None, poll_options=None, poll_duration_minutes=None, direct_message_deep_link=None):
        self.twitterapi.create_tweet(text=text,
                                     direct_message_deep_link=direct_message_deep_link,
                                     poll_options=poll_options,
                                     poll_duration_minutes=poll_duration_minutes)
        return True
            
# news_tweet_template = f"lastevents.space | {heading} https://www.lastevents.space/news/read/view/{heading_url}"
# blog_tweet_template = f"lastevents.space | Check the latest article, {heading} https://www.lastevents.space/blog/read/view/{heading_url}"
