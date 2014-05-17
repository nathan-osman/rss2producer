from datetime import datetime
from nose.tools import eq_
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

    def test_append(self):
        feed = RSS2Feed('', '', '')
        feed.append_item('Title', 'http://example.org', 'Description', datetime(1970, 01, 01))
        root = ElementTree.fromstring(feed.get_xml())
        eq_(root.find('./channel/item/title').text, 'Title')
        eq_(root.find('./channel/item/link').text, 'http://example.org')
        eq_(root.find('./channel/item/description').text, 'Description')
