# -*- coding: utf-8 -*-

import os
from flask import Flask
from server.api import api
from server.search import Search
from server.data import Database

def create_app(settings_overrides=None):
    app = Flask(__name__)
    configure_settings(app, settings_overrides)
    configure_blueprints(app)

    import cPickle as pickle

#    path = "./data.pkl"
#    if False == os.path.isfile(path):
#        print "data preprocessing work. it will take about 60 seconds..."
#        with open(path, 'wb') as pkl_file :
#            db = Database("./data/")
#            pickle.dump(db, pkl_file, -1)
#    with open(path, 'rb') as pkl_file :
#        app.data = pickle.load(pkl_file)
#
#    path = "./search.pkl"
#    if False == os.path.isfile(path):
#        print "spatial search preprocessing. it will take about 60 seconds..."
#        with open(path, 'wb') as pkl_file :
#            pickle.dump(Search(app.data), pkl_file, -1)
#    with open(path, 'rb') as pkl_file :
#        app.search = pickle.load(pkl_file)

    app.data = Database("./data/")
    app.search = Search(app.data)

    return app

def configure_settings(app, settings_override):
    parent = os.path.dirname(__file__)
    data_path = os.path.join(parent, '..', 'data')
    app.config.update({
        'DEBUG': True,
        'TESTING': False,
        'DATA_PATH': data_path
    })
    if settings_override:
        app.config.update(settings_override)

def configure_blueprints(app):
    app.register_blueprint(api)
