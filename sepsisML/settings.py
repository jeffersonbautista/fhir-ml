
import os
import json
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application root
APP_STATIC = os.path.join(APP_ROOT, 'static')

with open('{}/conf/config.json'.format(APP_ROOT)) as json_data:
    config = json.load(json_data)

FHIR_URL = config['fhir_url']
APIKEY = config['apikey']

MAP_ENDPOINT = config['map_endpoint']

