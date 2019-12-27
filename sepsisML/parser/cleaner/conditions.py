def extract_condition_data(data):
    data['id'] = data['resource'].apply(lambda x: eval(x)['id'] if type(x)!=dict else x['id'])
    data['conditions'] = data['resource'].apply(lambda x:  [i['display'] for i in eval(x)['code']['coding']][0] if type(x)!=dict else [i['display'] for i in x['code']['coding']][0])
    # data['encounter'] = data['resource'].apply(lambda x: eval(x)['context']['reference'] if type(x)!=dict else x['context']['reference'])
    data['patient'] = data['resource'].apply(lambda x: eval(x)['subject']['reference'] if type(x)!=dict else x['subject']['reference'])
    data['onsetDateTime'] = data['resource'].apply(lambda x: eval(x)['onsetDateTime'] if type(x)!=dict else x['onsetDateTime'])
    data['is_sepsis'] = data['conditions'].apply(lambda x: 1 if 'sepsis' in x.lower() else 0 )
    return data

def extract_condition_data_smart(data):
    data['id'] = data['resource'].apply(lambda x: eval(x)['id'] if type(x)!=dict else x['id'])
    data['conditions'] = data['resource'].apply(lambda x:  [i['display'] for i in eval(x)['code']['coding']][0] if type(x)!=dict else [i['display'] for i in x['code']['coding']][0])
    # data['encounter'] = data['resource'].apply(lambda x: eval(x)['encounter']['reference'] if type(x)!=dict else x['encounter']['reference'])
    data['patient'] = data['resource'].apply(lambda x: eval(x)['subject']['reference'] if type(x)!=dict else x['subject']['reference'])
    data['onsetDateTime'] = data['resource'].apply(lambda x: eval(x)['onsetDateTime'] if type(x)!=dict else x['onsetDateTime'])
    data['is_sepsis'] = data['conditions'].apply(lambda x: 1 if 'sepsis' in x.lower() else 0 )
    return data

def extract_condition_data_smart2(data):
    data['id'] = data['resource'].apply(lambda x: eval(x)['id'] if type(x)!=dict else x['id'])
    data['conditions'] = data['resource'].apply(lambda x:  [i['display'] for i in eval(x)['code']['coding']][0] if type(x)!=dict else [i['display'] for i in x['code']['coding']][0])
    # data['encounter'] = data['resource'].apply(lambda x: eval(x)['encounter']['reference'] if type(x)!=dict else x['encounter']['reference'])
    data['patient'] = data['resource'].apply(lambda x: eval(x)['patient']['reference'] if type(x)!=dict else x['patient']['reference'])
    data['onsetDateTime'] = data['resource'].apply(lambda x: eval(x)['onsetDateTime'] if type(x)!=dict else x['onsetDateTime'])
    data['is_sepsis'] = data['conditions'].apply(lambda x: 1 if 'sepsis' in x.lower() else 0 )
    return data

def filter_out_after_sepsis(data):
    _data = data.copy()
    _data = _data.loc[_data['is_sepsis']==1]
    for index,row in _data.iterrows():
        sepsis_patient = row['patient']
        sepsis_datetime = row['onsetDateTime']
        idx = ((data['patient'] == sepsis_patient) & (data['onsetDateTime'] > sepsis_datetime))
        data.drop(data[idx].index, inplace=True)
        
    return data