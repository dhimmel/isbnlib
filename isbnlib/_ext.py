# -*- coding: utf-8 -*-
"""Extra methods."""

from ._metadata import query
from ._infogroup import infogroup
from ._wcated import query as qed
from ._msk import msk
from ._gwords import goos
from ._core import EAN13
from .dev.bouth23 import u, b2u3
from .dev.helpers import last_first, cutoff_tokens, File


def mask(isbn, separator='-'):
    """`Mask` a canonical ISBN."""
    return msk(isbn, separator)


def meta(isbn, service='default'):
    """Get metadata from worldcat.org ('wcat'), Google Books ('goob') , ..."""
    service = service if service else 'default'
    return query(isbn, service)


def info(isbn):
    """Get language or country assigned to this ISBN."""
    return infogroup(isbn)


def editions(isbn):
    """Return the list of ISBNs of editions related with this ISBN."""
    return qed(isbn)


def isbn_from_words(words):
    """Return the most probable ISBN from a list of words."""
    return goos(words)


def doi(isbn):
    """Return a DOI's ISBN-A from a ISBN-13."""
    return "10.%s.%s%s/%s%s" % \
           tuple(msk(EAN13(isbn), '-').split('-'))


def ren(fp):
    """Renames a file using metadata from an ISBN in his filename."""
    cfp = File(fp)
    isbn = EAN13(cfp.name)
    if not isbn:                               # pragma: no cover
        return
    data = meta(isbn)
    author = data.get('Authors', u('UNKNOWN'))
    if author != u('UNKNOWN'):
        author = last_first(author[0])['last']
    year = data.get('Year', u('UNKNOWN'))
    maxlen = 98 - (20 + len(author) + len(year))
    title = data.get('Title', u('UNKNOWN'))\
        .replace(',', ' ')\
        .replace('.', ' ').strip()
    if title == u('UNKNOWN') or not title:     # pragma: no cover
        return
    if ' ' in title:
        tokens = title.split(' ')
        stitle = cutoff_tokens(tokens, maxlen)
        title = ' '.join(stitle)
    isbn13 = data.get('ISBN-13', u('UNKNOWN'))
    new_name = "%s%s_%s_%s" % (author, year, title, isbn13)
    return cfp.baserename(b2u3(new_name + cfp.ext))