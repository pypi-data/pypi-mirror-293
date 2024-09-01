import pandas as pd
import pkg_resources

def load_data():
    # Access the data files included in the package
    data_path = pkg_resources.resource_filename(__name__, 'playgolf_data.csv')
    test_path = pkg_resources.resource_filename(__name__, 'playgolf_test.csv')
    df_train = pd.read_csv(data_path)
    df_test = pd.read_csv(test_path)
    return df_train, df_test

# You can also include other functions and classes here
from .decision_tree import id3, classify
