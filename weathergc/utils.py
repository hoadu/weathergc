'''Utility functions.'''
import re


def html_to_dict(html):
    '''Return dict of key/value when html matches the following structure:
    <b>key</b>value<br/>
    '''
    pattern = re.compile(r'<b>(.*):.*</b>(.*)<br/>')
    return dict([(x[0].strip(), x[1].strip()) for x in pattern.findall(html)])


def list_iter(obj):
    '''Ensure obj is either a list, or is converted to one.'''
    if obj:
        return obj if isinstance(obj, list) else [obj]
    else:
        return []
