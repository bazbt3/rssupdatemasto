# rssupdatemasto

## Changelog
(most recent first)

### v0.4.1 2025-02-22:
* Added my Reddit *private* saved posts feed, checked by `'submitted by bazbt3' or 'saved by bazbt3'`.
* Tidied the layout of some code and comments without altering function or order.

### v0.4.0 2025-02-21:
* Added summary to non-Reddit posts. The creation of the summary (description) is currently at lines 58 to 67 and is hardcoded to omit a summary when 'submitted by bazbt3'. It would be preferable to use the source's site instead.

### v0.3.4 2025-02-21:
* Added feed title to post.
* Removed more redundant, commented-out code.

### v0.3.3 2025-02-20:
* Move the code to save the most recent post date outside the main loop - still comparing dates.

### v0.3.2 2025-02-18:
* Remove the commented-out now-redundant code related to the single feed source.

### v0.3.1 2025-02-18:
* Fixed: now adds hashtags to sources other than Reddit. (Tested only with my blog feed).

### v0.3.0 2025-02-15:
* Added the ability to check more than the original single RSS source - the `rsssource.txt` file can now have multiple lines.
* The previous code is currently commented out.
* The `rssupdatemasto_new` file is now redundant.
* Note: though it works, the code may not correctly check all sources due to the `rssupdatemasto_base` test working only on the most recent post found. It might be better to move writing the date to file outside the main loop - one everything is processed.

### v0.2.9 2025-02-15:
* Tidied comments and some code; no functional changes.

### v0.2.8 2025-02-010:
* Moved the Mastodon authorisation code from the post creation section at the end.

### v0.2.7 2025-02-08:
* Removed `import configparser` as redundant.

### v0.2.6 2025-02-08:
* Trapped an exception when finding the title of a non-Reddit feed.
* Needs work to find the variable used - checking if there is a standard.

### v0.2.5 2025-02-08:
* Added the feed title `p_feed = d.feed.title` in preparation for future expansion.
* Small code comment updates.

### v0.2.4 2025-02-05:
* Renamed `hashtags.ini` to `hashtags.txt`.

### v0.2.3 2025-02-04:
* Moved the formatting of the break between the hashtags and the text & URL into the hashtag variable definition.

### v0.2.2 2025-02-03:
* Converted `hashtags.ini` from a configparser .ini file to a Python .dict. The automatic conversion of configparser .ini file key names was too big a problem for me to want to solve.

### v0.2.1 2025-02-03:
* Convert `p_term` to lower case to be compatible with the configparser .ini keys.

### v0.2.0 2025-02-03:
* Added a `hashtags.ini` file containing subreddit-hashtag key pairs, and the code to load it into a dictionary, checked automatically to add hashtags to posts based on the subreddit name - the `p_term` variable.
* Removed the now redundant second line from `rsssource.txt` - it previously held a limiting range of hashtags.

### v0.1.6 2025-02-02:
* Added `p_term = d.entries[0].tags[0].term` to extract the subreddit name - in preparation for automatically adding or excluding hashtags based on the feed's source.

### v0.1.5 2025-02-01:
* The rsssource.txt file now has 2 lines: the feed address and the hashtags to post.
* The code doesn't account for a file with a single line or an empty line.

### v0.1.4 2025-01-28:
* Manually reverted to the v0.1.2 code - the hashtags are there after all. D'oh!

### v0.1.3 2025-01-28:
* Trying to fix the non-display of the hashtags, removed a newline from the post output and changed the quote type from '#NFL #Browns' to "#NFL #Browns".

### v0.1.2 2025-01-27:
* Removed print of feed text added when run during debugging.
* Added partial explanation of reason for use of `requests`.

### v0.1.1 2025-01-27:
* Removed the date completely from the post.
* Added '\#NFL' & '\#Browns' tags for visibility.

### v0.1.0 2025-01-26:
* A first release prior to committing to a new GitHub repo.
* None of the preceding iterations have been version managed in git, none backed up anywhere yet.
* Must be careful to not upload the configuration and working files, **especially the access token**.

### v0.0.7 2025-01-26:
* Fixed after  number of errors I found whist debugging - using the time-honoured principle of selectively printing(my variables).
* I found the answer eventually in post ['feedparser - no entries](https://www.reddit.com/r/learnpython/comments/fo42bg/feedparser_no_entries/) in the r/learnpython subreddit:
 * The Reddit server rejects poorly-formed request headers with 'bozo' within the 301 message it returns. To get around it, add *nicely*-formed headers. Simple!
* So, the post reaches Mastodon, albeit with a date and time poorly-formatted for humans. But I must have originally intended it to be like that in the previous application or else I'd not have used it. (shrugs)

### v0.0.6 2025-01-25:
* Well, no error message this time. Which is nice. No toot either.

### v0.0.5 2025-01-25:
* It transpires that the warning when the script runs kills the Mastodon authentication.
* It's likely I messed up somewhere when coping the code from v0.0.1 - which posts.
* The positive takeaway is that the code underlying the feed generation works.
* Updated Python to 3.13.1 to hopefully clear the issue highlighted here: [urllib3>=2.0 does not work with system Python on macOS](https://github.com/urllib3/urllib3/issues/3020).

### v0.0.4 2025-01-25:
* A test to examine if the first live post will occur after deleting the files generated by the program, then running it again:
 * `rssupdatemasto_new.txt`
 * `rssupdatemasto_base.txt`

### v0.0.3 2025-01-25:
* Fixes the test for the existence of a new feed because it prohibits the reading of the app token and instance.

### v0.0.2 2025-01-25:
* Saved the earlier code as `postmastodon.py`
* Copies the feed parser & formatter app from my earlier rssupdatepnut script at:
 * `https://github.com/bazbt3/rssupdatepnut`

### v0.0.1 2025-01-25:
* Copies the basic instructions and code from [Creating a Mastodon Bot with Python](https://dev.to/tr11/creating-a-mastodon-bot-with-python-475b) by Tiago Rangel.
* Adds an input line used to post test text:
 * `masto_message = input("Type something memorable: ")`
* Adds the prerequisite of pulling from files the app token and instance it's intended to be used on.
