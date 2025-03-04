#!/usr/bin/env python3

# rssupdatemasto
# v0.4.6 for Python 3

# Import modules:
import feedparser
import requests
import dateutil.parser
import datetime
import json
import os
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

# Get RSS feed sources from a file and then the content from the Internet:
# Sequentially read a multiple-line 'rsssource.txt' file - the list of feed sources:
# Process whatever is found according to the RSS parameter names, per feed title and per post:
with open('rsssource.txt') as sources:
    for line in sources:
        feed_title = line.strip('[]').strip()

        # The 'requests...headers=' was added because Reddit requires headers:
        d = feedparser.parse(requests.get(feed_title, headers={'User-Agent': 'Mozilla/5.0'}).content)
        # Extract the most recent post's title, link published date and description:
        p_title = d.entries[0].title
        p_link = d.entries[0].link
        p_publish = d.entries[0].published
        p_description = d.entries[0].description

        # Extract the feed title:
        try:
            p_feed = d.feed.title
        except AttributeError as error:
           p_feed = ""

        # Extract the subreddit name:
        p_term = d.entries[0].tags[0].term

        # If the feed is not 'saved by bazbt3' or 'submitted by bazbt3' add a 'n' character summary of the post text:
        # This does not attempt to strip out any html starting within the first 'n':
        # Try 2 of my Reddit feeds first and remove the post descriptions:
        # (Hardcoding the tests for posts created by me are not ideal, but allow for adding 'My new post:' & ' to Reddit'):
        # Saved by me *from* Reddit:
        if p_feed == 'saved by bazbt3':
            p_description = ""
            p_header = "A post " + p_feed + " from Reddit:"
        # Submitted by me *to* Reddit:
        elif p_feed == 'submitted by bazbt3':
            p_description = ""
            p_header = "My new post (" + p_feed + " to Reddit):"
        # Add the post description to what's left, i.e. likely to be a blog post by me:
        # In this case 'n' = 200 characters:
        else:
            p_description = p_description[:200] + "..."
            p_header = "My new post at " + p_feed + ":"
            p_title = p_title + '\n\n' + p_description

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
        # And if the previous 2 fail, trap the error and do not add hashtags:
        except KeyError as error:
            hashtags = ""

        # Store the date & time the most recent post was published:
        p_latest = p_publish

        # Does an 'rssupdatemasto_base.txt' file already exist, i.e. has this script run before?
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

        # Compare the post dates. If latest > last, compile a post, set the posted flag to True:
        p_last = dateutil.parser.parse(p_last)
        p_latest = dateutil.parser.parse(p_latest)
        masto_message = ''
        if p_latest > p_last:
            masto_message = p_header + '\n\n' + p_title + '\n\n' + p_link + hashtags

        # If a new feed post exists then create a public post using the text from masto_message:
        if masto_message != '':
            mastodon.status_post(masto_message)

# Finally save the current date over the previous in 'rssupdatemasto_base.txt':
now = datetime.datetime.now(datetime.timezone.utc)
now_formatted = now.strftime('%a, %d %b %Y %H:%M:%S %z')
basefile_w = open('rssupdatemasto_base.txt', 'w')
basefile_w.write(now_formatted)
basefile_w.close()