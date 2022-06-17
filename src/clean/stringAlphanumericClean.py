import pandas as pd

class CleanAlphanumeric():
    
    @classmethod
    def cleanAlphanumeric(cls, df, col_name) -> pd.DataFrame:
        df[col_name] = df[col_name].str.replace(' +', ' ')
        #Elimina todos los carácteres no alfanumericos incluyendo los espacios
        df[col_name] = df[col_name].str.replace('[^a-zA-Z0-9]', '') 
        return df