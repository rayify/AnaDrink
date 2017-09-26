from __future__ import print_function
import sys
import json
import time
import threading

from twitter import *
from pyspark import SparkContext
from pyspark.streaming import StreamingContext  
from pyspark.streaming.kafka import KafkaUtils
from cassandra.cluster import Cluster

coffee = ['coffee', 'cappuccino', 'espresso', 'frappuccino', 'mocha']
tea = ['tea', 'matcha', 'chai', 'oolong', 'pu-erh', 'tisane']
milk = ['milk', 'dairy', 'half-and-half']
soda = ['soda', 'coke', 'cola', 'fanta', 'sprite', 'pepsi', 'dr pepper', 'soft drink']
juice = ['juice', 'oj', 'cider']
wine = ['wine', 'riesling', 'merlot', 'syrah', 'chardonnay', 'sauvignon', 'pinot noir']
beer = ['beer', 'brew', 'amber', 'ipa', 'bud light', 'budweiser', 'miller lite', 'corona extra', 'heineken']
liquor = ['liquor', 'sake', 'shochu', 'whisky', 'tequila', 'gin', 'cognac', 'rum']


def check_drink(text):
    for c in coffee:
        if c in text:
            return 'coffee'
    for t in tea:
        if t in text:
            return 'tea'
    for m in milk:
        if m in text:
            return 'milk'
    for s in soda:
        if s in text:
            return 'soda'
    for j in juice:
        if j in text:
            return 'juice'
    for w in wine:
        if w in text:
            return 'wine'
    for b in beer:
        if b in text:
            return 'beer'
    for l in liquor:
        if l in text:
            return 'liquor'
    return ' '


def extract_data(json_body):
    json_body = json.loads(json_body)
    try:
        tweet_id = json_body['id_str']
        tweet_timestamp = json_body['created_at']
        tweet_text = json_body['text'].encode('utf-8')
        
        tweet_drink = check_drink(tweet_text)          
        if (tweet_drink == ' ') and ('quoted_status' in json_body):
            tweet_drink = check_drink(json_body['quoted_status']['text'])
          
        tweet_location = json_body['favorite_count']
        tweet_favorite = json_body['favorite_count']
        tweet_retweet = json_body['retweet_count']
        tweet_reply = json_body['reply_count']
        tweet_user_id = json_body['user']['id_str']
        tweet_user_followers = json_body['user']['followers_count']
        tweet_user_friends = json_body['user']['friends_count']
        
        tweet_user_location = 'None'
        if ('location' in json_body['user']):
            tweet_user_location = json_body['user']['location']
            
        print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    except:
        print ("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        return None
    data = {'id': tweet_id,
            'drink': tweet_drink,
            'timestamp': tweet_timestamp,
            'text': tweet_text,
            'favorite': tweet_favorite,
            'retweet': tweet_retweet,
            'reply': tweet_reply,
            'user_id': tweet_user_id,
            'user_followers': tweet_user_followers,
            'user_friends': tweet_user_friends,
            'user_location': tweet_user_location
           }
    return data
        
    
cassandra_master = "ec2-13-57-46-231.us-west-1.compute.amazonaws.com"
brokers = "ec2-13-57-46-231.us-west-1.compute.amazonaws.com:9092"
topics = "insight_topic"
keyspace = 'playground'

cluster = Cluster([cassandra_master])
session = cluster.connect(keyspace)
create_table = session.prepare("CREATE TABLE IF NOT EXISTS insight (id text PRIMARY KEY, drink text, timestamp text, tweet text, favorite int, retweet int, reply int, user_id text, user_followers int, user_friends int, user_location text);")
session.execute(create_table)
to_cassandra = session.prepare("INSERT INTO insight (id, drink, timestamp, tweet, favorite, retweet, reply, user_id, user_followers, user_friends, user_location) VALUES (?,?,?,?,?,?,?,?,?,?,?)")


def process(time, rdd):
    global i
    num_of_record=rdd.count()
    if num_of_record==0:
        return
    lines = rdd.map(lambda x : x[1])
    
    for x in lines.collect():
        tweet = extract_data(x)
        if (tweet['drink']==' '):
            continue
        session.execute(to_cassandra,(tweet['id'], tweet['drink'], tweet['timestamp'], tweet['text'], tweet['favorite'], tweet['retweet'], tweet['reply'], tweet['user_id'], tweet['user_followers'], tweet['user_friends'], tweet['user_location']))

sc = SparkContext(appName="InsightDrink")
ssc = StreamingContext(sc,10)

#get stream data from kafka
kafkaStream = KafkaUtils.createDirectStream(ssc, [topics], {"metadata.broker.list": brokers})


kafkaStream.foreachRDD(process) 
ssc.start()
ssc.awaitTermination()

