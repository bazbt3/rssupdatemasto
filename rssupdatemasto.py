#!/usr/bin/env python3

# rssupdatemasto
# v0.3.4 for Python 3

# Import RSS feed parser module:
import feedparser

# Import requests module:
import requests

# Import date parser, parse:
import dateutil.parser

# Import JSON module:
import json

# Import os, used to check if files exist:
import os

# Import Mastodon Python library for interacting with Mastodon:
from mastodon import Mastodon

# Setup Mastodon authorisation:
tokenfile = open("masto_app_token.txt", "r")
token = tokenfile.read()
token = token.strip()
instancefile = open("masto_instance.txt", "r")
instance = instancefile.read()
instance = instance.strip()
# Create an instance of the Mastodon class:
mastodon = Mastodon(access_token = token, api_base_url = instance)

# Get RSS feed source from files and then the content from the Internet:

# Sequentially read a multiple-line 'rsssource.txt' file - the list of feed sources - and process whatever is found according to the RSS parameter names per feed title and per post:
with open('rsssource.txt') as sources:
    for line in sources:
        feed_title = line.strip('[]').strip()

		# The 'requests...headers=' was added because Reddit requires headers:
        d = feedparser.parse(requests.get(feed_title, headers={'User-Agent': 'Mozilla/5.0'}).content)
        # Extract the most recent post's title, link & published date:
        p_title = d.entries[0].title
        p_link = d.entries[0].link
        p_publish = d.entries[0].published

        # Extract the feed title and subreddit name:
        # Feed title:
        try:
            p_feed = d.feed.title
        except AttributeError as error:
           p_feed = ""
        # Subreddit name:
        p_term = d.entries[0].tags[0].term

        # Read the hashtags from the 'hashtags.txt' file:
        with open('hashtags.txt') as h: 
            tags_str = h.read()
        # Convert the string to a JSON dict:
        tags_dict = json.loads(tags_str)

        # Check the source is one of those in the file, otherwise trap the resulting error of a missing key:
        # Format a successful match with 2 newlines to separate the tags from the taxt & address:
        try:
            # Try Reddit first:
            try:
                tags_dict[p_term]
                hashtags = "\n\n" + tags_dict[p_term]
            # Then try a different format (tested with my blog):
            except:
                tags_dict[p_feed]
                hashtags = "\n\n" + tags_dict[p_feed]
        # And if tg previous 2 fail, trap the error and do not add hashtags:
        except KeyError as error:
            hashtags = ""

        # Store the date & time the most recent post was published:
        p_latest = p_publish

        # Create a list of title, link & published date:
        p_list = []
        p_list.append(p_title)
        p_list.append(p_link)
        p_list.append(p_publish)

        # Does an 'rssupdatemasto_base.txt' file already exist, i.e. has this program run before?
        # If it does not, create the file with its only contents as the most recent post date:
        if not os.path.exists('rssupdatemasto_base.txt'):
            basefile_w = open('rssupdatemasto_base.txt', 'w')
            basefile_w.write(p_publish)
            basefile_w.close()
            p_last = p_publish

        # If 'rssupdatemasto_base.txt' does exist, read its contents:
        if os.path.exists('rssupdatemasto_base.txt'):
            basefile_r = open('rssupdatemasto_base.txt', 'r') 
            p_last = basefile_r.read()
            basefile_r.close()

        # Compare the post dates. If new > base, compile a post:
        p_last = dateutil.parser.parse(p_last)
        p_latest = dateutil.parser.parse(p_latest)
        masto_message = ''
        if p_latest > p_last:
            masto_message = 'My new post:\n' + p_feed + '\n' + p_title + '\n' + p_link + hashtags

        # If a new feed post exists:
        if masto_message != '':
            # Create a public post using the text from masto_message:
            mastodon.status_post(masto_message)

# Finally, check (may be redundant) and save the date of the latest post(s) over the previous in 'rssupdatemasto_base.txt':
if p_latest > p_last:
    basefile_w = open('rssupdatemasto_base.txt', 'w')
    basefile_w.write(p_publish)
    basefile_w.close()