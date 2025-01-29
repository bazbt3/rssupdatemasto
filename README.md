<img src="rssupdatemasto_logo.jpg" height="96" alt="rssupdatemasto RSS feed updates post to Mastodon."> <br>

# What is 'rssupdatemasto'?
A Python 3 application to post notifications to Mastodon when *a single* RSS feed is updated.

Application is currently being tested on my Mac. Whilst it can run standalone it's more likely to be useful when run automatically and periodically as a cron job on a server or at a dedicated web host.

### Prerequisites:
* A Mastodon account.
* Having the latest version of Python at least installed and available will help a lot when you're using this. The Apple system version will not run some of the modules it needs.
* I had to install the Mastodon module, so: `pip3 install mastodon.py`.
* My Python also did not have the feedparser module, so: `pip3 install feedparser`.

### Setup at your instance, and the configuration files you must create:
* A new 'application' must be created at your instance for your Python script - created whilst signed in. Go to `https://YourInstanceName/settings/applications/` and press the 'New application' button. Take educated guesses based on reading the help found elsewhere. You only need two Scopes checked: `write:statuses` and *(maybe!)* `profile`.
* `masto_app_token.txt` - a file containing the Mastodon application token - only one line. **This token MUST remain secret from others**. (It is read from a separate file to give some portability to the code).
* `masto_instance.txt` - a file containing the Mastodon instance address to post to - only one line.
* `rsssource.txt` - a file containing only the RSS feed address - only one line.

### Files the script creates:
The code itself creates 2 more files, both of which can be safely removed *while testing*, but which are necessary to create and retain a history:
* `rssupdatemasto_new.txt` - the title, URL and posting date of the latest RSS post.
* `rssupdatemasto_base.txt` - the most recent post date, which must be retained to check if any later posts appear.

### Automating it:
* To periodically run the script I created a 'cron job' by making a 'crontab' file on my always-on Mac. It should run every 3 hours starting at midnight. To create it I had to use the vi editor which was an experience in itself. Anyway, here it is:    
`0 0,3,6,9,12,15,18,21 * * * cd ~/coding/rssupdatemasto/rssupdatemasto; python3 rssupdatemasto.py`
* I found that on a Mac one has to add cron to the list of 'Full disk access apps' - [Crontab Operation not permitted](https://apple.stackexchange.com/questions/378553/crontab-operation-not-permitted/378558#378558) (*StackExchange*).

### The 2 other scripts in the repository:
* postmastodon.py - a short script to accept an input and post it to Mastodon.
* rssupdatemasto_print.py - a short script to print to the screen the 'raw' text extracted from the RSS feed.

---- 

### An aside:
Each time I ran the code the following warning appeared:

```
/Users/user/Library/Python/3.9/lib/python/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
```

I did some digging and it appears that it's a known issue - urllib3 does not play nicely with the Python supplied by Apple - a GitHub issue here: [urllib3>=2.0 does not work with system Python on macOS](https://github.com/urllib3/urllib3/issues/3020) (*GitHub*).

Well, I successfully installed Python 3.13.1 from here and the error goes away: https://www.python.org/downloads/
