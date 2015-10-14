# -*- coding: utf-8 -*-

import math
from flask import Blueprint, current_app, jsonify, request

api = Blueprint('api', __name__)

@api.route('/search', methods=['GET'])
def search():
    """
    A spatial search that finds the most popular conversation threads near user location. 

    GET

    Parameters are required as follows :

    :param lat: latitude of user location for spatial search
    :param lng: longitude of user location for spatial search
    :param radius: a search radius for spatial search
    :param tags: an optional value that allows user to narrow search. If tags 
                 are provided, a convthread needs to have at least one of them to be 
                 considered a candidate.
    :param count: the number of conversation threads to return.

    Returns a number of most popular conversation threads. 

    e.g.)
    [
        {
            'id': 'e3142db1a976471891257228ac532000',
            'title': 'Annie', 
            'popularity': 1.0, 
            'quantity': 10,
            'message': {
                'id': '2f8aab36b8884969811519d1fd0ac1c4',
                'name': 'Torphy-Corwin',
                'lat': 59.335460084597436,
                'lng': 18.060754569857444
            },
        },
        {
            ...
        },
        ...
    ]

    """

    lat = request.args.get('lat', float('nan'), float)
    lng = request.args.get('lng', float('nan'), float)
    radius = request.args.get('radius', 0, int) # unit : meter
    tags = request.args.get('tags', "", str)
    count = request.args.get('count', -1, int)

    if math.isnan(lat) or abs(lat) > 180:
        return jsonify({'error' : "lat is a nan or more than abs(180)"})
    if math.isnan(lng) or abs(lng) > 90:
        return jsonify({'error' : "lng is a nan or more than abs(90)"})
    if radius <= 0: 
        return jsonify({'error' : "Too small radius : %d" % radius})
    if count <= 0: 
        return jsonify({'error' : "Too small count : %d" % count})

    user_pos = (lat, lng)
    tags = tags.split(",") if "" != tags else None

    convthread_ids = current_app.search.convthreads_nearby_user(user_pos, radius, tags)
    popular_messages = current_app.search.popular_messages(convthread_ids, count)

    print popular_messages
    return jsonify({'messages': popular_messages})
