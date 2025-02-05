<img src="rssupdatemasto_logo.jpg" height="96" alt="rssupdatemasto RSS feed updates post to Mastodon."> <br>

# What is 'rssupdatemasto'?
A Python 3 application to post to Mastodon when *a single* RSS feed is updated.

The application is currently being tested on my Mac. Whilst it can run standalone it's more likely to be useful when run automatically and periodically as a cron job on a server or at a dedicated web host.

### This repository structure:
If you want to know more, the most important things to look at here are:
* The [CHANGELOG.](CHANGELOG.md)
* The **[rssupdatemasto.py](rssupdatemasto.py)** app. The comments within the code may be more useful than the documentation.
* This README file.

### Prerequisites:
* A Mastodon account.
* Having the latest version of Python at least installed and available will help a lot when you're using this. The Apple system version will not run some of the modules it needs.
* I had to install the Mastodon module, so: `pip3 install mastodon.py`.
* My Python also did not have the feedparser module, so: `pip3 install feedparser`.

### Setup at your instance:
* A new 'application' must be created at your instance for your Python script - created whilst signed in. Go to `https://YourInstanceName/settings/applications/` and press the 'New application' button. Take educated guesses based on reading the help found elsewhere. You only need two Scopes checked: `write:statuses` and *(maybe!)* `profile`.

### The configuration files you must create:
* **`masto_app_token.txt`** - a file containing the Mastodon application token obtained from above. It must be only one line. **This token MUST remain secret from others**. (It is read from a separate file to give some portability to the code). An example of how it might look:
```
   y0UWilllik3pLay1ngW1ththiSApporIt6Iv3sjOyus
```
* **`masto_instance.txt`** - a file containing the Mastodon instance address to post to - only one line. An example:
```
   https://mastodon.social/
```
* **`rsssource.txt`** - a file containing only the RSS feed address on one line. An example:
```
   https://reddit.com/user/{username}/submitted/.rss
```
* **`hashtags.txt`** - a file containing a Python dictionary of subreddit name and hashtags to post. It is important to use double quotes and the exact letter case from the subreddit name. Within the raw RSS data returned from Reddit are data `term="subreddit" label="r/subreddit"`. Use the `term` value as the key in the file you create. An example:    
For posts in r/Browns, `term="Browns" label="r/Browns"`, so use `"Browns"`.
```
   {"Browns": "#NFL #Browns",
    "FuckModell": "#NFL #Browns #History",
    "spacebrowns": "#NFL #Browns"}
```
Note: I *chose* to use this method of displaying the data within the `hashtags` file. Using an `.ini` with `configparser` one must make the values lower case throughout - configparser converts the key's text to lower case, thus never matching the `term` value.

### Files the script creates:
The code itself creates 2 more files, both of which can be safely removed *while testing*, but which are necessary to create and retain a history:
* `rssupdatemasto_new.txt` - the title, URL and posting date of the latest RSS post.
* `rssupdatemasto_base.txt` - the most recent post date, which must be retained to check if any later posts appear.

### Automating it:
* To periodically run the script I created a 'cron job' by making a 'crontab' file on my always-on Mac. It should run every 3 hours starting at midnight. To create and amend it I started with and continue to use the vi editor, which is an experience in itself. Anyway, here it is:    
`0 */3 * * * cd ~/coding/rssupdatemasto/rssupdatemasto; python3 rssupdatemasto.py`
* I found that on a Mac one has to add cron to the list of 'Full disk access apps' - [Crontab Operation not permitted](https://apple.stackexchange.com/questions/378553/crontab-operation-not-permitted/378558#378558) (*StackExchange*).

### The other script in the repository:
* [postmastodon.py](postmastodon.py) - a short script to accept an input and post it to Mastodon.

### An example .gitignore if using a remote public repository:
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

---- 

### An aside:
Each time I ran the code the following warning appeared:

```
/Users/user/Library/Python/3.9/lib/python/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
```

I did some digging and it appears that it's a known issue - urllib3 does not play nicely with the Python supplied by Apple - a GitHub issue here: [urllib3>=2.0 does not work with system Python on macOS](https://github.com/urllib3/urllib3/issues/3020) (*GitHub*).

Well, I successfully installed Python 3.13.1 from here and the error goes away: https://www.python.org/downloads/
