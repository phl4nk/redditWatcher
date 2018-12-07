#!/usr/bin/python
#
#  ReddiTWatch3r
#      ___
#    [|   |=|{)__
#     |___| \/   )
#      /|\      /|
#     / | \    | \
#
# Author: phl4nk
# Date: 07/12/2018
# Version: 0.0.7

import urllib2,re,datetime,time

class_regex = 's1wbv0ui-12 ffQWxW">([^<]*)<\/p>'
request_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}

# pull HTML from subreddit
def grab_subreddit(subreddit):
    try:
        print '[+] Crawling subreddit'
        request = urllib2.Request("https://www.reddit.com/r/"+subreddit, headers=request_headers)
        contents = urllib2.urlopen(request).read()
        return contents
    except Exception, e:
        print "[!] Crawling failed:", e
        return None

# parse total amount of subscribers, and currently online
# should return a list of subs,curr_online
def get_stats(html_data):
    try:
        regex=re.compile(class_regex)
        counts = regex.findall(html_data)
        total_subs = str(value_to_int(counts[0]))
        curr_online = str(value_to_int(counts[1]))
        return [total_subs,curr_online]
    except Exception, e:
        print '[!] Something went wrong',e

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

# save to CSV format for ease of ingest/graphing later
# data should be a list with 2 items
def save_data(data,filename):
    try:
        t = datetime.datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        f = open(filename+'.txt','a')
        f.write(t+','+data[0]+','+data[1]+'\n')
        print '[+] Written data to file:', data
        f.close()
    except Exception, e:
        #flailing
        print '[!] Nope, not writing this one to disk...'

def watch(subreddit):
    data = grab_subreddit(subreddit)
    output = get_stats(data)
    save_data(output,subreddit)

while True:
    watch('netsec')
    time.sleep(5)
