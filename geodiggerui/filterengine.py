"""
Provides an easier interface for querying a MongoDB server. Allows
searching for documents based on time, userID, and GeoJSON polygons and
points.

The general use case is to create a FilterEngine object, call one or
more of the "Query forming methods", then call `query()` on the object.
An object's query method may be called more than once. The methods that
build the query always overwrite any previous values, so a single object
may be re-used to perform the same query, a slighty modified query, or
an entirely new query. For example:

    >>> f = FilterEngine()
    >>> f.users(['userID1', 'userID2'])  # users with matching IDs
    >>> f.geography([[0.0, 0.0]], 2)     # coordinates within 2 units
    >>>                                  # distance from [0,0]
    >>> f.query()
    ** returned data **
    >>> f.query()
    ** returned data: same query **
    >>> f.users(['userid3'])             # overwrites previous list
    >>> f.query()
    ** returned data: userid3 and the previous geography **
    >>> f.datetime(myDateRange)          # adds a datetime restriction
    >>> f.query()
    ** returned data: userid3, geography, and date range **

"""

import pymongo
from bson.son import SON


class FilterEngine(object):
    def __init__(self):
        # Set up initial member variables.
        pass
        # Set up MongoDB connection.

    # Private member functions.
    formPolygon(self):
        """Reads a list of lists/tuples from a member variable, and
           returns a binary SON object in valid GeoJSON format.
        """
        pass

    formQuery(self):
        """Forms the finalized Mongo query from member variable
           contents, and returns it as a SON object.
        """
        pass


    # Query forming methods.
    def users(self, users):
        """Accepts a list of userIDs and adds them to the query.
           No return. (Void method.)
        """
        pass

    def datetime(self, datetime, weekends=True, weekdays=True):
        """Accepts a list with two entries representing a start and end
           date/time, and two boolean values that determine whether or not
           to include weekends/weekdays.
           No return. (Void method.)
        """
        pass

    def geography(self, polygon, radius=None):
        """Accepts a list of lists in the format: [[long1, lat1], ...,
           [[longN, latN]]. Each sub-list is a point. If `polygon`
           contains only one list, it is assumed to be a Point,
           otherwise it is assumed to be a Polygon. In the case of a
           single Point, `range` must be set to a non-negative integer
           value; for polygons this value is ignored.
           No return. (Void method.)
        """
        pass

    def sources(self, sources):
        """Accepts a list of strings representing the source of the
           data point.
           No return. (Void method.)
        """
        pass


    # Run the query.
    def query(self):
        """Send the pre-formed query to the MongoDB server.
           Returns the raw results of the query.
        """
        pass
