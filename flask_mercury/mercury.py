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

    # ----- example route ----
    @mercury.route('/<key>', methods=['GET', 'PUT'])
    def test(key):
        if flask.request.method == 'GET':
            content = {}
            try:
                content = store.load(key)
            except Exception as E:
                print "failed to load page data: %s" % E
            #content[<region>]['snippets'][snippet_<i:0-based>] = options
            # look for [snippet_<i>/1] in content[<region>]['value']
            # fix snippets?
            #for k in content:
            #    if 'snippets' in content[k]:
            #        snippets = content[k]['snippets'].copy()
            #        for s in snippets:
            #            content[k]['snippets'][s] = dict(
            #                    name=snippets[s]['name'],
            #                    options=snippets[s])
            page = flask.render_template('%s.html' % key, content=content)
            #return page
            stext = ""
            for rk in content:
                for si in content[rk]['snippets']:
                    skey = '[%s/1]' % si
                    snippet = content[rk]['snippets'][si]
                    stext = flask.render_template('/snippets/%s/preview.html' \
                            % snippet['name'], data=snippet)
                    page = page.replace(skey, stext)
            #page = page.replace('</body>', stext + '</body>')
            return page
        else:
            data = json.loads(flask.request.data)
            try:
                store.save(key, data['content'])
            except Exception as E:
                print "failed to save page data: %s" % E
            return flask.jsonify(data)

    # ---- snippets ----
    @mercury.route('/views/panels/snippets.html')
    def list_snippets():
        # load snippets
        snippets = []
        d = os.path.join(template_folder, 'snippets')
        for fn in os.listdir(d):
            path = os.path.join(d, fn)
            if os.path.isdir(path):
                options = os.path.exists(os.path.join(path, 'options.html'))
                snippet = dict(name=fn,
                        tags='', description=fn, options=options)
                # load snippet info from
                info_fn = os.path.join(path, 'info.json')
                if os.path.exists(info_fn):
                    with open(info_fn, 'r') as f:
                        info = json.load(f)
                    snippet.update(info)
                snippets.append(snippet)
        return flask.render_template('snippets.html', snippets=snippets)

    @mercury.route('/snippets/<name>/options.html', methods=['POST'])
    def get_snippet_options(name):
        # these snippet options should be forms!
        fn = 'snippets/%s/options.html' % name
        return flask.render_template(fn)

    @mercury.route('/snippets/<name>/preview.html', methods=['POST'])
    def get_snippet_preview(name):
        fn = 'snippets/%s/preview.html' % name
        data = {}
        # get options
        for k, v in flask.request.form.items():
            data[k] = v
        return flask.render_template(fn, data=data)

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
