import pandas as pd

def load_data():
    data = pd.read_csv('seoul_real_estate.csv',parse_dates = ['DEAL_YMD'])
    return data