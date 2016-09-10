# -*- coding: utf-8 -*-
'''
Tests for weathergc.
'''
from __future__ import absolute_import, unicode_literals
from mock import patch
from mock import Mock
import os
import re
import unittest

import xmltodict

from weathergc.utils import html_to_dict, list_iter
from weathergc import validators
from weathergc.forecast import Forecast


class TestForecast(unittest.TestCase):
    def _test_file_iter(self):
        folder = os.path.join(os.path.dirname(__file__), 'data')
        print(folder)
        for root, dirs, files in os.walk(os.path.dirname(__file__)):
            for file in files:
                if file.endswith('.xml'):
                    print('file is %s' % file)
                    with open(os.path.join(folder, file), 'rt') as f:
                        # encoding='utf8') as f:
                        s = f.read()
                        encoding = re.search(
                            '\?xml version="1.0" encoding="(.*?)"\?>',
                            s).group(1)
                        try:
                            data = unicode(s, encoding)
                        except NameError:
                            data = s
                        yield (file[:-4], data)

    @patch('weathergc.forecast.Forecast.refresh')
    def test_create_forecast_objects_from_all_files(self, mock_refresh):
        for city_code, xml in self._test_file_iter():
            f = Forecast(city_code)
            f._source = f._parse(xmltodict.parse(xml, dict_constructor=dict))
            self.assertIsInstance(f.as_dict(), dict)


class TestUtils(unittest.TestCase):
    def test_html_to_dict_parsing(self):
        html = '<b>Observed at:</b> Attawapiskat Airport 3:00 PM EDT Friday 02 September 2016 <br/>\n<b>Condition:</b> Mostly Cloudy <br/>\n'
        data = html_to_dict(html)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 2)
        self.assertEqual(data['Condition'], 'Mostly Cloudy')

    def test_list_iter(self):
        self.assertIsInstance(list_iter({1: 1}), list)
        self.assertIsInstance(list_iter(None), list)
        self.assertIsInstance(list_iter([{1: 1}]), list)


