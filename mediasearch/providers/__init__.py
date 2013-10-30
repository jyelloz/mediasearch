from collections import namedtuple

__all__ = [
    'SearchResult',
]


SearchResult = namedtuple('SearchResult', ['title', 'url', 'source'])
