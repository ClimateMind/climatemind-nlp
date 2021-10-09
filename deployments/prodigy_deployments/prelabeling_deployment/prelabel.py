import pandas as pd


def build_prelabel_dict(csv_path: str) -> dict:
    """ TODO: Add description """
    pattern_matcher_df = pd.read_csv(csv_path)
    pattern_dict = {}
    for column in pattern_matcher_df:
        for value in pattern_matcher_df[column].values:
            if value != None or value != '' or value != 'NaN':
                pattern_dict[value] = column
    
    return pattern_dict