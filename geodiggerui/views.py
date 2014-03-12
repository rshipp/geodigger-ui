import re
import exceptions
import pymongo
from datetime import datetime
import ast

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config

import geodiggerui.config as config


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

        # Connect to the database.
        #conn = pymongo.Connection(config.mongo['server'])
        #db = conn[config.mongo['database']]
        #self.db = db[config.mongo['collection']]


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
            query = dict()

            # Get geometry.
            if (self.request.POST['geojson'] != u''):
                geojson = ast.literal_eval(self.request.POST['geojson'])
                query['coordinates'] = {
                    '$within': {
                        '$polygon': geojson['coordinates'][0],
                    },
                }

            # Get min/max date.
            minDate = self.request.POST['minDate']
            maxDate = self.request.POST['maxDate']
            datefmt = '%a, %d %b %Y %H:%M:%S %Z'
            if (minDate != u'' or maxDate != u''):
                query['time'] = {}
            if (minDate != u''):
                minDate = datetime.strptime(minDate, datefmt).date()
                query['time']['$gt'] = minDate
            if (maxDate != u''):
                maxDate = datetime.strptime(maxDate, datefmt).date()
                query['time']['$lt'] = maxDate

            # Get weekends/weekdays.
            # TODO: Aggregation, use $dayOfWeek.

            # Get sources.
            sources = []
            for source in self.sources:
                if 'source_'+source in self.request.params:
                    sources += [source.lower()]
            query['source'] = {'$in': sources}

            # Get users.
            if self.request.POST['users'] != u'':
                users = int(self.request.POST['users'])
                #query['userID'] = {'$in': users}
                # TODO: Aggregation, limit the number of users.
                # Randomize data first!

            # Get download type.
            if self.request.POST['downloadtype'] == u'CSV':
                self.downloadtype = 'CSV'
            else:
                self.downloadtype = 'JSON'

            # Run the query.
            if 'submit' in self.request.params:
                # Run the query, redirect to the file.
                print query
                #url = self.request.route_url('download')
                #return HTTPFound(url)
            
        except Exception as e:
            return dict(title='Filter Parameters', sources=self.sources,
                    sliderOptions=self.sliderOptions, error=e.message)

        return dict(title='Filter Parameters', sources=self.sources,
                sliderOptions=self.sliderOptions, error="No Error")
