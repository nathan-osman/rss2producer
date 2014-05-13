from datetime import datetime
from nose.tools import eq_
from rss2producer import RSS2Feed

def test_empty():
    f = RSS2Feed('', '', '')
    eq_(f.get_xml(), '<?xml version="1.0" ?><rss version="2.0"><channel><title>' +
                     '</title><link></link><description></description></channel></rss>')

def test_append():
    f = RSS2Feed('', '', '')
    f.append_item('', '', '', datetime(1970, 01, 01))
    eq_(f.get_xml(), '<?xml version="1.0" ?><rss version="2.0"><channel><title>' +
                     '</title><link></link><description></description><item><title>' +
                     '</title><link></link><description></description><pubDate>' +
                     'Thu, 01 Jan 1970 00:00:00 -0000</pubDate></item></channel></rss>')
