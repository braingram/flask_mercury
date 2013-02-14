#!/usr/bin/env python

import os

import flask_mercury

directory = './data'
if not os.path.exists(directory):
    os.makedirs(directory)

print "storing data in: %s" % directory
store = flask_mercury.storage.FlatfileStore(directory)

print "Running flask_mercury.test"
flask_mercury.test(debug=True, store=store)
