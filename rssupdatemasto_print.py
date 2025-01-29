#!/usr/bin/env python3

# rssupdatemasto_print
# v0.0.1 for Python 3

# Import RSS feed parser module:
import feedparser

# Import requests module
import requests

# Get RSS feed source from files and then the content from the Internet:
rssfile = open("rsssource.txt", "r")
rsssource = rssfile.read()
rsssource = rsssource.strip()
feed_title = rsssource
# The 'requests...headers=' was added because Reddit requires headers.
d = feedparser.parse(requests.get(feed_title, headers={'User-Agent': 'Mozilla/5.0'}).content)

print(d)