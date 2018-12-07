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
# Version: 0.1.0

import urllib2,re,datetime,time

viewing_regex = 'currentlyViewingCount":(\d+),'
subs_regex = 'subscribersCount":(\d+),'
request_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}

# pull HTML from subreddit
def grab_subreddit(subreddit):
    try:
        request = urllib2.Request("https://www.reddit.com/r/"+subreddit, headers=request_headers)
        contents = urllib2.urlopen(request).read()
        return contents
    except Exception, e:
        print "[!] Crawling failed:", e
        return None

# parse total amount of subscribers, and currently online
# should return a list of total_subs,curr_viewing
def get_stats(html_data):
    try:
        Vregex = re.compile(viewing_regex)
        Sregex = re.compile(subs_regex)
        total_subs = str(Sregex.findall(html_data)[0])
        curr_viewing = str(Vregex.findall(html_data)[0])
        return [total_subs,curr_viewing]
    except Exception, e:
        print '[!] Something went wrong',e

# save to CSV format for ease of ingest/graphing later
# data should be a list with 2 items
def save_data(data,filename):
    try:
        t = datetime.datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        f = open(filename+'.csv','a')
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
    watch('news')
    time.sleep(30)
