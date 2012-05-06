import re, urllib, urllib2, json

BLACKLIST = ['odesk', 'elance', '#jobs', 'now hiring']

def search_twitter(query, no_retweets=True):
    if no_retweets:
        query += ' -RT'

    url = 'http://search.twitter.com/search.json?%s' % urllib.urlencode({
            'q': query,
            'lang': 'en', # restrict results to english tweets
            'rpp': 100, # return 100 results per page (maximum value)
    })
    response = json.loads(urllib2.urlopen(url).read())
    return response['results']

def init_queries():
    phrases = [
        'wish there was',
        'why isn\'t there',
        'wish someone would create',
        'somebody needs to create',
        'somebody should create',
        'someone needs to create',
        'someone should create',
    ]

    # add type of product (eg. app, site, or website) to end of phrases
    return ['%s %s' % (p, suffix) for p in phrases for suffix in ['app', 'site', 'website']]

def make_regex(query):
    s = r'(\s\S+){0,2}\s'.join(query.split())
    print s
    return re.compile(s, re.IGNORECASE)

def blacklist(text):
    # reject if tweet starts with quotes or contains blacklisted word
    return text[0] in ['"', unichr(8220)] or any(bad in text for bad in BLACKLIST)

if __name__ == '__main__':
    import sys

    queries = init_queries()

    try:
        index = int(sys.argv[1])
    except (ValueError, IndexError):
        print 'Usage: %s <int>' % sys.argv[0]
        for i, query in enumerate(queries):
            print '%s: %s' % (i, query)
        sys.exit()

    query = queries[index % len(queries)]
    results = search_twitter(query)
    regex = make_regex(query)
    for tweet in results:
        if regex.search(tweet['text']) and not blacklist(tweet['text']):
            print tweet['text'].encode('utf-8', 'ignore')
