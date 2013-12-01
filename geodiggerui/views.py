import re
import exceptions
import pymongo

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config

from filterengine import FilterEngine


class GeoDiggerUI(object):
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']

        # Read settings from the server.
        self.minDate = "2012, 0, 1"
        self.maxDate = "2013, 11, 31"
        self.sources = ['Twitter']

        # Set up view parameters.
        self.sliderOptions = str({
            'bounds': {
                'min': 'new Date('+self.minDate+')',
                'max': 'new Date('+self.maxDate+')'
            },
            'defaultValues': {
                'min': 'new Date('+self.minDate+')',
                'max': 'new Date('+self.maxDate+')'
            },
            'scales': [{
            'next': 'function(value){ var next = new Date(value); return new Date(next.setMonth(value.getMonth() + 1)); }',
            'label': 'function(value){ return months[value.getMonth()]; }',
            }],
        }).replace("'", '')

    @view_config(route_name='home',
            renderer='templates/home.pt',
            request_method='GET')
    def home_get(self):
        return dict(title="Setup", progress=45, error=None)

    @view_config(route_name='filter',
            renderer='templates/filter.pt',
            request_method='GET')
    def filter_get(self):
        return dict(title='Filter Parameters', sources=self.sources,
                sliderOptions=self.sliderOptions, error=None)

    @view_config(route_name='filter',
            renderer='templates/filter.pt',
            request_method='POST')
    def filter_post(self):
        print self.request.params

        # Validate the form, regardless of the button clicked.
        try:
            f = FilterEngine()
            # TODO: Get geometry
            if 'weekends' in self.request.params:
                weekends = True
            else:
                weekends = False
            if 'weekdays' in self.request.params:
                weekdays = True
            else:
                weekdays = False
            # TODO: Get min/max date
            if (minDate != self.minDate and maxDate != self.maxDate) or (
                    weekends == False or weekdays == False):
                f.datetime(daterange, weekends, weekdays)
            sources = []
            for source in self.sources:
                if 'source_'+source in self.request.params:
                    sources += source
            if sources != []:
                f.sources(sources)
            if self.request.POST['users'] != u'':
                users = self.request.POST['users'].replace(' ', '').split(',')
                f.users(users)
            if self.request.POST['downloadtype'] == u'JSON':
                self.downloadtype = 'JSON'
            else:
                self.downloadtype = 'CSV'

            # Run the query or save the filter.
            if 'submit' in self.request.params:
                # Run the query, redirect to the file.    
                #url = self.request.route_url('download')
                #return HTTPFound(url)
                pass
            
        except Exception as e:
            return dict(title='Filter Parameters', sources=self.sources,
                    sliderOptions=self.sliderOptions, error=e.message)

        return dict(title='Filter Parameters', sources=self.sources,
                sliderOptions=self.sliderOptions, error="Error")