class TestValidators(unittest.TestCase):
    def setUp(self):
        self.data = {'feed': {
            '@xml:lang': 'en-ca',
            '@xmlns': 'http://www.w3.org/2005/Atom',
            'author': {'name': 'Environment Canada',
                       'uri': 'http://www.weather.gc.ca'},
            'entry':
            [{'category': {'@term': 'Warnings and Watches'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_w1:20160831051500',
              'link': {'@href':
                       'http://www.weather.gc.ca/warnings/index_e.html',
                       '@type': 'text/html'},
              'published': '2016-08-31T05:15:00Z',
              'summary': {'#text': 'No watches or warnings in '
                          'effect.',
                          '@type': 'html'},
              'title': 'No watches or warnings in effect, '
              'Algonquin Park (Brent)',
              'updated': '2016-08-31T05:15:00Z'},
             {'category': {'@term': 'Current Conditions'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_cc:20160904190000',
              'link':
              {'@href':
               'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
               '@type': 'text/html'},
              'published': '2016-09-04T19:00:00Z',
              'summary': {'#text': '<b>Observed at:</b> Algonquin '
                          'Park East Gate 3:00 PM EDT '
                          'Sunday 04 September 2016 '
                          '<br/>\n'
                          '<b>Temperature:</b> '
                          '24.2&deg;C <br/>\n'
                          '<b>Pressure / Tendency:</b> '
                          '102.5 kPa falling<br/>\n'
                          '<b>Humidity:</b> 40 %<br/>\n'
                          '<b>Humidex:</b> 25 <br/>\n'
                          '<b>Dewpoint:</b> 9.7&deg;C '
                          '<br/>\n'
                          '<b>Wind:</b> ESE 7 km/h<br/>\n'
                          '<b>Air Quality Health '
                          'Index:</b> N/A <br/>',
                          '@type': 'html'},
              'title': 'Current Conditions: 24.2°C',
              'updated': '2016-09-04T19:00:00Z'},
             {'category': {'@term': 'Weather Forecasts'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc1:20160904150000',
              'link':
              {'@href':
               'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
               '@type': 'text/html'},
              'published': '2016-09-04T15:00:00Z',
              'summary': {'#text': 'Sunny. High 26. Humidex 28. '
                          'UV index 7 or high. Forecast '
                          'issued 11:00 AM EDT Sunday 04 '
                          'September 2016',
                          '@type': 'html'},
              'title': 'Sunday: Sunny. High 26.',
              'updated': '2016-09-04T15:00:00Z'},
             {'category': {'@term': 'Weather Forecasts'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc2:20160904150000',
              'link':
              {'@href':
               'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
               '@type': 'text/html'},
              'published': '2016-09-04T15:00:00Z',
              'summary': {'#text': 'Clear. Low 8. Forecast issued '
                          '11:00 AM EDT Sunday 04 '
                          'September 2016',
                          '@type': 'html'},
              'title': 'Sunday night: Clear. Low 8.',
              'updated': '2016-09-04T15:00:00Z'},
             {'category': {'@term': 'Weather Forecasts'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc3:20160904150000',
              'link':
              {'@href':
               'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
               '@type': 'text/html'},
              'published': '2016-09-04T15:00:00Z',
              'summary': {'#text': 'Sunny. High 27. Humidex 30. '
                          'Forecast issued 11:00 AM EDT '
                          'Sunday 04 September 2016',
                          '@type': 'html'},
              'title': 'Monday: Sunny. High 27.',
              'updated': '2016-09-04T15:00:00Z'}, {
                  'category': {'@term': 'Weather Forecasts'},
                  'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc4:20160904150000',
                  'link':
                  {'@href':
                   'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
                   '@type': 'text/html'},
                  'published': '2016-09-04T15:00:00Z',
                  'summary': {'#text': 'Clear. Low 9. Forecast issued '
                              '11:00 AM EDT Sunday 04 '
                              'September 2016',
                              '@type': 'html'},
                  'title': 'Monday night: Clear. Low 9.',
                  'updated': '2016-09-04T15:00:00Z'
              }, {'category': {'@term': 'Weather Forecasts'},
                  'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc5:20160904150000',
                  'link':
                  {'@href':
                   'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
                   '@type': 'text/html'},
                  'published': '2016-09-04T15:00:00Z',
                  'summary': {'#text': 'Sunny. High 28. Forecast '
                              'issued 11:00 AM EDT Sunday 04 '
                              'September 2016',
                              '@type': 'html'},
                  'title': 'Tuesday: Sunny. High 28.',
                  'updated': '2016-09-04T15:00:00Z'},
             {'category': {'@term': 'Weather Forecasts'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc6:20160904150000',
              'link':
              {'@href':
               'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
               '@type': 'text/html'},
              'published': '2016-09-04T15:00:00Z',
              'summary': {'#text': 'Cloudy periods. Low 16. '
                          'Forecast issued 11:00 AM EDT '
                          'Sunday 04 September 2016',
                          '@type': 'html'},
              'title': 'Tuesday night: Cloudy periods. Low 16.',
              'updated': '2016-09-04T15:00:00Z'}, {
                  'category': {'@term': 'Weather Forecasts'},
                  'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc7:20160904150000',
                  'link':
                  {'@href':
                   'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
                   '@type': 'text/html'},
                  'published': '2016-09-04T15:00:00Z',
                  'summary': {'#text': 'A mix of sun and cloud with '
                              '30 percent chance of showers. '
                              'High 29. Forecast issued '
                              '11:00 AM EDT Sunday 04 '
                              'September 2016',
                              '@type': 'html'},
                  'title': 'Wednesday: Chance of showers. High 29. POP '
                  '30%',
                  'updated': '2016-09-04T15:00:00Z'
              }, {'category': {'@term': 'Weather Forecasts'},
                  'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc8:20160904150000',
                  'link':
                  {'@href':
                   'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
                   '@type': 'text/html'},
                  'published': '2016-09-04T15:00:00Z',
                  'summary': {'#text': 'Cloudy periods with 30 '
                              'percent chance of showers. '
                              'Low 17. Forecast issued 11:00 '
                              'AM EDT Sunday 04 September '
                              '2016',
                              '@type': 'html'},
                  'title': 'Wednesday night: Chance of showers. Low '
                  '17. POP 30%',
                  'updated': '2016-09-04T15:00:00Z'},
             {'category': {'@term': 'Weather Forecasts'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc9:20160904150000',
              'link':
              {'@href':
               'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
               '@type': 'text/html'},
              'published': '2016-09-04T15:00:00Z',
              'summary': {'#text': 'A mix of sun and cloud with '
                          '40 percent chance of showers. '
                          'High 24. Forecast issued '
                          '11:00 AM EDT Sunday 04 '
                          'September 2016',
                          '@type': 'html'},
              'title': 'Thursday: Chance of showers. High 24. POP '
              '40%',
              'updated': '2016-09-04T15:00:00Z'},
             {'category': {'@term': 'Weather Forecasts'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc10:20160904150000',
              'link':
              {'@href':
               'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
               '@type': 'text/html'},
              'published': '2016-09-04T15:00:00Z',
              'summary': {'#text': 'Cloudy periods with 30 '
                          'percent chance of showers. '
                          'Low 15. Forecast issued 11:00 '
                          'AM EDT Sunday 04 September '
                          '2016',
                          '@type': 'html'},
              'title': 'Thursday night: Chance of showers. Low 15. '
              'POP 30%',
              'updated': '2016-09-04T15:00:00Z'}, {
                  'category': {'@term': 'Weather Forecasts'},
                  'id':
                  'tag:weather.gc.ca,2013-04-16:on-1_fc11:20160904150000',
                  'link':
                  {'@href':
                   'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
                   '@type': 'text/html'},
                  'published': '2016-09-04T15:00:00Z',
                  'summary': {'#text': 'A mix of sun and cloud. High '
                              '24. Forecast issued 11:00 AM '
                              'EDT Sunday 04 September 2016',
                              '@type': 'html'},
                  'title': 'Friday: A mix of sun and cloud. High 24.',
                  'updated': '2016-09-04T15:00:00Z'
              }, {'category': {'@term': 'Weather Forecasts'},
                  'id':
                  'tag:weather.gc.ca,2013-04-16:on-1_fc12:20160904150000',
                  'link':
                  {'@href':
                   'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
                   '@type': 'text/html'},
                  'published': '2016-09-04T15:00:00Z',
                  'summary': {'#text': 'Cloudy periods. Low 12. '
                              'Forecast issued 11:00 AM EDT '
                              'Sunday 04 September 2016',
                              '@type': 'html'},
                  'title': 'Friday night: Cloudy periods. Low 12.',
                  'updated': '2016-09-04T15:00:00Z'},
             {'category': {'@term': 'Weather Forecasts'},
              'id': 'tag:weather.gc.ca,2013-04-16:on-1_fc13:20160904150000',
              'link':
              {'@href':
               'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
               '@type': 'text/html'},
              'published': '2016-09-04T15:00:00Z',
              'summary': {'#text': 'A mix of sun and cloud with '
                          '30 percent chance of showers. '
                          'High 21. Forecast issued '
                          '11:00 AM EDT Sunday 04 '
                          'September 2016',
                          '@type': 'html'},
              'title': 'Saturday: Chance of showers. High 21. POP '
              '30%',
              'updated': '2016-09-04T15:00:00Z'}],
            'icon':
            'http://www.weather.gc.ca/template/gcweb/assets/favicon.ico',
            'id': 'tag:weather.gc.ca,2013-04-16:20160904190214',
            'link': [{'@href':
                      'http://www.weather.gc.ca/city/pages/on-1_metric_e.html',
                      '@rel': 'related',
                      '@type': 'text/html'},
                     {'@href': 'http://www.weather.gc.ca/rss/city/on-1_e.xml',
                      '@rel': 'self',
                      '@type': 'application/atom+xml'},
                     {'@href': 'http://www.meteo.gc.ca/rss/city/on-1_f.xml',
                      '@hreflang': 'fr-ca',
                      '@rel': 'alternate',
                      '@type': 'application/atom+xml'}],
            'logo':
            'http://www.weather.gc.ca/template/gcweb/assets/wmms-alt.png',
            'rights': 'Copyright 2016, Environment Canada',
            'title': 'Algonquin Park (Brent) - Weather - Environment Canada',
            'updated': '2016-09-04T19:02:14Z'
        }}

    def test_meta_schema(self):
        data = self.data['feed']
        self.assertIsInstance(validators.META_SCHEMA(data), dict)
        self.assertIn('lang', validators.META_SCHEMA(data))
        self.assertNotIn('@xml:lang', validators.META_SCHEMA(data))

    @patch('weathergc.forecast.Forecast.refresh')
    def test_entry_schema(self, mock_refresh):
        data = self.data
        obj = Forecast('on-1')
        obj._source = obj._parse(data)
        parsed = obj._parse(data)

        self.assertIsInstance(parsed, dict)
        self.assertEqual(len(parsed), 4)

    @patch('weathergc.forecast.Forecast.refresh')
    def test_warnings_and_watches_transformation(self, mock_refresh):
        data = self.data
        obj = Forecast('on-1')
        obj._source = obj._parse(data)

        x = obj._transform_warnings_and_watches()['Warnings and Watches']
        self.assertIsInstance(x, list)
        self.assertEqual(len(x), 1)
        self.assertEqual(
            x[0]['title'],
            'No watches or warnings in effect, Algonquin Park (Brent)')

    @patch('weathergc.forecast.Forecast.refresh')
    def test_weather_forecasts_transformation(self, mock_refresh):
        data = self.data
        obj = Forecast('on-1')
        obj._source = obj._parse(data)

        x = obj._transform_weather_forecasts()['Weather Forecasts']
        self.assertIsInstance(x, list)
        self.assertEqual(len(x), 13)
        self.assertEqual(x[0]['title'], 'Sunday: Sunny. High 26.')

    @patch('weathergc.forecast.Forecast.refresh')
    def test_current_conditions_transformation(self, mock_refresh):
        data = self.data
        obj = Forecast('on-1')
        obj._source = obj._parse(data)

        x = obj._transform_current_conditions()['Current Conditions']
        self.assertIsInstance(x, list)
        self.assertEqual(len(x), 1)
        self.assertEqual(x[0]['title'], 'Current Conditions: 24.2 C')


class TestLive(unittest.TestCase):
    def setUp(self):
        pass

    def test_current_conditions(self):
        obj = Forecast('on-82')
        x = obj._transform_current_conditions()['Current Conditions']
        self.assertIsInstance(x, list)
        self.assertEqual(len(x), 1)
        self.assertIn('Current Conditions', x[0]['title'])
