#!/usr/bin/env python

import logging
import os

import flask


def make_blueprint(app=None, register=True, fnfilter=None, dfilter=None):
    if fnfilter is None:
        fnfilter = lambda fn: True
    if dfilter is None:
        dfilter = lambda d: True
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

    @mercury.route('/test', methods=['GET', 'PUT'])
    def test():
        print flask.request.method
        if flask.request.method == 'GET':
            return flask.render_template('test.html')
        else:
            print "post called with", flask.request.data
            #for k in dir(flask.request):
            #    print k, getattr(flask.request, k)
            return flask.jsonify(flask.request.args)

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
    ft, app = make_blueprint(register=True)
    logging.debug(app.url_map)
    app.run(**kwargs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test()
