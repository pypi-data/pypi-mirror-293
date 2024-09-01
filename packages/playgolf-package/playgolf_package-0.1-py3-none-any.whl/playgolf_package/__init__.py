from .decision_tree import id3, classify
import pandas as pd

def load_data():
    df_train = pd.read_csv('playgolf_data.csv')
    df_test = pd.read_csv('playgolf_test.csv')
    return df_train, df_test
