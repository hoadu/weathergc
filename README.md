![Travis](https://travis-ci.org/jschnurr/weathergc.svg?branch=master)
# Environment Canada weather data parser

weather.gc.ca provides weather forecasts for 768 locations in Canada, on
the website and as atom RSS feeds. The purpose of this library is to
transform this raw data into a python object that helps you easily
integrate weather data into your application.

Environment Canada uses 4-5 character city codes to identify
the location for a given forecasts.  The city code can be found
by navigating to the Local forecast, and examining the URL.

For example:  
```
https://weather.gc.ca/city/pages/on-82_metric_e.html --> on-82  
https://weather.gc.ca/city/pages/ns-19_metric_e.html --> ns-19  
```

# Requirements
- Python 2.7 or 3.4

# Install
```python
pip install weathergc
```
## Usage
weathergc can be used from the command line, or as a library.

### Command line
Calling the script with a city code will return JSON.

```bash
$ python weathergc.py on-82
{
    "meta": {
...
```

### Library
Provide the city code to the constructor, and access the parsed data as either
JSON or a Python dict.

Create the object:  
```python
from weathergc import Forecast
f = Forecast('on-1')
```

Print as JSON string:  
```python
f.as_json()
```

Print as dict:  
```python
f.as_dict()
```

Refresh the data from web source:

```python
f.refresh()
```

# Sample Output
```json
{
    "meta": {
        "title": "Algonquin Park (Brent) - Weather - Environment Canada",
        "lang": "en-ca",
        "author": {
            "name": "Environment Canada",
            "uri": "http://www.weather.gc.ca"
        },
        "logo": "http://www.weather.gc.ca/template/gcweb/assets/wmms-alt.png",
        "updated": "2016-09-05T15:05:22Z",
        "badge": "https://weather.gc.ca/wxlink/wxlink.html?cityCode=on-1&lang=e",
        "rights": "Copyright 2016, Environment Canada"
    },
    "Weather Forecasts": [
        {
            "title": "Monday: Sunny. High 26.",
            "published": "2016-09-05T15:00:00Z",
            "summary": "Sunny. High 26. Humidex 29. UV index 7 or high.",
            "updated": "2016-09-05T15:00:00Z"
        },
        {
            "title": "Monday night: A few clouds. Low 11.",
            "published": "2016-09-05T15:00:00Z",
            "summary": "A few clouds. Fog patches developing overnight. Low 11.",
            "updated": "2016-09-05T15:00:00Z"
        },

...

    ],
    "Warnings and Watches": [
        {
            "title": "No watches or warnings in effect, Algonquin Park (Brent)",
            "published": "2016-08-31T05:15:00Z",
            "summary": "No watches or warnings in effect.",
            "updated": "2016-08-31T05:15:00Z"
        }
    ],
    "Current Conditions": [
        {
            "title": "Current Conditions: 21.1 C",
            "data": {
                "Observed at": "Algonquin Park East Gate 11:00 AM EDT Monday 05 September 2016",
                "Temperature": "21.1 C",
                "Air Quality Health Index": "N/A",
                "Pressure / Tendency": "102.5 kPa falling",
                "Humidex": "24",
                "Wind": "SW 6 km/h",
                "Humidity": "60 %",
                "Dewpoint": "13.1 C"
            },
            "published": "2016-09-05T15:00:00Z",
            "updated": "2016-09-05T15:00:00Z"
        }
    ]
}
```

# Tests
Run all tests:
```bash
tox
```

# Contributing
Updates, additional features or bug fixes are always welcome.

# License
The MIT License (MIT). See LICENCE file for details.
