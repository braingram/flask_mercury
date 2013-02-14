#!/usr/bin/env python


class Store(object):
    """
    Interface to store and retrieve (by key) json data
    corresponding to editable areas
    """
    def save(self, key, data):
        """
        """
        raise NotImplementedError

    def load(self, key):
        """
        """
        raise NotImplementedError
