#Libraries
import pandas as pd
import os
import numpy as np
from datetime import datetime

### FUTURO PRODUCCION
import pyodbc
conn=pyodbc.connect('Driver={SQL Server};'
                   'Server=DC1PPDSQL1'
                   'Database=SIT_MINERIA;'
                   'Trusted_Connection=yes;')

cursor = conn.cursor()

class Automatizacion():
    def execute_aut():
        
        cursor.execute("""SELECT TOP(1) VALOR FROM [SIT_MINERIA].[FRAUD].[TBL_MN_PFRAU_ACTCORTE]
                ORDER BY fecha_creacion desc""")
        valor_corte = cursor.fetchone()
        valor_corte = valor_corte[0]
    
        cursor.execute("""SELECT TOP(1) TIPO FROM [SIT_MINERIA].[FRAUD].[TBL_MN_PFRAU_ACTCORTE]
                ORDER BY fecha_creacion desc""")
        tipo_corte = cursor.fetchone()
        tipo_corte = tipo_corte[0]
        
        cursor.execute("""SELECT VAL_PARAMETRO FROM SIT_MINERIA.FRAUD.TBL_MN_PFRAU_PARAMETROS
                    WHERE NOM_PARAMETRO='FS_OUTPUT_PATH' AND PROCESO='GLOBAL'""")
        output_file_path = cursor.fetchone()
        output_file_path = output_file_path[0]
        
        Cambio_Estado = pd.read_sql_query("SELECT * FROM FRAUD.TBL_MN_PFRAU_CAMBIOESTADO",conn)
        Cambio_Estado['Observacion'] = Cambio_Estado['Observacion'].astype(str)
        Cambio_Estado = Cambio_Estado.rename(columns={'NUMERO_RECLAMACION':'NUMERO_RECLAMACION2'})
        Cambio_Estado = Cambio_Estado.drop(["NUMERO_SINIESTRO"], axis=1)
        Cambio_Estado['NUMERO_RECLAMACION2'] = Cambio_Estado['NUMERO_RECLAMACION2'].astype(str)
        
        LLAMADAS_AUDITORIA = pd.read_sql_query("SELECT * FROM FRAUD.TBL_MN_PFRAU_LLAMADASAUDITORIA",conn)
        LLAMADAS_AUDITORIA['RECLAMACION'] = LLAMADAS_AUDITORIA['RECLAMACION'].astype(str)

        Censo = pd.read_sql_query("SELECT * FROM FRAUD.TBL_MN_PFRAU_CENSO",conn)
        DIAS = pd.read_sql_query("SELECT * FROM FRAUD.TBL_MN_PFRAU_DIAS",conn)
        IPS_AR = pd.read_sql_query("SELECT * FROM FRAUD.TBL_MN_PFRAU_IPSALTORIESGO",conn)
        PLACAS = pd.read_sql_query("SELECT * FROM FRAUD.TBL_MN_PFRAU_PLACAS",conn)
        IPS_ALERTA = pd.read_sql_query("SELECT * FROM FRAUD.TBL_MN_PFRAU_IPSALERTA",conn)
        Ciudades = pd.read_sql_query("SELECT * FROM FRAUD.TBL_MN_PFRAU_CIUDADES",conn)    
        
        Base = pd.read_sql_query("""
        SELECT  
                                         TD1.NUMERO_SINIESTRO
                                        ,TD1.NUMERO_RECLAMACION
                                        ,TD1.NUMERO_POLIZA
                                        ,TD1.NUMERO_FACTURA
                                        ,TD3.FECHA_OCURRENCIA
                                        ,TD3.FECHA_RECP_ASEGURADORA
                                        ,CAST(TD3.CEDULA_ACCIDENTADO AS VARCHAR) AS CEDULA_ACCIDENTADO
                                        ,TD3.HORA_OCURRENCIA
                                        ,TD1.SCORE_PREDICCION
                                        ,TD1.EXISTE_RAF
                                        ,TD1.IPS_ESQUEMA
                                        ,TD1.IND_FRAUDE
                                        ,ISNULL(TD1.FUENTE_FRAUDE,'') AS FUENTE_FRAUDE
                                        ,ISNULL(dbo.FN_MN_PFRAU_ALERTAS(TD1.ALERTAS,'-', 'LINEA'),'') AS ALERTAS
                                        ,ISNULL(dbo.FN_MN_PFRAU_ALERTAS(TD1.INTERPRETABILIDAD_SCORE,'-', 'INTERPRETABILIDAD'),'') AS INTERPRETABILIDAD_SCORE
                                        ,TD1.FECHA_ESTADO_ACTUAL
                                        ,TD1.FECHA_PROCESO
                                        ,CAST(TD3.NIT_RECLAMANTE AS VARCHAR) AS NIT_RECLAMANTE
                                        ,TD3.VALOR_COBRADO
                                        ,TD3.TIPO_RECLAMACION
                                        ,ISNULL(TD2.FECHA_PROCESO,'') AS FECHA_PROCESO_ANT 
                                        ,ISNULL(TD2.SCORE_PREDICCION,0)AS SCORE_PREDICCION_ANT
                                        ,CASE WHEN TD1.CASO_SOSPECHOSO = '' THEN 'NO CUMPLE REGLAS' ELSE 'CUMPLE REGLAS PARA ASIGNAR A PREVENCION FRAUDE' END AS OBSERVACION 
                                        ,(CASE WHEN TD2.NUMERO_RECLAMACION IS NOT NULL AND 
                                            CAST(TD1.SCORE_PREDICCION AS DECIMAL(10,8))<> CAST(TD2.SCORE_PREDICCION AS DECIMAL(10,8)) THEN 'DUPLICADO CAMBIO SCORE' 
                                            WHEN TD2.NUMERO_RECLAMACION IS NOT NULL AND 
                                            CAST(TD1.SCORE_PREDICCION AS DECIMAL(10,8)) = CAST(TD2.SCORE_PREDICCION AS DECIMAL(10,8)) THEN 'DUPLICADO'
                                                WHEN TD2.NUMERO_RECLAMACION IS NULL THEN 'NUEVO'  END) AS VALIDACION_DUPLICADOS
                                    FROM STAGE.STG_MN_PFRAU_PREDICCIONES_VI TD1
                                    LEFT JOIN (SELECT TD1.NUMERO_POLIZA,TD1.NUMERO_RECLAMACION, TD1.NUMERO_SINIESTRO, TD1.SCORE_PREDICCION, MIN(TD1.FECHA_PROCESO) AS FECHA_PROCESO 
                                            FROM FRAUD.TBL_MN_PFRAU_PREDICCIONES_HIS TD1
                                            INNER JOIN (SELECT NUMERO_POLIZA,NUMERO_RECLAMACION, NUMERO_SINIESTRO, MAX(SCORE_PREDICCION) SCORE_PREDICCION 
                                            FROM FRAUD.TBL_MN_PFRAU_PREDICCIONES_HIS 
                                            WHERE FECHA_PROCESO <>  (SELECT MAX(REPLACE(FECHA_PROCESO,'-','')) FECHA_PROCESO 
                                                                     FROM STAGE.STG_MN_PFRAU_PREDICCIONES_VI) 
                                                                     GROUP BY NUMERO_POLIZA,NUMERO_RECLAMACION, NUMERO_SINIESTRO) TD2
                                        ON TD1.NUMERO_RECLAMACION=TD2.NUMERO_RECLAMACION AND TD1.NUMERO_SINIESTRO=TD2.NUMERO_SINIESTRO AND TD1.NUMERO_POLIZA=TD2.NUMERO_POLIZA AND TD1.SCORE_PREDICCION=TD2.SCORE_PREDICCION
                                    GROUP BY TD1.NUMERO_POLIZA,TD1.NUMERO_RECLAMACION, TD1.NUMERO_SINIESTRO, TD1.SCORE_PREDICCION) TD2
                                        ON TD1.NUMERO_RECLAMACION=TD2.NUMERO_RECLAMACION AND TD1.NUMERO_SINIESTRO=TD2.NUMERO_SINIESTRO AND TD1.NUMERO_POLIZA=TD2.NUMERO_POLIZA
                                    LEFT JOIN (SELECT DISTINCT NUMERO_POLIZA,NUMERO_SINIESTRO,NUMERO_RECLAMACION,NUMERO_FACTURA,FECHA_OCURRENCIA,FECHA_RECP_ASEGURADORA,CEDULA_ACCIDENTADO,HORA_OCURRENCIA, NIT_RECLAMANTE, VALOR_COBRADO,TIPO_RECLAMACION  FROM FRAUD.TBL_MN_PFRAU_RECLAMACION WHERE NUMERO_FACTURA <> '' ) TD3
                                        ON TD1.NUMERO_RECLAMACION=TD3.NUMERO_RECLAMACION AND TD1.NUMERO_SINIESTRO=TD3.NUMERO_SINIESTRO AND TD1.NUMERO_POLIZA=TD3.NUMERO_POLIZA AND TD1.NUMERO_FACTURA = TD3.NUMERO_FACTURA""",conn)

        comparativo = pd.read_sql_query("""SELECT CAST(NUMERO_SINIESTRO AS VARCHAR) AS NUMERO_SINIESTRO, CAST(NUMERO_RECLAMACION AS varchar) AS NUMERO_RECLAMACION, CAST(NUMERO_POLIZA AS VARCHAR) AS NUMERO_POLIZA, PLACA, CIUDAD_RECLAMANTE,NOMBRE_RECLAMANTE,ESTADO_ACTUAL FROM FRAUD.TBL_MN_PFRAU_RECLAMACION
                                WHERE FORMAT(FEC_MODIFICACION, 'MM-dd-yy')=FORMAT(getdate(), 'MM-dd-yy') OR FORMAT(FEC_CREACION, 'MM-dd-yy')=FORMAT(getdate(), 'MM-dd-yy')""",conn)
        
        Base[['NUMERO_POLIZA','NUMERO_SINIESTRO','NUMERO_RECLAMACION']]=Base[['NUMERO_POLIZA','NUMERO_SINIESTRO','NUMERO_RECLAMACION']].astype(str)
        comparativo[['NUMERO_SINIESTRO','NUMERO_POLIZA']] = comparativo[['NUMERO_SINIESTRO','NUMERO_POLIZA']].astype(str)
        Base = Base.merge(comparativo[["NUMERO_SINIESTRO","NUMERO_RECLAMACION", "NUMERO_POLIZA", "PLACA"]].astype(str),how='left', left_on=['NUMERO_SINIESTRO', 'NUMERO_RECLAMACION','NUMERO_POLIZA'], right_on=["NUMERO_SINIESTRO","NUMERO_RECLAMACION", "NUMERO_POLIZA"])
        
        ##Se genera la columna base de fecha en numero
        Base['Fecha_Ocurrencia_Formato'] = ((pd.to_datetime(Base['FECHA_OCURRENCIA'], format='%Y/%m/%d'))- datetime(1899,12,30)).dt.days
        
        ##SE AÑADEN LAS COLUMNAS LLAVES
        Base['Poliza+Fecha accidente+Cedula'] = Base['NUMERO_POLIZA']+Base['Fecha_Ocurrencia_Formato'].astype(str)+Base['CEDULA_ACCIDENTADO'].astype(str)
        Base['Poliza+Stro']= Base['NUMERO_POLIZA']+ Base['NUMERO_SINIESTRO']
        
        ##CRUCES DE INFORMACIÓN
        Base = Base.merge(Censo[['Poliza+Fecha accidente+Cedula', 'RESULTADO']].drop_duplicates(), on = 'Poliza+Fecha accidente+Cedula', how = 'left')
        Base = Base.rename(columns = {'RESULTADO':'Censo'})
        
        Base = Base.merge(Cambio_Estado[['Observacion', 'Cambio de estad']].drop_duplicates(), how = 'left', left_on = 'Poliza+Stro', right_on = 'Observacion')
        Base = Base.drop(["Observacion"], axis=1)
        Base = Base.rename(columns = {'Cambio de estad':'Cambio de estado'})
        
        Base = Base.merge(Cambio_Estado[['NUMERO_RECLAMACION2']].drop_duplicates(), how = 'left', left_on = 'NUMERO_RECLAMACION', right_on = 'NUMERO_RECLAMACION2')
        Base = Base.rename(columns = {'NUMERO_RECLAMACION2':'Reclamo cambio de estado'})
        
        ##Variables calculadas
        Base['Estado'] = np.where(Base['Censo'].notnull(), 'No cambia de estado','')
        Base['Estado'] = np.where(Base['Cambio de estado'].notnull(), 'No cambia de estado',Base['Estado'])
        Base['Estado'] = np.where(Base['Reclamo cambio de estado'].notnull(), 'No cambia de estado',Base['Estado'])
        Base['Estado'] = np.where((Base['EXISTE_RAF'] == 'SI') & (Base['Estado'] ==''), 'No cambia de estado', Base['Estado'])
        Base['Estado'] = np.where((Base['IND_FRAUDE'] == 'SI') & (Base['Estado'] ==''), 'No cambia de estado', Base['Estado'])
        
        #Base['Fecha'] = datetime(2022,1,26).date()
        Base['Fecha'] = datetime.now().date()
        Base['Dias'] = (Base['Fecha']-(pd.to_datetime(Base['FECHA_RECP_ASEGURADORA'], format='%Y/%m/%d')).dt.date).dt.days
        Base['Estado'] = np.where(Base['Dias'] >= 16, 'No cambia de estado', Base['Estado'])
        
        ##Se toman solamente los datos de aquellos en el que estado es vacio
        Base['Prediccion_0'] = np.where((Base['OBSERVACION'] == 'CUMPLE REGLAS PARA ASIGNAR A PREVENCION FRAUDE') & (Base['Estado'] == ""), 1, np.nan)
        
        Comp = Base[Base['Prediccion_0'] == 1]
        
        #################################
        if tipo_corte =='PORCENTAJE':
            Comp['Prediccion_0']=np.where(Comp['SCORE_PREDICCION'].astype(float)>=float(valor_corte.replace(',','.')), Comp['Prediccion_0'],0)
        else: 
            Comp['Prediccion_0'].iloc[int(valor_corte):] = 0  
        ##################
        
        Comp = Comp.rename(columns = {'Prediccion_0':'Corte'})        
        Base = Base.merge(Comp[['NUMERO_SINIESTRO', 'NUMERO_RECLAMACION','NUMERO_POLIZA','Corte']].drop_duplicates(), how = 'left', on = ['NUMERO_SINIESTRO', 'NUMERO_RECLAMACION','NUMERO_POLIZA'])
        Base['Prediccion_0'] = np.where(Base['Prediccion_0'] == Base['Corte'], Base['Prediccion_0'], Base['Corte'])
        Base = Base.drop(["Corte"], axis=1)
            
        ##aquellas que sean Prediccion_0='', Estado='', & Observación=Cumple reglas para asignar a prevención fraude se llenan las siguientes variables para revisión por reglas
        Base = Base.merge(LLAMADAS_AUDITORIA, how = 'left', left_on = 'NUMERO_RECLAMACION', right_on = 'RECLAMACION')
        Base['Auditoria telefonica Reclamo'] = np.where(Base['RECLAMACION'].notnull(), Base['RECLAMACION'], np.nan)
        Base = Base.drop(["RECLAMACION", "SINIESTRO", "POLIZA"], axis = 1)
        Base['Auditoria telefonica Reclamo'] = np.where((Base['Prediccion_0'] == 0), Base['Auditoria telefonica Reclamo'], np.nan)
        
        Base = Base.merge(IPS_ALERTA[['NIT','ALERTA']].drop_duplicates(), how = 'left', left_on = 'NIT_RECLAMANTE', right_on = 'NIT')
        Base = Base.drop(["NIT"], axis = 1)
        Base = Base.rename(columns = {'ALERTA':'Nuevas alertas ips NIT'})
        Base = Base.drop_duplicates(['NUMERO_SINIESTRO','NUMERO_RECLAMACION','NUMERO_POLIZA'],keep = 'last')
        Base['Nuevas alertas ips NIT'] = np.where((Base['Prediccion_0'] == 0), Base['Nuevas alertas ips NIT'], np.nan)
        
        Base = Base.merge(DIAS[['CEDULA']].drop_duplicates(), how = 'left', left_on = 'CEDULA_ACCIDENTADO', right_on = 'CEDULA')
        Base = Base.rename(columns = {'CEDULA':'Dias Cedula'})
        Base['Dias Cedula'] = np.where((Base['Prediccion_0'] == 0), Base['Dias Cedula'], np.nan)
        
        Base = Base.merge(PLACAS[['PLACA']].drop_duplicates(), how = 'left', left_on = 'PLACA', right_on = 'PLACA')
        Base['Dias placa']=Base['PLACA']
        Base['Dias placa'] = np.where((Base['Prediccion_0'] == 0), Base['Dias placa'], np.nan)
        
        Base = Base.merge(comparativo[["NUMERO_RECLAMACION", "CIUDAD_RECLAMANTE"]].astype(str),how = 'left', left_on = ['NUMERO_RECLAMACION'], right_on = ["NUMERO_RECLAMACION"])
        Base = Base.rename(columns = {'CIUDAD_RECLAMANTE':'Alerta ciudad'})
        
        Base = Base.merge(comparativo[["NUMERO_RECLAMACION", "NOMBRE_RECLAMANTE"]].astype(str),how = 'left', left_on = ['NUMERO_RECLAMACION'], right_on = ["NUMERO_RECLAMACION"])
        Base = Base.rename(columns = {'NOMBRE_RECLAMANTE':'Alerta Fabisalud'})
        Base['Alerta Fabisalud'] = np.where((Base['Prediccion_0'] == 0), Base['Alerta Fabisalud'], np.nan)
        
        Base = Base.merge(IPS_AR[['Etiquetas de fila','Enviar']],how = 'left', left_on = ['NIT_RECLAMANTE'], right_on = ["Etiquetas de fila"])
        Base = Base.drop(["Etiquetas de fila"], axis = 1)
        Base = Base.rename(columns={'Enviar':'Valor'})
        Base['Valor'] = np.where((Base['Prediccion_0'] == 0), Base['Valor'], np.nan)
        
        Base['Casos Esp'] = np.where((Base['Prediccion_0'] == 0) & (Base['Nuevas alertas ips NIT']).notnull() ,Base['Nuevas alertas ips NIT'],np.nan)
        Base['Casos Esp'] = np.where((Base['Casos Esp'].isnull()) & (Base['Prediccion_0'] == 0) & (Base['Valor'].isin(['Enviar','No tiene casos'])),'IPS presenta fraude mayor a 30 millones',Base['Casos Esp'])
        Base['Casos Esp'] = np.where((Base['Casos Esp'].isnull()) & (Base['Prediccion_0'] == 0) & (Base['Alerta ciudad'].isin(list(Ciudades['Ciudades'].str.upper()))), 'Ciudad con alto indice de fraude',Base['Casos Esp'])
        
        Base['Prediccion_0'] = np.where((Base['Prediccion_0'] == 0) & (Base['Casos Esp'].notnull()), 2, Base['Prediccion_0'])
        Base['Prediccion_0'] = np.where(np.isnan(Base['Prediccion_0']),'',Base['Prediccion_0'].astype('Int64').astype(str))

                ###Se eliminan historial de más de dos semanas/meses
        cursor.execute("""TRUNCATE TABLE [FRAUD].[TBL_MN_PFRAU_RESULTADOS]""")
        cursor.commit()
        
        
        ###Envio de información a tabla para glosas
        for index, row in Base.iterrows():           
                cursor.execute("INSERT INTO [FRAUD].[TBL_MN_PFRAU_RESULTADOS] ([NUMERO_SINIESTRO],[NUMERO_RECLAMACION],[NUMERO_POLIZA],[NUMERO_FACTURA],[INVESTIGACION],[FEC_CREACION])" + \
                           " values (?, ?, ?, ?, ?, ?)",row['NUMERO_SINIESTRO'],row['NUMERO_RECLAMACION'],row['NUMERO_POLIZA'], row['NUMERO_FACTURA'], row['Prediccion_0'],datetime.now())
                cursor.commit()
        
        
        ###revision valores
        Dif0 = Base[Base['Prediccion_0'] == '0']
        Dif1 = Base[Base['Prediccion_0'] == '1']
        Dif2 = Base[Base['Prediccion_0'] == '2']    
        
        File_CambioEstado = Base[Base['Prediccion_0'].isin(['1','2'])]
        File_CambioEstado['Poliza+Stro'] = np.where(File_CambioEstado['Prediccion_0'] == '1', 'Modelo predicciones', File_CambioEstado['Casos Esp'])
        File_CambioEstado['Poliza+Fecha accidente+Cedula'] = np.where(File_CambioEstado['IPS_ESQUEMA'] == 'SI', 'Pendiente Verificación', 'Pendiente aseguradora - investigación')

        File_CambioEstado.to_csv('//dc1pcadfrs1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Output/Consolidado'+str(datetime.now().date())+'.csv', index=False)
