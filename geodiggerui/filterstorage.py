"""
Store FilterEngine objects in a MongoDB server for later use.
"""

import pymongo


class FilterStorage(object):
    def __init__(self):
        # Connect to the server
        pass

    def saveFilter(self, filterObject):
        """Save a filter."""
        pass

    def loadFilters(self, filterObject):
        """Returns a list of filter objects."""
        pass
