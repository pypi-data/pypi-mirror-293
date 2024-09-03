# tests/test_pandas_profiling_manual.py

import pandas as pd
from pandas_profiling_manual import profile_report

def test_profile_report():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    profile_report(df)
