#!/usr/bin/env python3

# rssupdatemasto
# v0.1.5 for Python 3

# Import RSS feed parser module:
import feedparser

# Import requests module
import requests

# Import date parser, parse:
import dateutil.parser

# Import JSON module:
import json

# Import os, used to check if files exist:
import os

# Import Mastodon Python library for interacting with Mastodon:
from mastodon import Mastodon

# Get RSS feed source from files and then the content from the Internet:
# rsssource is the feed address, hashtags is the second line of the file
with open('rsssource.txt') as rssfile:
    lines = [line.rstrip('\n') for line in rssfile]
rsssource = lines[0]
hashtags = lines[1]
feed_title = rsssource
# The 'requests...headers=' was added because Reddit requires headers.
d = feedparser.parse(requests.get(feed_title, headers={'User-Agent': 'Mozilla/5.0'}).content)
# Extract the most recent feed post's title, link & published date:
p_title = d.entries[0].title
p_link = d.entries[0].link
p_publish = d.entries[0].published

p_latest = p_publish

# Create a list of title, link & published date:
p_list = []
p_list.append(p_title)
p_list.append(p_link)
p_list.append(p_publish)

# Save the latest post to a file, as JSON:
with open('rssupdatemasto_new.txt', 'w') as newfile:  
	json.dump(p_list, newfile)

# Does an 'rssupdatemasto_base.txt' file already exist, i.e. has this program run before?
# If not, create the file with its only contents as the most recent post date;
if not os.path.exists('rssupdatemasto_base.txt'):
	basefile_w = open('rssupdatemasto_base.txt', 'w')
	basefile_w.write(p_publish)
	basefile_w.close()
	p_last = p_publish

# If yes, read its contents: 	
if os.path.exists('rssupdatemasto_base.txt'):
	basefile_r = open('rssupdatemasto_base.txt', 'r') 
	p_last = basefile_r.read()
	basefile_r.close()

# Compare the post dates, if new > base, compile message & save latest over base:
p_last = dateutil.parser.parse(p_last)
p_latest = dateutil.parser.parse(p_latest)
masto_message = ''
if p_latest > p_last:
	masto_message = 'My new Reddit post:\n' + p_title + '\n' + p_link + '\n' + '\n' + hashtags
	basefile_w = open('rssupdatemasto_base.txt', 'w')
	basefile_w.write(p_publish)
	basefile_w.close()

# If a new feed post exists:
if masto_message != '':
	# Setup Mastodon authorisation:
	tokenfile = open("masto_app_token.txt", "r")
	token = tokenfile.read()
	token = token.strip()
	instancefile = open("masto_instance.txt", "r")
	instance = instancefile.read()
	instance = instance.strip()
	# Create an instance of the Mastodon class:
	mastodon = Mastodon(access_token = token, api_base_url = instance)
	# Create a public post using the text from masto_message:
	mastodon.status_post(masto_message)