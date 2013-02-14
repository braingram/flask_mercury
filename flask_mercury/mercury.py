#!/usr/bin/env python

import json
import logging
import os

import flask

import storage


def make_blueprint(app=None, register=True, store=None):
    if store is None:
        store = storage.Store()
    main_dir = os.path.dirname(os.path.abspath(__file__))
    template_folder = os.path.join(main_dir, 'templates')
    static_folder = os.path.join(main_dir, 'static')
    logging.debug('mercury main_dir: %s' % main_dir)
    logging.debug('mercury template_folder: %s' % template_folder)
    logging.debug('mercury static_folder: %s' % static_folder)
    mercury = flask.Blueprint('mercury', 'mercury', \
            template_folder=template_folder, static_folder=static_folder)

    @mercury.route('/save_content', methods=['POST'])
    def save_content():
        print flask.request
        return flask.jsonify(flask.request)

    @mercury.route('/<key>', methods=['GET', 'PUT'])
    def test(key):
        if flask.request.method == 'GET':
            content = {}
            if flask.request.args.get('mercury_frame', False):
                try:
                    content = store.load(key)
                except Exception as E:
                    print "failed to load page data: %s" % E
            return flask.render_template('%s.html' % key, content=content)
        else:
            data = json.loads(flask.request.data)
            try:
                store.save(key, data['content'])
            except Exception as E:
                print "failed to save page data: %s" % E
            return flask.jsonify(data)

    # dirty fix for flask static bug
    @mercury.route('/files/<path:path>')
    def files(path):
        return mercury.send_static_file(path)

    if register:
        if app is None:
            app = flask.Flask('mercury')
        app.register_blueprint(mercury, url_prefix='/mercury')
        return mercury, app
    return mercury


def test(**kwargs):
    store = kwargs.pop('store', None)
    ft, app = make_blueprint(register=True, store=store)
    logging.debug(app.url_map)
    app.run(**kwargs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test()
