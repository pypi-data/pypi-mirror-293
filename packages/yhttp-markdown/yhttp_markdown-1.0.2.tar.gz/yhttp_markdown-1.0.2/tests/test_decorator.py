from bddrest import status, response, when

import yhttp.core as y
from yhttp.markdown import markdown2html


def test_if_contenttype(yserver, yapp):
    @yapp.route()
    @markdown2html()
    @y.html
    def get(req):
        return '<h1>Foo</h1>'

    @yapp.route()
    @markdown2html()
    @y.html
    def list(req):
        yield '<h1>'
        yield 'Foo'
        yield '</h1>'

    with yserver():
        assert status == 200
        assert response == '<h1>Foo</h1>'
        assert response.content_type == 'text/html'

        when(verb='list')
        assert status == 200
        assert response == '<h1>Foo</h1>'
        assert response.content_type == 'text/html'


def test_simple(yserver, yapp):
    @yapp.route()
    @markdown2html(if_contenttype=None)
    def get(req):
        return '# Foo'

    with yserver():
        assert status == 200
        assert response == '<h1 id="foo">Foo</h1>\n'
        assert response.content_type == 'text/html'


def test_generator(yserver, yapp):
    @yapp.route()
    @markdown2html(if_contenttype=None)
    def get(req):
        yield '# Foo'
        yield '## bar'

    with yserver():
        assert status == 200
        assert response == '<h1 id="foo">Foo</h1>\n<h2 id="bar">bar</h2>\n'


def test_error(yserver, yapp):
    @yapp.route()
    @markdown2html(if_contenttype=None)
    def get(req):
        raise y.statuses.notfound()

    with yserver():
        assert status == 404
