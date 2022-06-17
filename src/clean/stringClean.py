import pandas as pd
import numpy as np

class CleanString():
    
    @classmethod
    def cleanString(cls, df, col_name) -> pd.DataFrame:
        
        df[col_name] = df[col_name].astype(str)
        
        df.loc[pd.isna(df[col_name]), col_name]=''
        df.loc[:, col_name]= df.loc[:, col_name].str.upper()
        df.loc[:, col_name]= df.loc[:, col_name].str.lstrip()
        df.loc[:, col_name]= df.loc[:, col_name].str.rstrip()
        
        replaceDict = {"-":" ",";":"", "Ã³":"O", "Ã":"O", "Ï¿½":"O", "Á":"A", "É":"E", "Í":"I", "Ó":"O", "Ú":"U", "À":"A", "È":"E", "Ì":"I", "Ò":"O", "Ù":"U", "#¡VALOR!":"", "#¡REF!":"", "ﾓ":"O", "Â¥":"N", "Ã‹":"O", "ÂŽ":"O", "Â¢":"O", "Â°":"O", "Â":"", "â€˜":"N", "â€œ":"O", "\r\n":" ", "\r":" ", "\n":" ", " – ":"-", " - ":"-", "|":" ", "\.0+$":"", "\.0+$":"", "0X2A":"", "0X17":"", ' +':' ','DOBLE COBRO ':'','ÃÂÃÂ³':'o','U;O':'UÑO','&#323;':'N','&#262;':'C','&#7742;':'M','&#7764;': 'P','&#313;': 'L', '&#340;':'R', '&#358;': 'T', "\"":"" }
        
        for key,value in replaceDict.items():
            df.loc[:, col_name]= df.loc[:, col_name].str.replace(key, value, regex=True)
           
        df[col_name]= df[col_name].apply(lambda x: x.replace('NAN','') if 'NAN' in x and len(x)==3 else x)
        df[col_name]= df[col_name].apply(lambda x: x.replace('nan','') if 'nan' in x and len(x)==3 else x)
        df[col_name]= df[col_name].apply(lambda x: x.replace('0X2A','') if 'nan' in x and len(x)==4 else x)
        df[col_name]= df[col_name].apply(lambda x: x.replace('0X17','') if 'nan' in x and len(x)==4 else x)
    
        df.loc[pd.isna(df[col_name]), col_name]=''
        return df