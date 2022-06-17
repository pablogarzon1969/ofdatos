from tabulate import tabulate
from src.infraestructure.log.loggingDict import LoggingDict
from src.infraestructure.log.logCodification import  LogCodification
from src.infraestructure.log.responseInsert import ResponseInsert
from src.data.repository.logRepository import LogRepository
from typing import List
from pathlib import Path
import logging
import pandas as pd
import time
import json

class LoggingHandler(logging.Handler): # Inherit from logging.Handler
            
    log_df = pd.DataFrame()     
    def __init__(cls):
        logging.Handler.__init__(cls)
                    
    @classmethod
    def emit(cls, id_tarea:int, nom_tarea:str, nom_proceso:str, object_py:str, object_bd:str, fail:str, description:str):
        record = pd.DataFrame({
            LoggingDict.id_tarea.value:[id_tarea],
            LoggingDict.nom_tarea.value:[nom_tarea],
            LoggingDict.nom_proceso.value:[nom_proceso],
            LoggingDict.object_py.value:[object_py],
            LoggingDict.object_bd.value:[object_bd],
            LoggingDict.fail.value:[fail],
            LoggingDict.description.value:[description]
        }) 
        cls.log_df = cls.log_df.append(record)
        
    @classmethod
    def insertLogIntoBd(cls) -> bool:
        response:ResponseInsert = LogRepository.insertLogIntoBd(cls.log_df)
        if isinstance(response, ResponseInsert):
            return response.response
        else:
            cls.emit(*LogCodification.database_log_failure(ex = str(response)))
            return False
            
            
        
    
    @classmethod
    def logIntoHtml(cls):
        return cls.log_df.to_html()
    
    @classmethod
    def logCheckErrors(cls): #devuelve 1 si hay errores y 0 si no
        if 'SI' in cls.log_df[LoggingDict.fail.value].unique():
            a = 1
        else:
            a = 0
        return a
    
    @classmethod
    def logReadDescription(cls, description:str): #devuelve 1 si la descripcion está en el log y 0 si no
        if description in cls.log_df[LoggingDict.description.value].unique():
            a = True
        else:
            a = False
        return a
    
    @classmethod
    def logIntoTxt(cls):
        try:   
            base_path = Path(__file__).parents[1]
            file_path = (base_path / "../config.json").resolve()
            
            with open(file_path, 'r') as f:
                config = json.load(f)
                
            if config['DebugConfiguration']['DEBUG'] == 0: #si debug = 0 se hace debug
            
                cols:List = ['ID_Tarea', 'Nombre Tarea', 'Nombre Proceso', 'Objeto PY', 'Objeto BD', 'Fallo', 'Descripción']
                timestr:time = time.strftime("%Y%m%d-%H%M%S")
                projectName:str = config['DebugConfiguration']['PROJECT_NAME']
                filename:str = projectName + str(timestr) +'.txt'
                path:str = config['DebugConfiguration']['LOG_FILE_PATH']
                fullpath:str = path + filename
                
                with open(fullpath, 'w') as f:
                    f.write(tabulate(cls.log_df, headers=cols))
                    
                print('Debug creado ' + fullpath)
            else:
                print('Debug desactivado')
        except Exception as ex:
            print(ex)
