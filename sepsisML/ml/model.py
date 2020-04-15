import pickle
from eli5.sklearn.explain_prediction import explain_prediction_linear_classifier, explain_prediction_tree_classifier
from eli5.formatters.as_dict import format_as_dict

from sepsisML.ml.features import FEATURES

import os

def predict(data, model='random-forest'):
    print(os.getcwd())
    model_path = 'sepsisML/ml/LogisticRegression-20200103.pkl' if model=='logistic-regression' else 'sepsisML/ml/RandomForest-20200103.pkl'
    loaded_model = pickle.load(open(model_path, 'rb'))
    new_data = data.copy()
    new_data['prediction']="Negative" if loaded_model.predict(data[FEATURES])==0 else "Positive"
    new_data = new_data['prediction']

    return new_data

def explain(data, model='random-forest'):
    print(os.getcwd())
    model_path = 'sepsisML/ml/LogisticRegression-20200103.pkl' if model=='logistic-regression' else 'sepsisML/ml/RandomForest-20200103.pkl'
    loaded_model = pickle.load(open(model_path, 'rb'))
    
    results = []

    if model=='logistic-regression':
        for idx, row in data.iterrows():
            x = explain_prediction_linear_classifier(loaded_model, row[FEATURES])
            desc = format_as_dict(x)['targets'][0]
            desc['patient'] = idx
            results.append(desc) 

    elif model=='random-forest':
        for idx, row in data.iterrows():
            x = explain_prediction_tree_classifier(loaded_model, row[FEATURES])
            desc = format_as_dict(x)['targets'][0]
            desc['patient'] = idx
            results.append(desc) 
    
    return results
