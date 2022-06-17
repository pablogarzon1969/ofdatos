import imp
from pandas.core.frame import DataFrame
from sqlalchemy import false
from src.domain.response.fileParametersResponse import FileParametersResponse
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
import pandas as pd
from datetime import datetime
from src.dataStorage.validationFile import ValidationFile
from src.agentservices.mail.mailParametersDB import MailParametersDb
from src.agentservices.mail.mailManagement import MailManagement
from src.domain.response.mailSendResponse import MailSendResponse
import xdrlib
import csv

class File:

    @classmethod
    #Importación del archivo
    def getFile(cls, parameters : FileParametersResponse, process : str) -> DataFrame:
        try:
            objectPy = ValidationFile.validationFileName(filePath=parameters.inputPath, formatFile=parameters.inputFileType, fileName=parameters.inputFileName,fileRequired=parameters.fileRequired, process=process)
            if isinstance(objectPy,str):            
                fileFullPath = parameters.inputPath+objectPy
                columnNames = parameters.fileColumnNames.split(',')
                fileSheet = parameters.fileSheet
                if parameters.inputFileType == '.xlsx':
                    if objectPy=='DIAS.xlsx' or objectPy=='PLACAS.xlsx':
                        df = pd.read_excel(fileFullPath, names=columnNames, skiprows=2)    
                    else:    
                        df = pd.read_excel(fileFullPath, names=columnNames)
                elif parameters.inputFileType == '.xls': 
                    df = pd.read_excel(fileFullPath, names=columnNames, engine='xlrd')   
                elif parameters.inputFileType == '.csv':
                    if objectPy=='CapacidadInstalada.csv':
                        df = pd.read_csv(fileFullPath,sep = ';',encoding = 'Latin-1',engine = 'python', index_col = False,keep_default_na = False, quoting = csv.QUOTE_NONE,names=columnNames)
##cambio
                    if 'Comparativo Reserva pendiente' in objectPy:
                        df = pd.read_csv(fileFullPath,sep = ';',encoding = 'Latin-1',engine = 'python',
                        index_col = False,keep_default_na = False,
                        usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,
                          24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,
                          45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62])
                        df.columns=['RECLAMACION','TIPO_RECLAMACION','FECHA_RECP_ASEGURADORA','FECHA_RECP_CORIS','ESTADO_ACTUAL','FECHA_ESTADO_ACTUAL','RESPONSABLE_ESTADO','ESTADO_RESERVA','ESTADO_PAGO','VALOR_RESERVADO','VALOR_COBRADO','TIPO_GLOSA_OBJECION','RESPONSABLE_RESERVA','MES','SOLICITUD_PAGO','NUMERO_FACTURA','FORMULARIO','FECHA_OCURRENCIA','HORA_OCURRENCIA','FECHA_MUERTE','NIT_RECLAMANTE','TIPO_DOCUMENTO_RECLAMANTE','TIPO_RECLAMACION_2','NOMBRE_RECLAMANTE','FECHA_ATENCION','AMPARO','VALOR_LIQUIDADO','VALOR_GLOSADO','SINIESTRO_SISE','CIUDAD_OCURRENCIA','DEPTO_OCURRENCIA','CIUDAD_RECLAMANTE','DEPTO_RECLAMANTE','CEDULA_ACCIDENTADO','NOMBRES_ACCIDENTADO','FECHA_AVISO','INICIO_VIGENCIA_POLIZA','FIN_VIGENCIA_POLIZA','TIPO_VEHICULO','PLACA','TIPO_DOCUMENTO_LESIONADO','FECHA_FACTURA','FEC_LIBERACION_RESERVA','CONCILIACION','PLACA_TRASLADO','GENERO','EDAD','DESCRIPCION_SINIESTRO','FEC_NAC_LESIONADO','LUGAR_OCURRENCIA','TIPO_RECLAMANTE','DIRECCION_RECLAMANTE','CONDICION_ACCIDENTADO','COD_CIUDAD_OCURR','COD_DEPTO_OCURR','COD_CIUDAD_RECLAMANTE','COD_DEPTO_RECLAMANTE','ANIO_EJERCICIO','COD_SUC','COD_CRUE','COD_IPS','LIQ_AUTOMATICA','PROC_JURIDICO']
#fin cambio
                    else:
                        df = pd.read_csv(fileFullPath, delimiter=';', encoding = "ISO-8859-1", engine='python',names=columnNames, skiprows=1) # Parametrizar el delimiter ?
                else:
                    LoggingHandler.emit(*LogCodification.import_invalid_file_type(process=process, objectPy=objectPy))
                    raise # Todavia no que se hacer en este caso
                
                LoggingHandler.emit(*LogCodification.import_sucess(process=process, objectPy=objectPy))
            
            else:
                df : DataFrame = None
    
        except Exception as ex:
            LoggingHandler.emit(*LogCodification.import_other_exception(process=process, objectPy=objectPy, ex = ex))
            df : DataFrame = None
            
        return df
    
    @classmethod
    #Exportación del archivo
    def writeFile(cls, file : DataFrame, process:str, parameters : FileParametersResponse):
        objectPy = parameters.outputFileName + parameters.outputFileType
        try:
            if parameters.outputFileName.__contains__('%'):
                exportDate : str = datetime.today().strftime('%Y%m%d')
                fileExportPath = parameters.outputPath+'\\'+parameters.outputFileName+exportDate+parameters.outputFileType
            else:
                fileExportPath = parameters.outputPath+'\\'+parameters.outputFileName+parameters.outputFileType
            if parameters.outputFileType == '.xlsx':
                writer = pd.ExcelWriter(fileExportPath, engine='openpyxl')
                file.to_excel(writer, index = False)
                writer.save()
                writer.close()
            elif parameters.outputFileType == '.csv':
                file.to_csv(fileExportPath, encoding='utf-8', sep=';', index=False) #Parametrizar separador?
            else:
                LoggingHandler.emit(*LogCodification.export_invalid_file_type(process=process, objectPy=objectPy))
                raise # Todavia no que se hacer en este caso
            
            LoggingHandler.emit(*LogCodification.export_success(process=process, objectPy=objectPy))
            
        except Exception as ex:
            ex = str(ex)
            LoggingHandler.emit(*LogCodification.import_other_exception(process=process, objectPy=objectPy, ex = ex))