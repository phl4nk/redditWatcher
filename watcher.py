#!/usr/bin/python
# Manditory ASCII Logo
#
# Author: phl4nk
# Date: 07/12/2018
# Version: 0.0.1

import urllib2,re,ast

online_regex = 's1wbv0ui-12 ffQWxW">([^<]*)<\/p>'

def grab_subreddit(subreddit):
    try:
        request_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}
        request = urllib2.Request("https://www.reddit.com/r/"+subreddit, headers=request_headers)
        contents = urllib2.urlopen(request).read()
        return contents
    except Exception, e:
        print "[!] Crawling failed:", e
        return None

def get_online(html_data):
    try:
        regex=re.compile(online_regex)
        return value_to_int(regex.findall(html_data)[0]);
    except Exception, e:
        print 'Cannot find view count from response'

# Custom function to turn strings into ints
# https://stackoverflow.com/questions/39684548/convert-the-string-2-90k-to-2900-or-5-2m-to-5200000-in-pandas-dataframe
# There is a legit reason to do int(float()) - edge case: '1.2k'
def value_to_int(x):
    try:
        return int(float(x))
    except ValueError:
        if 'k' in x:
            if len(x) > 1:
                return int(float(x.replace('k', '')) * 1000)
        if 'm' in x:
            if len(x) > 1:
                return int(float(x.replace('m', '')) * 1000000)
        return 0

#print value_to_int('1.2k')
#print get_online(grab_subreddit("netsec"))
#print get_online(grab_subreddit("conspiracy"))
#print get_online(grab_subreddit("gif"))
#print get_online(grab_subreddit("redteam"))
