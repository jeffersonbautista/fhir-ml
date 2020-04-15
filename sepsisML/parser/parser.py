import pandas as pd

from sepsisML.model import *
from sepsisML import logger
from sepsisML.errors import PatientNotFound, InvalidId, NotEnoughData
from sepsisML.request_handler import request_handler
from sepsisML.parser.cleaner import conditions, observations, utils
from sepsisML import settings

def combine(dfs):
    try:
        df_ = pd.concat([dfs[0], dfs[1]], axis=1, join='inner')
        df_ = utils.remove_unnamed(df_)
        for df in dfs[2:]:
            df_ = pd.concat([df_, df], axis=1, join='inner')
            df_ = utils.remove_unnamed(df_)
        
        return df_
    except IndexError:
        raise NotEnoughData("Not enough data")


def get_fhir_data(patient_id, endpoint, version):
    for patient in patient_id:
        logger.info("- Getting patient data")
        df_patient = get_patient(patient, endpoint, version)

        logger.info("- Getting observations data")
        df_observation = get_observations(patient, endpoint, version)

        logger.info("- Getting conditions data")
        df_condition = get_conditions(patient, endpoint, version)

        logger.info("- Merging of data")
        raw_combinelist = [df_patient, df_observation, df_condition]
        combinelist = [dataframe for dataframe in raw_combinelist if dataframe is not None]
        df_final = combine(combinelist)
        
    return df_final

""" ============ PATIENT EXTRACTION: ============ """

def get_patient_generic(raw_patient):
    # http://localhost:5656/api/v1/predict?patient=fc200fa2-12c9-4276-ba4a-e0601d424e55&endpoint=smart&version=4
    # http://localhost:5656/api/v1/predict?patient=smart-7321938&endpoint=smart&version=3
    # http://localhost:5656/api/v1/predict?patient=8ab4791f-0790-44f3-97c0-88f14c9329da&endpoint=smart&version=2

    df_patient = pd.DataFrame([raw_patient])

    df_patient['gender'] = df_patient['gender'].apply(lambda x: 1 if x.lower()=="male" else 0).values[0] if key_exist(df_patient, 'gender') else -1

    try:
        df_patient['id'] = df_patient['id'].apply(lambda x: utils.remove_prefix(x))
    except KeyError:
        raise InvalidId("Invalid patient ID")     

    df_patient.set_index('id', inplace=True)
    return df_patient


def get_patient(patient, endpoint, version):   
    raw_patient = request_handler.fhir( id=patient, api='Patient', server=endpoint, version=version)
    return eval(settings.MAP_ENDPOINT[endpoint]['version'][version]['get_patient'])(raw_patient)

""" ============ OBSERVATION EXTRACTION: ============ """

def get_observations_generic(raw_observations):
    try:
        df_observation = pd.DataFrame(raw_observations['entry'])
    except:
        return None
    
    df_observation['procedure'] = df_observation['resource'].apply(lambda x: observations.extract_procedure(x))
    
    df_observation['measurement'] =  df_observation['resource'].apply(lambda x: observations.extract_measure(x))
    df_observation['value'] = df_observation['resource'].apply(lambda x: observations.extract_value(x))
    df_observation['id'] = df_observation['fullUrl'].apply(lambda x: utils.remove_prefix(x))
    df_observation['patient'] = df_observation['resource'].apply(lambda x: observations.extract_patient(x))
    # df_observation['procedure'] = utils.create_others(df_observation, 'procedure', 'id')

    df_obs_pivot = df_observation.pivot_table(index='patient', columns='procedure', values='value', aggfunc = 'mean')
    df_obs_pivot.fillna(0, inplace=True)

    return df_obs_pivot


def get_observations(patient, endpoint, version):
    raw_observations = request_handler.fhir( id=patient, api='Observation', server=endpoint, version=version)
    return eval(settings.MAP_ENDPOINT[endpoint]['version'][version]['get_observations'])(raw_observations)

""" ============ CONDITIONS EXTRACTION: ============ """

def get_conditions_generic(raw_conditions):
    try:
        df_condition = pd.DataFrame(raw_conditions['entry'])
    except Exception:
        return None

    df_condition = conditions.extract_condition_data(df_condition)
    df_condition = conditions.filter_out_after_sepsis(df_condition)
    df_condition['conditions'] = df_condition['conditions'].apply(lambda x: utils.parse_unicode(x))

    # df_condition['conditions'] = utils.create_others(df_condition, 'conditions', 'id')
    df_condition['conditions'] = df_condition['conditions'].apply(lambda x: utils.underscoreify(x))
    df_condition = utils.dummify(df_condition, ['conditions'], prefix='hist')
    df_condition['patient'] = df_condition['patient'].apply(lambda x: utils.remove_prefix(x))
    df_condition = df_condition.groupby('patient').sum()

    return df_condition

def get_conditions_smart(raw_conditions):
    try:
        df_condition = pd.DataFrame(raw_conditions['entry'])
    except Exception:
        return None

    df_condition = conditions.extract_condition_data_smart(df_condition)
    df_condition = conditions.filter_out_after_sepsis(df_condition)
    df_condition['conditions'] = df_condition['conditions'].apply(lambda x: utils.parse_unicode(x))

    # df_condition['conditions'] = utils.create_others(df_condition, 'conditions', 'id')
    df_condition['conditions'] = df_condition['conditions'].apply(lambda x: utils.underscoreify(x))
    df_condition = utils.dummify(df_condition, ['conditions'], prefix='hist')
    df_condition['patient'] = df_condition['patient'].apply(lambda x: utils.remove_prefix(x))
    df_condition = df_condition.groupby('patient').sum()

    return df_condition

def get_conditions_smart2(raw_conditions):
    try:
        df_condition = pd.DataFrame(raw_conditions['entry'])
    except Exception:
        return None

    df_condition = conditions.extract_condition_data_smart2(df_condition)
    df_condition = conditions.filter_out_after_sepsis(df_condition)
    df_condition['conditions'] = df_condition['conditions'].apply(lambda x: utils.parse_unicode(x))

    # df_condition['conditions'] = utils.create_others(df_condition, 'conditions', 'id')
    df_condition['conditions'] = df_condition['conditions'].apply(lambda x: utils.underscoreify(x))
    df_condition = utils.dummify(df_condition, ['conditions'], prefix='hist')
    df_condition['patient'] = df_condition['patient'].apply(lambda x: utils.remove_prefix(x))
    df_condition = df_condition.groupby('patient').sum()

    return df_condition

def get_conditions(patient, endpoint, version):
    raw_conditions = request_handler.fhir( id=patient, api='Condition', server=endpoint, version=version)
    return eval(settings.MAP_ENDPOINT[endpoint]['version'][version]['get_conditions'])(raw_conditions)


def key_exist(data, key):
    try:
        data[key]
        return True
    except KeyError:
        return False