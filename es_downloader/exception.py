"""exception"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class ElasticSearchDownloader(Exception):
    """Validation related exception"""
    pass


class NoResultsException(Exception):
    """Query returned an empty result."""
    pass
