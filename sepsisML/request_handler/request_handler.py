import requests

from sepsisML import settings
from sepsisML import logger
from sepsisML.errors import PatientNotFound, InvalidVersion
from sepsisML.request_handler.fhir_servers import SERVERS


def _slasher(string):
    return string + '/' if string[-1] != '/' else string

def fhir(id, api, server, version):
   
    _ = settings.MAP_ENDPOINT[server]['version']
    if version not in _.keys():
        raise InvalidVersion("Invalid version")
    
    url = _[version]['url']
    url = _slasher(url)

    if api=='Patient':
        api = _slasher(api)
        uri = url+api+id+'?'
    else:
        uri = url+api+'?patient='+id+'&'

    for k,v in settings.MAP_ENDPOINT[server]['params'].items():
        uri += "{}={}&".format(k,v)

    # uri = "{url}{api}{patient}?apikey={apikey}".format(url=url, api=api, patient=id, apikey=settings.APIKEY) \
    #             if api == "Patient/" else "{url}{api}?apikey={apikey}&patient={patient}".format(url=url, api=api, apikey=settings.APIKEY, patient=id)
    
    logger.info("-- Accesing {} ...".format(uri))
    raw_data = requests.get(uri).json()

    if 'storage_error' in str(raw_data) or 'error' in str(raw_data):
        if api=="Patient/":
            raise PatientNotFound("Patient cannot be found")

    return raw_data