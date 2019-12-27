import pickle
from eli5.sklearn.explain_prediction import explain_prediction_linear_classifier
from eli5.formatters.as_dict import format_as_dict

def predict(data, model='default'):
    model_path = 'LogisticRegression-20191216.pkl'
    loaded_model = pickle.load(open(model_path, 'rb'))
    new_data = data.copy()
    new_data['prediction']="Negative" if loaded_model.predict(data)==0 else "Positive"
    new_data = new_data['prediction']
    data.to_csv("Fooo.csv")

    return new_data

def explain(data, model='default'):
    model_path = 'LogisticRegression-20191216.pkl'
    loaded_model = pickle.load(open(model_path, 'rb'))
    
    results = []

    for idx, row in data.iterrows():
        x = explain_prediction_linear_classifier(loaded_model, row)
        desc = format_as_dict(x)['targets'][0]
        desc['patient'] = idx
        results.append(desc) 
    
    return results
