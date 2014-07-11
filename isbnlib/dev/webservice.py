# -*- coding: utf-8 -*-
"""Query web services."""

import logging
import gzip
from .bouth23 import s, bstream
try:                     # pragma: no cover
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
except ImportError:      # pragma: no cover
    from urllib import urlencode
    from urllib2 import Request, urlopen, HTTPError, URLError
from ._exceptions import ISBNLibHTTPError, ISBNLibURLError

UA = 'isbnlib (gzip)'
LOGGER = logging.getLogger(__name__)


class WEBService(object):

    """Class to query web services."""

    def __init__(self, url, user_agent=UA, values=None, appheaders=None):
        """Initialize main properties."""
        self._url = url
        # headers to accept gzipped content
        headers = {'Accept-Encoding': 'gzip', 'User-Agent': user_agent}
        # add more user provided headers
        if appheaders:  # pragma: no cover
            headers.update(appheaders)
        # if 'data' it does a PUT request (data must be urlencoded)
        data = urlencode(values) if values else None
        self._request = Request(url, data, headers=headers)
        self.response = None

    def _response(self):
        try:
            self.response = urlopen(self._request)
            LOGGER.debug('Request headers:\n%s', self._request.header_items())
        except HTTPError as e:  # pragma: no cover
            LOGGER.critical('ISBNLibHTTPError for %s with code %s [%s]',
                            self._url, e.code, e.msg)
            if e.code in ('401', '403', '429'):
                raise ISBNLibHTTPError('Are you are making many requests?')
            if e.code in ('502', '504'):
                raise ISBNLibHTTPError('Service temporarily unavailable!')
            raise ISBNLibHTTPError('(%s) %s' % (e.code, e.msg))
        except URLError as e:   # pragma: no cover
            LOGGER.critical('ISBNLibURLError for %s with reason %s',
                            self._url, e.reason)
            raise ISBNLibURLError(e.reason)

    def data(self):
        """Return the uncompressed data."""
        self._response()
        LOGGER.debug('Response headers:\n%s', self.response.info())
        if self.response.info().get('Content-Encoding') == 'gzip':
            buf = bstream(self.response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:                   # pragma: no cover
            data = self.response.read()
        return s(data)


def query(url, user_agent=UA, values=None, appheaders=None):
    """Query to a web service."""
    service = WEBService(url, user_agent, values, appheaders)
    data = service.data()
    LOGGER.debug('Raw data from service:\n%s', data)
    return data
