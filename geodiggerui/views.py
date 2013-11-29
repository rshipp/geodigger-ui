import re
import exceptions

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config

#from filterengine import FilterEngine


class GeoDiggerUI(object):
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']

    @view_config(route_name='home',
            renderer='templates/home.pt',
            request_method='GET')
    def home_get(self):
        return dict(title='Home')

    @view_config(route_name='home',
            renderer='templates/home.pt',
            request_method='POST')
    def home_post(self):
        pass
#        url = self.request.route_url('dns_addedit', hostname=hostname)
#        return HTTPFound(url)
