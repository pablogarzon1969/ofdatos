import pandas as pd

class CleanInteger():
    
    @classmethod
    def cleanInteger(cls, df, col_name) -> pd.DataFrame:
        #Por ahora si hay valores vacios o NaN o #REF no puede convertir la columna a INT
        df[col_name] = df[col_name].astype(str)
        df[col_name] = df[col_name].str.replace(r'[^0-9]+', '')
        df[col_name] = df[col_name].astype(int)
        return df