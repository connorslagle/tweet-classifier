from bson import json_util
from pymongo import MongoClient
import pprint

# Connect to mongoserver in docker container '27017'
client = MongoClient('localhost', 27017)

# Goal: to filter db by state
# Connect to tweet db
db = client['political_tweet_nlp']

# Connect to test set - 'oregon_covid'
or_covid = db['arkansas_covid_trump']

first_elem = or_covid.find_one()

# Tweet table columns

# 'id' - tweet id, int64 '1245437551424528384'
# 'created_at' - when tweet was created, str 'Wed Apr 01 19:47:06 +0000 2020'
# 'source' - what interface tweet was sent from, str '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>'
# 'text' - text of tweet, str, 144 chars


# look at tweets w/ place field

# Seems like tweepy's geo search is an or not an AND so the geo tweets (and maybe the loc) are not-necessarily trump/state relates smh

tweets_w_place = or_covid.find({'$and': [{'lang': {'$eq':'en'}}, {'place': {'$ne':None}}]})
count = 0
for tweet in tweets_w_place:
    count += 1
    if count == 1:
        with open()
        pprint.pprint(tweet)

print(tweets_w_place.count())

