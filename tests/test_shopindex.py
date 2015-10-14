# -*- coding: utf-8 -*-
"""
    tests.shopindex
    ~~~~~~~~~~~~~~~~~~~~~

    The shop indexer functionality.
"""

import pytest
import unittest
from server.spatialindex import SpatialIndexPoint, SpatialIndex

class TestShopindex(unittest.TestCase):
    def test_shopindex_init(self):
        for radius in [100,500,1000,2000] :
            shopindex = SpatialIndex(radius)
            assert shopindex != None

    def test_shopindex_point_equal_check(self):
        point_a = SpatialIndexPoint(34,23)
        point_b = SpatialIndexPoint(34,23)
        assert point_a == point_b

        point_a = SpatialIndexPoint(34.000008,23.000009)
        point_b = SpatialIndexPoint(34.000007,23.000007)
        assert point_a != point_b

        point_a = SpatialIndexPoint(34.0000008,23.0000009)
        point_b = SpatialIndexPoint(34.0000007,23.0000007)
        assert point_a == point_b

    def test_shopindex_point_distance(self):
        import os
        import cPickle as pickle
        path = "./search.pkl"
        if False == os.path.isfile(path):
            print "spatial search preprocessing. it will take about 60 seconds"
            with open(path, 'wb') as pkl_file :
                pickle.dump(Search(app.data), pkl_file, -1)
        with open(path, 'rb') as pkl_file :
            search = pickle.load(pkl_file)

        radius_size = 2000 
        user_point = SpatialIndexPoint(59.3325800, 18.0649000)
        index = search.spatial_indexers[radius_size]
        points = index.get_nearest_points(user_point)
        for point, distance in points:
            assert distance <= 2000

