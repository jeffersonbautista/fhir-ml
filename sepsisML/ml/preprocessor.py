import pandas as pd
from sklearn.model_selection import train_test_split

from sepsisML.ml.features import FEATURES

def preprocess(data):
    sepsis_cols = [i for i in data.columns.tolist() if "Sepsis" in i]
    data.drop(sepsis_cols, inplace=True, axis=1)

    for feature in FEATURES:
        if feature not in data.columns:
            data[feature] = 0
    for col in data.columns:
        if col not in FEATURES and col!='patient':
            data.drop(col, inplace=True, axis=1)

    return data

