from dotlab.data_analysis import get_distribution

import pandas as pd


def test_get_distribution():
    df_input = pd.DataFrame({
        'col1': [1.0, 2.0, 3.0],
        'col2': [0.0, 1.0, 0.0],
        'target': [0.0, 1.0, 1.0]
    })
    
    expected_output = pd.DataFrame({
        'Attributes': ['col1', 'col2:0.0', 'col2:1.0'],
        'Total': ['2.0 (1.0)', '2/3 (66.7)', '1/3 (33.3)'],
        'target:0.0': ['1.0 (0.0)', '1/1 (100.0)', '-'],
        'target:1.0': ['2.5 (0.7)', '1/2 (50.0)', '1/2 (50.0)'],
    })
    
    output =  get_distribution(df_input, 'target', ['col1'])
    
    assert output.equals(expected_output)
