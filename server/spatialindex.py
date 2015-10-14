# -*- coding: utf-8 -*-
"""
    spatialindex
    ~~~~~~

    Implements spatial indexer.

"""

import math
import geohash
from itertools import chain
from werkzeug.datastructures import ImmutableDict

# Default grid size parameters
# unit : meter
GEO_HASH_GRID_SIZE = ImmutableDict({
    5: 4800,
    6: 1220,
    7: 152,
})

class SpatialIndexPoint(object):
    """ A spatial point
    """
    # optimization
    __slots__ = ('latitude', 'longitude', 'rad_latitude', 'rad_longitude', 
                 'ref')

    def __init__(self, latitude, longitude, ref=None):
        #: latitude of point
        self.latitude = latitude
        #: longitude of point
        self.longitude = longitude
        #: latitude of point in radian
        self.rad_latitude = math.radians(self.latitude)
        #: latitude of point in radian
        self.rad_longitude = math.radians(self.longitude)
        #: a reference to associated object
        self.ref = ref

    def __eq__(self, target_point):
        assert isinstance(target_point, SpatialIndexPoint), (
            'Instance of target point != SpatialIndexPoint.'
        )
        return (
            round(self.latitude, 6) == round(target_point.latitude, 6) and
            round(self.longitude, 6) == round(target_point.longitude, 6)
        )

    def distance_to(self, target_point):
        assert isinstance(target_point, SpatialIndexPoint), (
            'Instance of target point != SpatialIndexPoint.'
        )
        if self == target_point:
            return 0.0

        # coefficient : 69.09 * 1.609344 * 1000 
        # 69.09 : coefficient to convert geo-coordinate to mile
        # 1.609344 : mile to km
        # 1000 : km to meter
        coefficient = 111189.57696 
        theta = self.longitude - target_point.longitude

        distance = math.degrees(math.acos(
            math.sin(self.rad_latitude) * math.sin(target_point.rad_latitude) +
            math.cos(self.rad_latitude) * math.cos(target_point.rad_latitude) *
            math.cos(math.radians(theta))
        )) * coefficient

        return distance

class SpatialIndex(object):
    """ Implements spatial search 

            from spatialindex import SpatialIndexPoint, SpatialIndex
            spatialindex = SpatialIndex()

            spatialindex.add_point(SpatialIndexPoint(19.8,23.3))
            point, distance = spatialindex.get_nearest_points((19.8,23.3))

    """

    def __init__(self, maximum_radius=2000):
        #: A precision that determines size of grid 
        self.precision = self.get_suggested_precision(maximum_radius)
        #: A spatial points container
        self.data = {}

    def get_suggested_precision(self, maximum_radius=2000):
        """Finds suggested precision for given radius.
        
        : param maximum_radius: an optional parameter that determines a 
        precision of spatial index
        """ 
        
        suggested_precision = 1
        for precision, grid_size in GEO_HASH_GRID_SIZE.items():
            #Because we are only going to fetch all points 4 neighborhood grids,
            #``maximum_radius`` is larger than ``grid_size / 2``.
            if maximum_radius > grid_size / 2: 
                suggested_precision = precision - 1
                break
        return suggested_precision

    def get_point_hash(self, point):
        """Get hash for spatial point

        : param point: a spatial index point
        """
        assert isinstance(point, SpatialIndexPoint), (
            'Instance of point != SpatialIndexPoint.'
        )
        return geohash.encode(point.latitude, point.longitude, self.precision)

    def add_point(self, point):
        """Add spatial point to spatial index object
        
        : param point: a spatial index point
        """
        assert isinstance(point, SpatialIndexPoint), (
            'Instance of point != SpatialIndexPoint.'
        )

        point_hash = self.get_point_hash(point)
        points = self.data.setdefault(point_hash, [])
        points.append(point)

    def get_near_points(self, center_point, radius=2000):
        """A cheap filter that fetchs all points of 4 neighbor grids that are 
        within a circle generated from given center point and radius.
        
        : param center_point: a center point
        : param radius: a radius from a center point. 2000 by default.
        """
        me_and_neighbors = geohash.expand(self.get_point_hash(center_point))
        return chain(*(self.data.get(key, []) for key in me_and_neighbors))

    def get_nearest_points(self, center_point, radius=2000):
        """A expensive filter that calculates precise distance between 
        ``target_point`` and ``center_point``. Since it is computationally 
        expensive, we make use of a cheap filter to reduce the number of 
        point candidates.
        
        : param center_point: a center point
        : param radius: a radius from a center point. 2000 by default.
        """
        target_points = self.get_near_points(center_point, radius)
        for point in target_points:
            distance = point.distance_to(center_point)
            if distance <= radius:
                yield point, distance
