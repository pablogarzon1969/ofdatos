import pandas as pd

class CleanDecimal():
    
    @classmethod
    def cleanDecimal(cls, df, col_name) -> pd.DataFrame:
        #Elimina todos los caracteres no numericos o punto. Se cambia la coma por punto
        df[col_name] = df[col_name].astype(str)
        df.loc[:, col_name]= df.loc[:, col_name].str.replace(",", ".")
        df[col_name] = df[col_name].str.replace(r'[^0-9.]+', '')
        df[col_name] = df[col_name].astype(float)        
        return df