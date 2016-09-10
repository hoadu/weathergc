import re
from urllib import request

city_base = 'https://weather.gc.ca/rss/city/prov-city_e.xml'
prov_base = 'https://weather.gc.ca/forecast/canada/index_e.html?id='

provinces = ['ON', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'PE', 'QC', 'SK',
             'YT']

urls_pattern = re.compile(
    r'<li><a href="/city/pages/(.*)_metric_e.html">.*</a></li>', re.MULTILINE)

for province in provinces:
    data = request.urlopen(prov_base + province).read()  #bytes
    body = data.decode('utf-8')
    cities = list(set(urls_pattern.findall(body)))
    for city in cities:
        city_url = city_base.replace('prov-city', city)
        city_file = 'data/%s.xml' % city
        print('Saving %s to %s' % (city_url, city_file))
        pfile = request.urlretrieve(city_url, city_file)
