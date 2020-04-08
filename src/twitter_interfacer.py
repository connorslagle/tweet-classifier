from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter_credentials


class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.auth_handler = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        self.auth_handler.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list,locations_list,tweet_file_size, async_bool):
        '''
        
        '''
        listener = StdOutListener(fetched_tweets_filename,tweet_file_size)

        stream = Stream(self.auth_handler, listener)

        stream.filter(track=hash_tag_list,locations=locations_list, is_async=async_bool)

class StdOutListener(StreamListener):
    """
    This tweet listener will record tweets with the keywords specified in
    has_tag_list
    """

    def __init__(self, fetched_tweets_filename,tweet_file_size):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.tweet_count = 0
        self.tweet_file_size = tweet_file_size

    def on_data(self, data):
        '''
        Method that describes what to do when encountering tweet.

        Inputs: data 
        '''
        try:
            print(f'Tweets recorded: {self.tweet_count}')
            if self.tweet_count < self.tweet_file_size:
                with open(self.fetched_tweets_filename, 'a') as f:
                    f.write(data)
                self.tweet_count += 1
                return True
            else:
                print(f'Finished\nTweets recorded: {self.tweet_count}')
                return False
        except BaseException as e:
            print("Error on data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            print(f'Error Code: {status}')
            return False

if __name__ == "__main__":
    print('test')