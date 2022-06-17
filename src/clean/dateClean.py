import pandas as pd

class CleanDate():
    
    @classmethod
    def cleanDate(cls, df, col_name) -> pd.DataFrame:
        
        df[col_name] = pd.to_datetime(df[col_name],dayfirst=True).dt.date
        
        #Fecha Nula
        df[col_name] = df[col_name].astype(str)
        
        df.loc[:, col_name]= df.loc[:, col_name].str.rstrip()
        df.loc[:, col_name]= df.loc[:, col_name].str.lstrip()
        df[col_name].replace({';': ''}, inplace=True)
        df[col_name].replace({'nan': ''}, inplace=True)
        df[col_name].replace({'NAN': ''}, inplace=True)
    
        
        df[col_name]= df[col_name].apply(lambda x: x.replace('NaT','') if 'NaT' in x  else x)
        df[col_name]= df[col_name].apply(lambda x: x.replace('NAT','') if 'NAT' in x  else x)
        

        
        #Arreglar formato fecha
        df.loc[:, col_name]= df.loc[:, col_name].str.lstrip()
        df.loc[:, col_name]= df.loc[:, col_name].str.rstrip()
        df.loc[:, col_name]= df.loc[:, col_name].str.replace(";", "")
        fechas_seriales= df.loc[(~ df[col_name].str.contains(":", na = True)), col_name]
        fechas_seriales= df.loc[(df[col_name].str.contains(".", na = True)), :]
        fechas_seriales= fechas_seriales.loc[(~ fechas_seriales[col_name].str.contains("-", na = True)), :]
        fechas_seriales= fechas_seriales.loc[(~ fechas_seriales[col_name].str.contains("/", na = True)), :]
        fechas_seriales= fechas_seriales.loc[(~ fechas_seriales[col_name].str.contains("NaT", na = True)), :]
        fechas_seriales= fechas_seriales.loc[(~ fechas_seriales[col_name].str.contains("nan",)), col_name]
        fechas_seriales= fechas_seriales.index
        if len(fechas_seriales) > 0:
            df.loc[fechas_seriales, col_name]= pd.to_datetime((pd.to_numeric(df.loc[fechas_seriales, col_name])- 25569) * 86400.0, unit='s').astype(str)
        
        
        df[col_name]= df[col_name].apply(lambda x: x.split('.')[0] if '.' in x and 'nan' not in x and "NaT" not in x  else x)
        
        
        #df[col_name] = df[col_name].astype('datetime64[ns]')        
        df[col_name] = pd.to_datetime(df[col_name]).dt.strftime('%d/%m/%Y')
        
        return df