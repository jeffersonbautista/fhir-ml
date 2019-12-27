import pandas as pd

def parse_unicode(x):
    try:
        return (x.encode('ascii', 'ignore')).decode("utf-8")
    except:
        return None

def underscoreify(x):
    return str(x).replace(" ", "_")

def dummify(data, cat_cols, prefix):
    catdf = pd.get_dummies(data[cat_cols], prefix = prefix)
    data = pd.concat([data, catdf], axis=1)
    return data

def remove_prefix(x):
    try:
        return str(x).split("/")[-1]
    except:
        return None

def create_others(df, group_col, agg_col, measure=2, trans="count"):
    df['_temp'] = df.groupby(group_col)[agg_col].transform(trans)
    df[group_col] = df[['_temp', group_col]].apply(lambda x: 'others' if x['_temp'] < measure else x[group_col], axis=1)
    df.drop('_temp', axis=1, inplace=True)

    return df[group_col]

def remove_unnamed(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]


def find_using_key(query, dictionary):
    """ 
        General utility function that 
    """
    if isinstance(dictionary,str):
        dictionary = eval(stringify(dictionary))

    for k, v in dictionary.items():
        if k==query:
            yield v
        elif isinstance(v, dict):
            for result in find_using_key(query, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find_using_key(query, d):
                    yield result


def nested_key_search(keys, agent):
    ret = agent
    for key in keys:
        ret = list(find_using_key(key, ret))[0]
    return ret