#!/usr/bin/env python
"""
flatfile storage of json objects
"""

import json
import os

import base


class FlatfileStore(base.Store):
    def __init__(self, directory='.'):
        self.directory = directory

    def save(self, key, data):
        fn = os.path.join(self.directory, '%s.json' % key)
        with open(fn, 'w') as f:
            json.dump(data, f)

    def load(self, key):
        fn = os.path.join(self.directory, '%s.json' % key)
        with open(fn, 'r') as f:
            data = json.load(f)
        return data
