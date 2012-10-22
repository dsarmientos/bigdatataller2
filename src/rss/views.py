import feedparser
import re
import urllib2
import lxml.html

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from django.shortcuts import render_to_response

import sentiment


def home(request):
    parsed_feeds = get_parsed_feeds()
    items = []
    for feed in parsed_feeds:
        items.extend((item for item in feed['items']))
    return render_to_response('index.html', {'items': items})

def sentiment_analysis(request):
    if request.method != 'POST' or 'text'not in request.POST:
        return HttpResponseBadRequest()
    text = request.POST['text'].encode('ascii', 'xmlcharrefreplace')
    sentiment_, features = sentiment.sentiment(text)
    features = sorted(features, key=lambda f: f[1])
    return HttpResponse(
                simplejson.dumps(
                    {'sentiment': '%0.2f' % sentiment_,
                     'features': '|'.join((unicode(f) for f in features))}
                ),
                mimetype='application/json')


def filtro_regex(request):
    if request.method != 'GET' or 'q'not in request.GET:
        return HttpResponseBadRequest()
    keyword = request.GET['q'].encode('ascii', 'xmlcharrefreplace')
    filter_regex = build_filter_regex(keyword)
    item_regex = re.compile('<item>(?P<item>.*?)</item>', re.DOTALL)
    title_regex = re.compile('<title>(.*?)</title>')
    titles = []
    for feed_xml in get_feeds_xml():
        for match in item_regex.finditer(feed_xml):
            item_xml = match.group('item')
            if filter_regex.search(item_xml):
                title = title_regex.search(item_xml).group(1)
                titles.append(title)
    return HttpResponse(simplejson.dumps({'titles': titles}),
                        mimetype='application/json')


def get_parsed_feeds():
    feeds_xml = get_feeds_xml()
    parsed_feeds = []
    for feed_xml in feeds_xml:
        parsed_feeds.append(parse_feed(feed_xml))
    return parsed_feeds


def parse_feed(xml):
    feed = feedparser.parse(xml)
    for item in feed['items']:
        item['bottom_line'] = extract_bottom_line(item)
    return feed


def extract_bottom_line(item):
    description = item['description']
    desc_text = lxml.html.fromstring(description).text_content()
    bottom_line_re= re.compile(r'Bottom +Line:(.*)\[Read +more\]')
    match = bottom_line_re.findall(desc_text)
    if match:
        bottom_line = match[0].strip()
        return bottom_line


def get_feeds_xml():
    feeds_urls = ('http://feeds.feedburner.com/cnet/YIff',)
    feeds_xml = []
    for feed_url in feeds_urls:
        feed_xml = cache.get(feed_url)
        if feed_xml is None:
            feed_xml = get_feed_xml(feed_url)
            cache.set(feed_url, feed_xml)
        feeds_xml.append(feed_xml)
    return feeds_xml


def get_feed_xml(feed_url):
    request = urllib2.urlopen(feed_url)
    xml = request.read()
    request.close()
    return xml


def build_filter_regex(keyword):
    filter_regex = (
        '(<title>[^<]*?%(keyword)s[^<]*?</title>|'
        '<description>[^<]*?%(keyword)s[^<]*?</description>|'
        '<category[^>]*?>[^<]*?%(keyword)s[^<]*?</category>)') % (
            {'keyword': re.escape(keyword)})
    return re.compile(filter_regex, re.DOTALL | re.IGNORECASE)
