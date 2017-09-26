from twitter import *
import re
import threading
import time
import json
import sys
from kafka.producer import KafkaProducer


config = {'access_key': '824366116042477568-D7RAYXsXDlZtLHwsF9rnlxnYmslqs2n',
          'access_secret': 'vr1b9hmkDAnNCIMqaiLJXEb4uclTIdEk7BZdqZi4raRPb',
          'consumer_key': 'sLIwSWJi9AFXgwM0TuNMSPeC1',
          'consumer_secret': 'AXcXpiocAbW07us9PmjKDNTCBxjpPD8kVEN8nvofgVVQIQRQhE'}



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

producer = KafkaProducer(bootstrap_servers='13.57.46.231:9092') 

for tweet in tweet_iter:
    print (tweet)
    producer.send('insight_topic', json.dumps(tweet))
    
