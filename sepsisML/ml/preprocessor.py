import pandas as pd
from sklearn.model_selection import train_test_split
import pickle

from sepsisML.ml.features import FEATURES, MAP_FEATURES

def preprocess(data):
    target = 'is_sepsis'
    id = 'patient_id'
    sepsis_cols = [i for i in data.columns.tolist() if "Sepsis" in i or "Pseudomonas" in i ]
    hist_cols = [i for i in data.columns.tolist() if "hist" in i]
   
    data.drop(sepsis_cols + hist_cols, inplace=True, axis=1)

    for col in data.columns:
        if col not in FEATURES:
            if col in MAP_FEATURES:
                data[MAP_FEATURES[col]] = data[col]

    for feature in FEATURES:
        if feature not in data.columns:
            data[feature] = 0
    for col in data.columns:
        if col not in FEATURES and col!='patient':
            data.drop(col, inplace=True, axis=1)
    
    numeric_cols = sorted([i for i in data.columns.tolist() if  i != "gender" 
                                                    and i != id 
                                                    and i != target
                                                    and i != 'birthDate' ])

    # from sklearn.preprocessing import StandardScaler
    # scaler = pickle.load(open("StandardScaler-20200102.pkl", 'rb'))
    # data[numeric_cols] = scaler.transform(data[numeric_cols])

    return data

