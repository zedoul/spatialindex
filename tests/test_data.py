# -*- coding: utf-8 -*-
"""
    tests.data
    ~~~~~~~~~~~~~~~~~~~~~

    The data functionality.
"""

import pytest
import unittest
import cPickle as pickle
import os

from server.data import Database

class TestData(unittest.TestCase):
    def test_database(self):
        path = "./data.pkl"
        if False == os.path.isfile(path):
            print "data preprocessing work. it will take about 60 seconds..."
            with open(path, 'wb') as pkl_file :
                db =Database("./data/")
                pickle.dump(db, pkl_file, -1)
        with open(path, 'rb') as pkl_file :
            database = pickle.load(pkl_file)
        assert database != None

        # convthreads test
        assert len(database.convthreads()) == 3

        # convthreads by tag_id test
        tag_id = "7516c3b35580b3490248629cff5e498c"
        convthreads = database.convthreads(tag_id)
        assert len(convthreads) == 1
        for convthread in convthreads:
            assert convthread[5] == tag_id
        tag_id = "-1"
        convthreads = database.convthreads(tag_id)
        assert len(convthreads) == 0

        # convthread(convthread_id) test
        convthread_id = "ead27ca5d277b0fdd6b2ee47cf4ba21b"
        convthread = database.convthread(convthread_id)
        assert convthread[0] == convthread_id
        convthread_id = "-1"
        convthread = database.convthread(convthread_id)
        assert convthread == None

        # tag_ids test
        assert 3 == len(database.tag_ids())

        # tag_ids(convthread_id) test
        # tag_id test
        tag_id = database.tag_id("cafe")
        assert tag_id == "d2626f412da748e711ca4f4ae9428664"
        assert None == database.tag_id("-1")

        # popular_messages test
        convthread_id = "ead27ca5d277b0fdd6b2ee47cf4ba21b"
        popular_products = database.popular_messages(convthread_id)
        min_popularity = 0
        for popular_product in popular_products:
            target_popularity = popular_product["popularity"]
            # it should be ordered in ascending order
            assert min_popularity <= target_popularity
            min_popularity = target_popularity

        assert [] == database.popular_products("-1")
