import pandas as pd

class CleanAlphabetic():
    
    @classmethod
    def cleanAlphabetic(cls, df, col_name) -> pd.DataFrame:
        df[col_name] = df[col_name].str.replace('[^a-zA-Z ]', '', regex = True)
        return df