#        File_CambioEstado.to_csv('//dc2tvaftp1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Output/Consolidado'+str(datetime.now().date())+'.csv', index=False)
        
        ConsModFinal=File_CambioEstado[['NUMERO_SINIESTRO','NUMERO_RECLAMACION','SCORE_PREDICCION','FECHA_PROCESO','FECHA_ESTADO_ACTUAL']]
        ConsModFinal['Modelo Dia proceso'], ConsModFinal['Modelo estado actual'], ConsModFinal['Negativos'] = ['', '', '']

        if os.path.exists('//dc1pcadfrs1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Output/ConsolidadoModeloFinal.xlsx'): 
#        if os.path.exists('//dc2tvaftp1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Output/ConsolidadoModeloFinal.xlsx'): 

            df_excel = pd.read_excel(output_file_path+'ConsolidadoModeloFinal.xlsx')
            result = pd.concat([df_excel, ConsModFinal], ignore_index=True)
            result.to_excel(output_file_path+'ConsolidadoModeloFinal.xlsx', index=False)
        else:
            ConsModFinal.to_excel('//dc1pcadfrs1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Output/ConsolidadoModeloFinal.xlsx', index = False)
#            ConsModFinal.to_excel('//dc2tvaftp1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Output/ConsolidadoModeloFinal.xlsx', index = False)
        
        
        Final = File_CambioEstado[['NUMERO_RECLAMACION','Poliza+Fecha accidente+Cedula','Poliza+Stro','NUMERO_SINIESTRO']]
        Final = Final.merge(comparativo[['NUMERO_RECLAMACION','ESTADO_ACTUAL']], how = "left", left_on = 'NUMERO_RECLAMACION', right_on = 'NUMERO_RECLAMACION')
        
        Final_ETL= Final[['Poliza+Stro','Poliza+Fecha accidente+Cedula','NUMERO_SINIESTRO','NUMERO_RECLAMACION']]
        Final_ETL = Final_ETL.rename(columns = {'Poliza+Fecha accidente+Cedula': 'Cambio de estad',
                                        'Poliza+Stro':'Observacion'})
    
        #ARCHIVO PARA ETL
        Final_ETL.to_excel('//dc1pcadfrs1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Input/Cambio de estado.xlsx',index=False)
#        Final_ETL.to_excel('//dc2tvaftp1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Input/Cambio de estado.xlsx',index=False)



        Final = Final[['NUMERO_RECLAMACION', 'ESTADO_ACTUAL','Poliza+Fecha accidente+Cedula', 'Poliza+Stro']]
        Final = Final.rename(columns = {'NUMERO_RECLAMACION':'Reclamacion', 
                                        'Poliza+Fecha accidente+Cedula': 'Estado siguiente',
                                        'Poliza+Stro':'Observaciones',
                                        'ESTADO_ACTUAL':'Estado actual'})
        
        Final.to_csv('//dc1pcadfrs1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Output/Cambio de estado'+str(datetime.now().date())+'.csv', index=False)
#        Final.to_csv('//dc2tvaftp1/IntercambioTerceros/AUTOS/SOAT_FRAUDE/Output/Cambio de estado'+str(datetime.now().date())+'.csv', index=False)
        
        cursor.close()
