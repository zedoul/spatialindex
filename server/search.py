# -*- coding: utf-8 -*-
"""
    search
    ~~~~~~

    Implements search related features such as spatial search.

"""

from flask import current_app
from server.spatialindex import SpatialIndexPoint, SpatialIndex
from server.data import Database
from werkzeug.datastructures import ImmutableList

# Default radius size parameters
RADIUS_SIZES = ImmutableList([
    500,
    2000,
])

class Search(object):
    """Searches for nearby convthreads or conversation threads
    """

    def __init__(self, data):
        """
        Initializes spatial indexers

        :param data: a data container. See :class `~Data` for more information. 
        """

        #: A dictionary that contains the convthread indexers. 
        #: See :class: `~SpatialIndexer` for more information. 
        self.spatial_indexers = self.create_spatial_indexers(data)

    def create_spatial_indexers(self, data):
        """Create spatial indexers for convthreads 

        :param data: a data container. See :class `~Data` for more information. 
        """

        # Initialize indexers for each combination of radius size 
        # and ``tag_id``s.
        spatial_indexers = {}
        for size in RADIUS_SIZES:
            spatial_indexers[size] = SpatialIndex(size)
        for tag_id in data.tag_ids():
            spatial_indexers[tag_id] = {}
            for size in RADIUS_SIZES:
                spatial_indexers[tag_id][size] = SpatialIndex(size)

        # Add points for each indexer
        for [convthread_id, lat, lng, title] in data.convthreads():
            point = SpatialIndexPoint(lat, lng, ref=convthread_id)

            for size in RADIUS_SIZES:
                spatial_indexers[size].add_point(point)
                for tag_id in data.tag_ids(convthread_id):
                    spatial_indexers[tag_id][size].add_point(point)

        return spatial_indexers

    def convthreads_nearby_user(self, user_location, radius, tags=None):
        """ Finds all convthreads nearby user for given a user location 
        as center point and a radius. 

        : param user_location: two-dimensional tuple (latidute, longitude). 
                               e.g. (59.33, 18.06) Stockholm!
        : param radius: the radius for search area. 
        : param tags: if set, this method will return convthreads have at least 
                      one of given tags. 
        """

        # currently only 500 and 2000 radius sizes are supported for searching
        radius_size = 500 if radius < 500 else 2000 

        user_point = SpatialIndexPoint(user_location[0], user_location[1])
        convthread_ids = []

        if None == tags:
            index = self.spatial_indexers[radius_size]
            points = index.get_nearest_points(user_point, radius)
            for point, _ in points:
                convthread_ids.append(point.ref)
        else :
            for tag in tags:
                tag_id = current_app.data.tag_id(tag)
                convthread_ids_by_tag = []
                if None != tag_id:
                    index = self.spatial_indexers[tag_id][radius_size]
                    points = index.get_nearest_points(user_point, radius)
                    for point, _ in points:
                        convthread_ids_by_tag.append(point.ref)
                # recursively constructs union set of convthread_id 
                convthread_ids = set(convthread_ids_by_tag) | set(convthread_ids)

        return convthread_ids

    def popular_messages(self, convthread_ids, count=10, min_quantity=1):
        """ Finds popular messages of selected convthreads in descending order

        : param convthread_ids: convthreads ids 
        : param count: the number of popular message to return 
        : param min_quantity: a threshold for the minimum quantity of message 
                              candidates. 1 by default. 
        """

        convthreads_messages = []

        # fetch popular messages for each convthread. they are sorted in ascending 
        # order. 
        for convthread_id in convthread_ids:
            messages = current_app.data.popular_messages(convthread_id)
            if messages != []:
                convthreads_messages.append(messages)

        # find the best messages in descending order. since all 
        # ``convthread_messages`` are already sorted in ascending order, it simply 
        # compares the last element as a possible candidates.
        popular_messages = []
        popular_threshold = 1.0
        while (len(popular_messages) < count) :
            target_convthread_messages = None
            max_popularity = 0.0

            for convthread_messages in convthreads_messages:
                if 0 < len(convthread_messages):
                    convthread_message = convthread_messages[-1]
                    popularity = convthread_message["popularity"]

                    if max_popularity < popularity:
                        target_convthread_messages = convthread_messages
                        max_popularity = popularity
                        if popular_threshold <= popularity :
                            break

            if target_convthread_messages == None:
                popular_threshold = max_popularity
                break

            popular_message = target_convthread_messages.pop()
            popular_messages.append(popular_message)

        return popular_messages
