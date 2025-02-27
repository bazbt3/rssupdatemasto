<img src="rssupdatemasto_logo.jpg" height="96" alt="rssupdatemasto RSS feed updates post to Mastodon."> <br>

# What is 'rssupdatemasto'?
A Python 3 application to post to Mastodon when nominated RSS feeds are updated.

The application is currently tested on my Mac. Whilst it can run standalone it's more likely to be useful when run automatically and periodically as a cron job on a server or at a dedicated web host.

### Calling it from the command line:
`python3 rssupdatemasto.py`.

### Prerequisites:
* A Mastodon account.
* Having the latest version of Python at least installed and available will help a lot when you're using this. The Apple system version will not run some of the modules it needs.
* I had to install the Mastodon module, so: `pip3 install mastodon.py`.
* My Python also did not have the feedparser module, so: `pip3 install feedparser`.

### Setup at your instance:
A new 'application' must be created at your instance for your Python script - created whilst signed in. Take educated guesses based on reading the help you can find elsewhere.
1. Go to `https://{YourInstanceName}/settings/applications/` and press the 'New application' button,
2. Give it a snappy application name,
3. If you have a web site you intend to document the app at, add its address.
4. I left the redirect URI untouched.
5. You probably only need 1 Scope checked: `write:statuses` (and *maybe!* `profile`).

### The configuration files you must create:
* **`masto_app_token.txt`** - a file containing the Mastodon application token obtained after creating your application. It must be only one line. **This token MUST remain secret from others**. (It is read from a separate file to give some portability to the code). An example of how it might look:
```
   y0UWilllik3pLay1ngW1ththiSAppForIt8r1n6sjOy
```
* **`masto_instance.txt`** - a file containing the Mastodon instance address to post to - only one line. An example:
```
   https://mastodon.social/
```
* **`rsssource.txt`** - a file containing one or more RSS feed, each with their address on a new line - an improvement on the single feed in the script prior to v0.3.0. An example:
```
   https://reddit.com/user/{username}/submitted/.rss
   https://{url.tld}/feed
```
* **`hashtags.txt`** - a file containing a Python dictionary of subreddit name and hashtags to post. It is important to use double quotes and the exact letter case from the subreddit name. Within the raw RSS data returned from Reddit are data `term="subreddit" label="r/subreddit"`. Use the `term` value as the key in the file you create. An example:    
For posts in r/Browns, `term="Browns" label="r/Browns"`, so use `"Browns"`.
```
   {"Browns": "#NFL #Browns",
    "FuckModell": "#NFL #Browns #History",
    "spacebrowns": "#NFL #Browns"}
```
Note: I *chose* to use this method of displaying the data within the `hashtags` file. (Do't bother using an `.ini` with `configparser` - configparser converts the key's text to lower case, thus never matching the `term` value for instance).

### Files the script creates:
The code itself creates one file, which can be safely removed *while testing*, but which is necessary to create and retain a history:
* `rssupdatemasto_base.txt` - the most recent post date, which must be retained to check if any later posts appear. If editing the date and time while testing, do not omit the time zone offset (e.g. `+0000`) - the script will fail with an error that comparing two different formats is not allowed.

### An example .gitignore file if saving this into a remote public repository:
```
# The files to ignore for this app
# The masto_app_token.txt file must not be made public, the rest won't cause issues.
masto_app_token.txt
masto_instance.txt
rsssource.txt
rssupdatemasto_base.txt
rssupdatemasto_new.txt
.DS_Store
```

### Automating it:
* To periodically run the script I created a 'cron job' by making a 'crontab' file on my always-on Mac. Mine runs every hour starting at midnight. To create and amend it I started with and continue to use the vi editor, which is an experience in itself. Anyway, here it is:    
`0 * * * * cd ~/coding/rssupdatemasto/rssupdatemasto; python3 rssupdatemasto.py`
* I found that on a Mac one has to add cron to the list of 'Full disk access apps' - [Crontab Operation not permitted](https://apple.stackexchange.com/questions/378553/crontab-operation-not-permitted/378558#378558) (*StackExchange*).

### The other script in the repository:
* [postmastodon.py](postmastodon.py) - a short script to accept an input and post it to Mastodon.

### More:
If you want to know more, look at the following:
* The [CHANGELOG.](CHANGELOG.md)
* The **[rssupdatemasto.py](rssupdatemasto.py)** script itself. The comments within the code may be more useful than the documentation.

---- 

### An aside:
Each time I ran the code the following warning appeared:

```
/Users/user/Library/Python/3.9/lib/python/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
```

I did some digging and it appears that it's a known issue - urllib3 does not play nicely with the Python supplied by Apple - a GitHub issue here: [urllib3>=2.0 does not work with system Python on macOS](https://github.com/urllib3/urllib3/issues/3020) (*GitHub*).

Well, I successfully installed Python 3.13.1 from here and the error goes away: https://www.python.org/downloads/
