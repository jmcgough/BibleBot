#! /usr/bin/python
"""
#/*****************************************************
#*****************************************************
#**
#** SOURCE NAME | BibleBot.py
#**             |
#**    SYNOPSIS | BibleBot.py
#**             |
#** DESCRIPTION | Sends back Bible verse as a reply for
#**             | Tweet/Message to it with hashtag #bverse
#**             |
#**     CHANGES | Programmer:         Date:       Reason/Comments
#**             | Jeffrey B. McGough  01-02-2016  Initial
#**             |
#**             |
#**       NOTES | This is a TwitterBot that looks for the
#**             | hashtag #bverse in Tweets and Messages sent
#**             | to it, and replies back with a Bible verse.
#**             | Working Example: @mcgoobot Send me a #bverse
#**             |
#**             | It requires tweepy, a Python Twitter API,
#**             | found here: http://www.tweepy.org/
#**             | It also needs Python Requests, I am not sure
#**             | if it is standard install or not:
#**             | http://docs.python-requests.org/en/latest/
#**             |
#****************************************************/
"""

import re
import requests
import sys
import tweepy

#
# This is where we get our account keys for Twitter
####
from TApiKeys import *

def authenticate():
    """Authenticate us to Twitter"""
    auth = tweepy.OAuthHandler(C_Key, C_Secret)
    auth.set_access_token(A_Token_Key, A_Token_Secret)
    return(tweepy.API(auth))

def getverse():
    """Get bible verse"""
    # I would rather have KJV, but this is the best API
    # I have found and it is ESV
    # Nice thing is we can just plug in a new API here...
    ####
    payload = {'key': 'IP', 'output-format': 'plain-text',  \
               'include-footnotes': 'false', \
               'include-verse-numbers': 'false', \
               'include-first-verse-numbers': 'false', \
               'include-passage-horizontal-lines': 'false', \
               'include-heading-horizontal-lines': 'false', \
               'include-headings': 'false', \
               'include-subheadings': 'false', \
               'line-length': '0', \
               'include-short-copyright': 'true'}
    bvurl = 'http://www.esvapi.org/v2/rest/verse'

    try:
        bv = requests.get(bvurl, params=payload)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout,
            RequestException):
        sys.exit(1)

    clean_verse = re.sub('\s+', ' ', bv.text)

    if re.search('\(ESV\)', clean_verse):
        return(clean_verse)
    else:
        clean = clean_verse + " (ESV)"
        return(clean)

def chunktext(text, tlength):
    """Return a list of strings in chunks of length"""
    # Kinda happy with this chunking function, it should probably
    # have more generic named varibles, and called more generic.
    # It chunks what ever text you input to at most the length you request.
    # Chunked at spaces, so as to not split words.
    ####
    wspace = re.compile("\s")
    chunks = list()
    txtlen = len(text)
    remainder = txtlen % tlength

    numberofchunks = txtlen / tlength

    if remainder > 0:
        numberofchunks += 1

    start = 0
    end = tlength

    # This is the work - We splice up text into chunks
    # we know the number of chunks needed, and if we use up
    # the remainder of the last chunk do to word breaks
    # we will add another chunk
    ####
    for chunk in range(numberofchunks):

        if wspace.match(text[end:]):
            chunks.insert(chunk, text[start:end])
            start = (end + 1) # This steps over the end space
            end = (start + tlength)

        else:
            for char in reversed(text[:end]):
                end -= 1

                if wspace.match(char):
                    chunks.insert(chunk, text[start:end])
                    start = (end + 1) # This steps over the end space
                    end = (start + tlength)

                    break

    if chunk == numberofchunks -1 and start < txtlen:
        chunks.append(text[start:])

    return(chunks)


def main():
    """For Stand Alone Invocation"""

    #
    # Read in the last since_id
    ####
    try:
        with open('/var/tmp/SinceID.txt', 'r') as idcount:
            since_id = long(idcount.readline())
    except (ValueError, IOError):
        since_id = long(0)

    #
    # We made it this far now Authenticate to Twitter
    ####
    api = authenticate()

    #
    # Setup a list to capture who we send Bible verses to
    ####
    trepto = list()

    if since_id:
        mentions = api.mentions_timeline(since_id)
    else:
        mentions = api.mentions_timeline()

    for tweet in mentions:

        if since_id < tweet.id:
            since_id = tweet.id

        if re.search('#bverse', tweet.text, re.IGNORECASE):
            trepto.append(tweet.user.screen_name)
    #
    # This helps us to be more efficient, we only get a verse
    # if someone has requested one, and we only get one verse
    # for each run. Every request in a run gets the same verse.
    # trepto is twitter reply to [:^P I hate varible naming...
    ####
    if trepto:
        slength = 120
        verse = getverse()

        for tname in trepto:
            if len(verse) <= slength:
                rverse = "@" + tname + " " + verse
                api.update_status(status=rverse)
            else:
                cverse = chunktext(verse, slength)
                for s in reversed(cverse):
                    rverse = "@" + tname + " " + s
                    api.update_status(status=rverse)

    try:
        with open('/var/tmp/SinceID.txt', 'w') as idcount:
            idcount.write(str(since_id) + "\n")
    except IOError:
        pass

if __name__ == '__main__':
    main()
