"""Provides the RSS2Feed class."""

from calendar import timegm
from email.utils import formatdate
from xml.dom.minidom import Document

class RSS2Feed(object):
    """Represents an RSS 2.0 feed."""

    def __init__(self, title, link, description):
        """Initialize the feed with the specified attributes."""
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

    def append_item(self, title, link, description, pub_date):
        """Append the specified item to the feed."""
        element = self._document.createElement('item')
        element.appendChild(self._create_text_element('title', title))
        element.appendChild(self._create_text_element('link', link))
        element.appendChild(self._create_text_element('description', description))
        element.appendChild(self._create_text_element('pubDate', formatdate(timegm(pub_date.utctimetuple()))))
        self._channel.appendChild(element)

    def get_xml(self):
        """Return the XML for the feed."""
        return self._document.toxml()
