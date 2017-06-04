# Import  dependencies
import time
import json
import tweepy
import urllib2
import feedparser
from fake_useragent import UserAgent
from datetime import datetime, timedelta
from credentials import *

print("Loading Configuration Files...")

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Access and authorize Twitter credentials
consumer_key = data["twitterAccessKeys"][0]["consumer_key"]
consumer_secret = data["twitterAccessKeys"][1]["consumer_secret"]
access_token = data["twitterAccessKeys"][2]["access_token"]
access_token_secret = data["twitterAccessKeys"][3]["access_token_secret"]

print("\033[33m[INFO]\033[0m Your Consumer Key is " + consumer_key)
print("\033[33m[INFO]\033[0m Your Consumer Secret Key is " + consumer_secret)
print("\033[33m[INFO]\033[0m Your Access Token is " + access_token)
print("\033[33m[INFO]\033[0m Your Access Token Secret is " + access_token_secret)

time.sleep(3)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Date parsing function
def dt_parse(t):
	ret = datetime.strptime(t[0:16],'%Y-%m-%dT%H:%M')
	if t[19]=='-':
		ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
	elif t[19]=='+':
		ret+=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
	return ret

# Establish user agent
ua = UserAgent()

# Set initial time
testTime = dt_parse(datetime.utcnow().isoformat())

link = data['link'][0]['baseLink']

# Run Shopify website scrubber
response = urllib2.urlopen(link + 'products.json')
data2 = json.load(response)

while True:

    print("\033[33m" + str(testTime) + "! \033[0m")

    for item in data2['products']:   # Python's for loops are a "for each" loop
        if (str(dt_parse(item['updated_at'])) > str(testTime)):
            print('\033[1;36m[LOG]\033[0m ' + item['title'] + '  ' + link + item['handle'] + '  ' + item['updated_at'])
            api.update_status(item['title'] + '  ' + link + 'products/' + item['handle'] + '  ' + str(dt_parse(item['updated_at'])))

    print("\033[1;36m[LOG]\033[0m Checking Site! " + link)
    print("\033[1;36m[LOG]\033[0m Site Checked! Status Code: " + str(response.code) + "!")
    testTime = dt_parse(datetime.utcnow().isoformat())
    time.sleep(5)
