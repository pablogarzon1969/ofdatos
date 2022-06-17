import pandas as pd
import csv
import os

os.chdir(r"\\Dc2tvffra1\e$\InterCambioDatos\AUTOS\SOAT_FRAUDE\Input")

df = pd.read_csv('AXA_INFORME_RECLAMACIONES_20220404.csv',sep = ';',encoding = 'Latin-1',engine = 'python',
                        index_col = False,keep_default_na = False, quoting = csv.QUOTE_NONE,
                        usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,
                          24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,
                          45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62])
df.columns=['RECLAMACION','TIPO_RECLAMACION','FECHA_RECP_ASEGURADORA','FECHA_RECP_CORIS','ESTADO_ACTUAL','FECHA_ESTADO_ACTUAL','RESPONSABLE_ESTADO','ESTADO_RESERVA','ESTADO_PAGO','VALOR_RESERVADO','VALOR_COBRADO','TIPO_GLOSA_OBJECION','RESPONSABLE_RESERVA','MES','SOLICITUD_PAGO','NUMERO_FACTURA','FORMULARIO','FECHA_OCURRENCIA','HORA_OCURRENCIA','FECHA_MUERTE','NIT_RECLAMANTE','TIPO_DOCUMENTO_RECLAMANTE','TIPO_RECLAMACION_2','NOMBRE_RECLAMANTE','FECHA_ATENCION','AMPARO','VALOR_LIQUIDADO','VALOR_GLOSADO','SINIESTRO_SISE','CIUDAD_OCURRENCIA','DEPTO_OCURRENCIA','CIUDAD_RECLAMANTE','DEPTO_RECLAMANTE','CEDULA_ACCIDENTADO','NOMBRES_ACCIDENTADO','FECHA_AVISO','INICIO_VIGENCIA_POLIZA','FIN_VIGENCIA_POLIZA','TIPO_VEHICULO','PLACA','TIPO_DOCUMENTO_LESIONADO','FECHA_FACTURA','FEC_LIBERACION_RESERVA','CONCILIACION','PLACA_TRASLADO','GENERO','EDAD','DESCRIPCION_SINIESTRO','FEC_NAC_LESIONADO','LUGAR_OCURRENCIA','TIPO_RECLAMANTE','DIRECCION_RECLAMANTE','CONDICION_ACCIDENTADO','COD_CIUDAD_OCURR','COD_DEPTO_OCURR','COD_CIUDAD_RECLAMANTE','COD_DEPTO_RECLAMANTE','ANIO_EJERCICIO','COD_SUC','COD_CRUE','COD_IPS','LIQ_AUTOMATICA','PROC_JURIDICO']

col_name='DIRECCION_RECLAMANTE'

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