# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/Users/matthowes/.spyder2/.temp.py
"""
import re
import sys
import csv
import json 
import os 
import pandas as pd
import time
import pytz, datetime
from TwitterSearch import *
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream  
import pytz 
from datetime import datetime
from time import gmtime, strftime
from datetime import datetime
from dateutil import tz




latitude = 47.6349926    # geographical centre of search
longitude = -122.3629609     # geographical centre of search
max_range = 10            # search range in kilometres
search_keyword = ''
tweets_within_initial_criteria = 0;  # criteria is geography and terms 

regexp = re.compile('hiring|position|job|Job')   # filter out the query on this term 
min_num_followers = 90 
tweets_within_secondary_criteria = 0; #criteria is number of followers 





outfile = "output.csv"   # this is where we output the file 





twitter = Twitter(auth = OAuth(access_token_key, access_token_secret, consumer_key,consumer_secret))

df = pd.DataFrame()

last_id = None

    #-----------------------------------------------------------------------
    # perform a search based on latitude and longitude
    # twitter API docs: https://dev.twitter.com/docs/api/1/get/search
    #-----------------------------------------------------------------------
query = twitter.search.tweets(q = search_keyword, geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), since=strftime("%Y-%m-%d"), count = 100)
    
for result in query["statuses"]:
    #-----------------------------------------------------------------------
    # only process a result if it has a geolocation
    #-----------------------------------------------------------------------
    
    if result["geo"]:
        tweets_within_initial_criteria += 1
        screen_name = result["user"]["screen_name"].encode("ascii")
        text = result["text"]
        #time_val = .encode("ascii")           
        #ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(,'%a %b %d %H:%M:%S +0000 %Y'))
        utc_created = result["created_at"].encode("ascii")    
        utc_created_at = datetime.strptime (utc_created ,'%a %b %d %H:%M:%S +0000 %Y')
        utc_time_zone = pytz.utc
        loc_dt = utc_time_zone.localize(utc_created_at)
        pacific =  timezone('America/Los_Angeles')
        pst_created_at = loc_dt.astimezone(pacific).strftime('%Y-%m-%d %H:%M:%S')
        loc_dt = loc_dt.strftime('%Y-%m-%d %H:%M:%S')
                    
        num_followers = result["user"]["followers_count"]
        text = text.encode('ascii', 'replace')
        latitude = result["geo"]["coordinates"][0]
        longitude = result["geo"]["coordinates"][1]
        #num_followers = result["followers_count"]
        # now write this row to our CSV file
        if num_followers > min_num_followers and regexp.search(text) is None and  regexp.search(screen_name) is None :
           tweets_within_secondary_criteria +=1
           df = df.append({'utc_time': loc_dt, 'pst_time':  pst_created_at, 'screenname':screen_name, 'text':text, 'latitude':latitude, 'longitude':longitude  }, ignore_index=True)
                

df.sort(['pst_time'], ascending=False, inplace=True)


    #-----------------------------------------------------------------------
    # let the user know where we're up to
    #-----------------------------------------------------------------------
print " "
print "Tweets within Geo area with targeted keyword: "  +  str(tweets_within_initial_criteria)
print "Tweets with required num of followers: " + str( tweets_within_secondary_criteria )  
print ""
for i in range(len(df)):
    print df['screenname'][i]
    print df['pst_time'][i]  
    print df['utc_time'][i]  
    print df['text'][i]
    print " "
#-----------------------------------------------------------------------
# we're all finished, clean up and go home.
#-----------------------------------------------------------------------
