<img src="rssupdatemasto_logo.jpg" height="96" alt="rssupdatemasto RSS feed updates post to Mastodon."> <br>

# What is 'rssupdatemasto'?
A Python 3 application to post notifications to Mastodon when *a single* RSS feed is updated.

Application is currently being tested on my Mac. Whilst it can run standalone it's more likely to be useful when run automatically and periodically as a cron job on a server or at a dedicated web host.

### Prerequisites:
* A Mastodon account.
* A Mastodon application token - **a token which MUST remain secret from others**, read from a separate file here to give some portability to the code:
 * `masto_app_token.txt`.
* A Mastodon instance address - read from a file again:
 * `masto_instance.txt`.
* A feed address - read from a file again:
 * `rsssource.txt`.
* Having the latest version of Python at least installed and available will help a lot when you're using this. The Apple version will not allow some of the modules it needs to run.
* The Mastodon libraries: `pip3 install mastodon.py`.
* The feedparser RSS, er… feed parser: `pip3 install feedparser`.

### The code itself creates 2 more files, both of which can be safely removed *while testing*, but which are necessary to retain a history:
* The title, URL and posting date of the latest post found online:
 * `rssupdatemasto_new.txt`.
* The most recent post date, retained to check if any later posts appear:
 * `rssupdatemasto_base.txt`.

Note: the code can be run with minor modifications to alert independently of a Mastodon account, but it's been years since I did any actual coding, sorry I can't help there.

Moreover, each time I run the code the following warning appears, one I've not worked out how to fix and certainly one for which I have not created an exception.

```
/Users/user/Library/Python/3.9/lib/python/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
```

Painful, isn't it.

OK, I did some digging and it appears that it's a known issue - urllib3 does not play nicely with the Python supplied by Apple - a GitHub issue here: [urllib3>=2.0 does not work with system Python on macOS](https://github.com/urllib3/urllib3/issues/3020).

Well, I've successfully installed Python 3.13.1 from here: https://www.python.org/downloads/
