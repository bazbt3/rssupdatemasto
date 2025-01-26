#!/usr/bin/env python3

# Import the Mastodon module:
from mastodon import Mastodon

# Type something to post to the network
masto_message = input("Type something memorable: ")

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