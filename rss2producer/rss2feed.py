"""Provides the RSS2Feed class."""

from calendar import timegm
from email.utils import formatdate
from xml.dom.minidom import Document

class RSS2Feed(object):
    """An RSS 2.0 feed."""

    class FeedError(Exception):
        """Error encountered while producing a feed."""

    def __init__(self, title, link, description):
        """Initialize the feed with the specified attributes.

        :param title: brief title for the feed
        :param link: URL for the page containing the syndicated content
        :param description: longer description for the feed
        """
        self._document = Document()
        rss_element = self._document.createElement('rss')
        rss_element.setAttribute('version', '2.0')
        self._document.appendChild(rss_element)
        self._channel = self._document.createElement('channel')
        rss_element.appendChild(self._channel)
        self._channel.appendChild(self._create_text_element('title', title))
        self._channel.appendChild(self._create_text_element('link', link))
        self._channel.appendChild(self._create_text_element('description', description))

    def _create_text_element(self, type_, text):
        """Create a text element and return it."""
        element = self._document.createElement(type_)
        element.appendChild(self._document.createTextNode(text))
        return element

    def append_item(self, title=None, link=None, description=None, pub_date=None):
        """Append the specified item to the feed.

        :param title: brief title for the item
        :param link: URL for the page for the item
        :param description: longer drescription for the item
        :param pub_date: UTC timestamp or datetime instance of the item's publication date
        """
        # Either title or description *must* be present
        if title is None and description is None:
            raise self.FeedError("Either title or description must be provided.")
        element = self._document.createElement('item')
        if not title is None:
            element.appendChild(self._create_text_element('title', title))
        if not link is None:
            element.appendChild(self._create_text_element('link', link))
        if not description is None:
            element.appendChild(self._create_text_element('description', description))
        if not pub_date is None:
            try:
                timestamp = int(pub_date)
            except TypeError:
                timestamp = timegm(pub_date.utctimetuple())
            element.appendChild(self._create_text_element('pubDate', formatdate(timestamp)))
        self._channel.appendChild(element)

    def get_xml(self):
        """Return the XML for the feed.

        :returns: XML representation of the RSS feed
        """
        return self._document.toxml()
