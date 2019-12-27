import traceback
from sepsisML.parser.cleaner import utils

def extract_measure(x):
    x = eval(x) if type(x) != dict else x
    try:
        if 'valueQuantity' in x.keys():
            return x['valueQuantity']['unit']
        if 'component' in x.keys():
            if 'valueQuantity' not in  x['component'][1].keys():
                return (x['component'][1]['code']['coding'][0]['display'])
            return x['component'][1]['valueQuantity']['unit']
        if 'valueCodeableConcept' in x.keys():
            return x['valueCodeableConcept']['coding'][0]['display']
    except Exception as e:
        # print(traceback.format_exc())
        # print(x)
        return None

def extract_value(x):
    x = eval(x) if type(x) != dict else x
    try:
        if 'valueQuantity' in x.keys():
            return x['valueQuantity']['value']
        if 'component' in x.keys():
            if 'valueQuantity' not in  x['component'][1].keys():
                return 0
            return x['component'][1]['valueQuantity']['value']
        if 'valueCodeableConcept' in x.keys():
            return int(x['valueCodeableConcept']['coding'][0]['display'] != "Never smoker")
    except Exception as e:
        # print(traceback.format_exc())
        # print(x)
        return None

def extract_procedure(x):
    x = eval(x) if type(x) != dict else x

    try:
        return (x['code']['coding'][0]['display'].encode('ascii', 'ignore')).decode("utf-8").replace(" ", "_")
    except:
        # print(traceback.format_exc())
        # print(x)
        return None

def extract_patient(x):
    x = eval(x) if type(x) != dict else x
    x = x['subject']
    try:
        if 'Reference' in x.keys():
            return x['Reference'].split('/')[-1]
        elif 'reference' in x.keys():
            return x['reference'].split('/')[-1]
    except:
        # print(traceback.format_exc())
        # print(x)
        return None