import tweepy
import requests
import json
import sys
import time
import random

# Tweet auth

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


fb_url = "https://{yourfirebaseappname}.firebaseio.com/tweets.json"

#check for tweet in data

def check_tweet(tweet):
    try:
        r = requests.get(fb_url)
        r = r.json()
        for i in r:
            if tweet.id == r[i]["id"]:
                return False
   #error handle
    except KeyboardInterrupt:
        sys.exit("KeyboardInterrupt")
    except Exception as e:
        print(e)
        pass
    finally:
        return True



# check for tweet dupli
def search(tag):
    try:
        c = tweepy.Cursor(api.search, q=tag)
        print("Searching "+tag)
        i = 0
        for tweet in c.items():
            if i < 1 and tweet.retweet_count > 20:
                if check_tweet(tweet):
                    api.retweet(tweet.id)
                    db_tweet = {"id": tweet.id}
                    requests.post(fb_url, json.dumps(db_tweet))
                    i += 1
                    break
    except KeyboardInterrupt:
        sys.exit("KeyboardInterrupt")
    except Exception as e:
        print(e)
        pass

# specify hastags
while True:
    tags = ["#PUBG", "#CSGO", "#firebase", "#tweepy" , "#IND"]
    search(random.choice(tags))
        time.sleep(60)
