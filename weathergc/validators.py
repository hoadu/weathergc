# -*- coding: utf-8 -*-
'''Schema definitions
'''
import sys

from voluptuous import (ALLOW_EXTRA, REMOVE_EXTRA, All, Any, Remove, Replace,
                        Schema, SetTo)
from voluptuous.util import Strip

from weathergc.utils import html_to_dict

is_python3 = sys.version_info.major == 3
if is_python3:
    unicode = str

# top level validator, ensure we're dealing with a known file format
META_SCHEMA = Schema(
    {All('@xml:lang', SetTo('lang')): 'en-ca',
     Remove('@xmlns'): 'http://www.w3.org/2005/Atom',
     'author': {'name': 'Environment Canada',
                'uri': 'http://www.weather.gc.ca'},
     'logo': unicode,
     'rights': unicode,
     'title': unicode,
     'updated': unicode,
     Remove('entry'): Any(list, dict)},
    extra=REMOVE_EXTRA)

# Validator for each member of the 'entry' list in the feed.
# Includes some minor transformations to simplify later validations
ENTRY_SCHEMA = Schema(
    {'category': All({'@term': Any('Weather Forecasts', 'Current Conditions',
                                   'Warnings and Watches')}, dict.values,
                     ''.join),
     Remove('id'): unicode,
     Remove('link'):
     {'@href': unicode,
      '@type': 'text/html'},
     'published': unicode,
     'summary': All({'#text': unicode,
                     Remove('@type'): 'html'}, dict.values, ''.join),
     'title': unicode,
     'updated': unicode},
    extra=REMOVE_EXTRA)

WW_SCHEMA = Schema({Remove('category'): unicode}, extra=ALLOW_EXTRA)

CC_SCHEMA = Schema(
    {Remove('category'): unicode,
     All('summary', SetTo('data')):
     All(Replace('&deg;', ' '), Replace(u'\N{DEGREE SIGN}', ' '),
         html_to_dict),
     'title': All(Replace('&deg;', ' '), Replace(u'\N{DEGREE SIGN}', ' '))},
    extra=ALLOW_EXTRA)

WF_SCHEMA = Schema({Remove('category'): unicode,
                    'summary': All(Replace('Forecast issued.*$', ''), Strip),
}, extra=ALLOW_EXTRA)
