from datetime import datetime
from nose.tools import eq_, raises
from xml.etree import ElementTree

from rss2producer import RSS2Feed

class TestRSS2Feed:
    """Tests the RSS2Feed class."""

    def test_feed(self):
        feed = RSS2Feed('Title', 'http://example.org', 'Description')
        root = ElementTree.fromstring(feed.get_xml())
        eq_(root.find('./channel/title').text, 'Title')
        eq_(root.find('./channel/link').text, 'http://example.org')
        eq_(root.find('./channel/description').text, 'Description')

    def test_utf8(self):
        hello_world = u'\u3053\u3093\u306b\u3061\u306f\u4e16\u754c'
        feed = RSS2Feed(hello_world, '', '')
        root = ElementTree.fromstring(feed.get_xml().encode('utf-8'))
        eq_(root.find('./channel/title').text, hello_world)

    def test_append(self):
        feed = RSS2Feed('', '', '')
        feed.append_item('Title', 'http://example.org', 'Description', datetime(1970, 01, 01))
        root = ElementTree.fromstring(feed.get_xml())
        eq_(root.find('./channel/item/title').text, 'Title')
        eq_(root.find('./channel/item/link').text, 'http://example.org')
        eq_(root.find('./channel/item/description').text, 'Description')
        eq_(root.find('./channel/item/pubDate').text, 'Thu, 01 Jan 1970 00:00:00 -0000')

    def test_timestamp(self):
        feed = RSS2Feed('', '', '')
        feed.append_item('Title', pub_date=0)
        root = ElementTree.fromstring(feed.get_xml())
        eq_(root.find('./channel/item/pubDate').text, 'Thu, 01 Jan 1970 00:00:00 -0000')

    def test_absent_items(self):
        feed = RSS2Feed('', '', '')
        feed.append_item(description='Description')
        root = ElementTree.fromstring(feed.get_xml())
        eq_(root.find('./channel/item/title'), None)
        eq_(root.find('./channel/item/link'), None)
        eq_(root.find('./channel/item/pubDate'), None)

    @raises(RSS2Feed.FeedError)
    def test_title_description_required(self):
        feed = RSS2Feed('', '', '')
        feed.append_item()
