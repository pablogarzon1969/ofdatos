import pandas as pd
import numpy as np

class CleanNumeric():
    
    @classmethod
    def cleanNumeric(cls, df, col_name) -> pd.DataFrame:
    
        df[col_name] = df[col_name].astype(str)    

        df.loc[:, col_name]= df.loc[:, col_name].str.lstrip()
        df.loc[:, col_name]= df.loc[:, col_name].str.rstrip()   
        df.loc[:, col_name]= df.loc[:, col_name].str.replace(";", "")
        df.loc[:, col_name]= df.loc[:, col_name].str.split('.').str[0]
    
        df[col_name].replace({'nan': '0'}, regex=True, inplace=True)
        df[col_name].replace({'NAN': '0'}, regex=True, inplace=True)
        df[col_name].replace({'': np.nan}, regex=True, inplace=True)
        df[col_name].replace({'None': np.nan}, regex=True, inplace=True)
        
        df[col_name] = df[col_name].fillna('0').astype('int64')
        
        return df