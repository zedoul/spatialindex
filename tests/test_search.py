# -*- coding: utf-8 -*-
"""
    tests.search
    ~~~~~~~~~~~~~~~~~~~~~

    The search functionality.
"""

import pytest

def test_search_counts(client):
    rv = client.get('/search?lat=59.33258&lng=18.0649&radius=500&tags=&count=10')
    assert {'products': []} != rv.json
    assert len(rv.json['products']) == 10

    rv = client.get('/search?lat=59.33258&lng=18.0649&radius=500&tags=&count=20')
    assert {'products': []} != rv.json
    assert len(rv.json['products']) == 20

    rv = client.get('/search?lat=59.33258&lng=18.0649&radius=500&tags=&count=50')
    assert {'products': []} != rv.json
    assert len(rv.json['products']) == 50

def test_search_speed_performance(client):
    import time
    start = time.time()
    rv = client.get('/search?lat=59.33258&lng=18.0649&radius=2000&tags=&count=50')
    elapsed = time.time() - start
    assert elapsed < 0.3, "elapsed %f" % elapsed
