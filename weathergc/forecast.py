'''Main entry point for the weathergc package.'''
from __future__ import absolute_import
import json
import re
import sys
from collections import defaultdict

import xmltodict

from weathergc import validators
from weathergc.utils import list_iter

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


class Forecast(object):
    '''Environment Canada weather data for humans.

    weather.gc.ca provides weather forecasts for 768 locations in Canada, on
    the website and as atom RSS feeds. The purpose of this library is to
    transform this raw data into a python object that helps you easily
    integrate weather data into your application.

    High level flow:
    - constructor accepts city-code, which calls refresh to retrieve the data
      and transform it into a Python dict.  _refresh can update it later too.
    - _parse handles basic validation and re-organizes the data structure to
      group entries into sections, and stores as _source
    - section specific _transform methods further refine and annotate the
      data to a point where it's ready for final use.
    '''

    def __init__(self, city_code):
        '''Constructor to create an instance of Forecast.

        Environment Canada uses 4-5 character city codes to identify
        the location for a given forecasts.  The city code can be found
        by navigating to the Local forecast, and examining the URL.

        For example:
        https://weather.gc.ca/city/pages/on-82_metric_e.html --> on-82
        https://weather.gc.ca/city/pages/ns-19_metric_e.html --> ns-19

        Args:
            city_code: code for the location
        '''
        if self._valid_city_code(city_code):
            self._city_code = city_code.lower()
        else:
            raise ValueError('%s is not a valid city code.' % city_code)

        self._source = None
        self.refresh()

    def as_json(self):
        return json.dumps(self._collate(), indent=4)

    def as_dict(self):
        return self._collate()

    def refresh(self):
        '''Retrieve data from website, parse and store in _source.'''
        url = 'https://weather.gc.ca/rss/city/%s_e.xml' % self._city_code

        response = urlopen(url)
        xml = response.read()

        obj = xmltodict.parse(xml, dict_constructor=dict)
        self._source = self._parse(obj)

    @staticmethod
    def _valid_city_code(city_code):
        return re.match('^[a-z]{2}-[a-z]{0,1}[0-9]{1,3}$', city_code.lower())

    def _parse(self, atom):
        '''
        Handles basic validation and re-organizes the data structure to
        group entries by category. 'feed' is dropped, and everything not under
        'entry' becomes part of a category called 'meta'.
        Like this:

            Before:
                {'feed': {'@xml:lang': 'en-ca',
                 'entry': [{'category': {'@term': 'Warnings and Watches'},
                            'title': 'No watches or warnings in effect, Canora',

            After:
                {'meta': [{'@xml:lang': 'en-ca'}],
                 'Warnings and Watches': [
                           {'title': 'No watches or warnings in effect, Canora',
                           ...

        Args:
            data: dict version of the unprocessed atom rss of a city forecast

        Returns:
            dict with one key per section
        '''
        obj = defaultdict(list)

        # meta is everything except 'entry'
        obj['meta'] = validators.META_SCHEMA(atom['feed'])

        # break out the entry key into lists by their type
        if 'entry' in atom['feed']:
            entries = atom['feed']['entry']

            for entry in list_iter(entries):
                parsed_entry = validators.ENTRY_SCHEMA(entry)

                # type will be 'Warnings and Watches', 'Current Conditions' etc
                obj[parsed_entry['category']].append(parsed_entry)

        return obj

    def _transform_warnings_and_watches(self):
        '''Transform warnings and watches section into final structure.'''
        category = 'Warnings and Watches'
        processed = []
        if category in self._source:
            for entry in self._source[category]:
                processed.append(validators.WW_SCHEMA(entry))

        return {category: processed}

    def _transform_current_conditions(self):
        '''Transform current conditions section into final structure.'''
        category = 'Current Conditions'
        processed = []
        if category in self._source:
            for entry in self._source[category]:
                processed.append(validators.CC_SCHEMA(entry))

        return {category: processed}

    def _transform_weather_forecasts(self):
        '''Transform weather forecasts section into final structure.'''
        category = 'Weather Forecasts'
        processed = []
        if category in self._source:
            for entry in self._source[category]:
                processed.append(validators.WF_SCHEMA(entry))

        return {category: processed}

    def _transform_meta(self):
        '''Transform meta section into final structure.'''
        category = 'meta'
        processed = self._source[category]
        processed['badge'] = self._forecast_badge_url()

        return {category: processed}

    def __str__(self):
        return self.as_json()

    def _forecast_badge_url(self):
        '''Environment Canada provides a city forecast in badge / graphic
        format at a different URL.

        Returns:
            string for URL of the badge based on the city code for this object
        '''
        return ('https://weather.gc.ca'
                '/wxlink/wxlink.html?cityCode=%s&lang=e' % self._city_code)

    def _collate(self):
        '''Invoke transformations and collate all data into a single, nested
        object.

        Returns:
            dict of combined, processed results.
        '''
        collated = self._transform_meta()
        collated.update(self._transform_warnings_and_watches())
        collated.update(self._transform_current_conditions())
        collated.update(self._transform_weather_forecasts())
        return collated


if __name__ == '__main__':
    print(Forecast(sys.argv[1]).as_json())
