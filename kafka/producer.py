from twitter import *
import re
import threading
import time
import json
import sys
from kafka.producer import KafkaProducer


config = {'access_key': 'your_access_key_here',
          'access_secret': 'your_access_secret_key_here',
          'consumer_key': 'your_consumer_key_here',
          'consumer_secret': 'your_consumer_secret_key_here'}



auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"])
stream = TwitterStream(domain='userstream.twitter.com', auth = auth, secure = True)


search_term = "coffee, cappuccino, espresso, frappuccino, mocha, \
               tea, matcha, chai, oolong, pu-erh, tisane, \
               milk, dairy, half-and-half, \
               soda, coke, cola, fanta, sprite, pepsi, Dr pepper, soft drink, \
               juice, oj, cider, \
               wine, riesling, merlot, syrah, chardonnay, sauvignon, pinot noir, \
               beer, brew, amber, ipa, bud light, budweiser, miller lite, corona extra, heineken, \
               liquor, sake, shochu, whisky, tequila, gin, cognac, rum"
tweet_iter = stream.statuses.filter(track = search_term, language = 'en')

producer = KafkaProducer(bootstrap_servers='your_aws_cluster_public_IP:9092') 

for tweet in tweet_iter:
    print (tweet)
    producer.send('insight_topic', json.dumps(tweet))
    
