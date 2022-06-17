from pandas import DataFrame
from sqlalchemy import exc
from typing import List
import re

from src.data.connection import Connection
from src.infraestructure.log.logData import LogData
from src.infraestructure.error.errorCategory import ErrorCategory
from src.infraestructure.log.loggingDict import LoggingDict
from src.infraestructure.log.responseInsert import ResponseInsert


class LogRepository:

    @classmethod
    async def saveLog(cls, log: LogData):
        try:
            logError: str = re.sub('[^a-zA-Z0-9 \n\.]', '', log.message)
            await Connection().asyncExecute('SaveLog @message=' + "'"+str(logError)+"'")
        except exc.SQLAlchemyError:
            return ErrorCategory.Technical
        except Exception:
            return ErrorCategory.Technical
        
        
    @classmethod
    def insertLogIntoBd(cls, logDf: DataFrame) -> ResponseInsert:
        #Se crea un ciclo sube todas las filas del dataframe de errores a BD usando un procedimiento almacenado
        try:
            i : int = 0
            while i < len(logDf[LoggingDict.id_tarea.value]):
                
                id_tarea : int = logDf[LoggingDict.id_tarea.value].iloc[i]
                nom_tarea : str = logDf[LoggingDict.nom_tarea.value].iloc[i]
                nom_proceso : str = logDf[LoggingDict.nom_proceso.value].iloc[i]
                object_py : str = logDf[LoggingDict.object_py.value].iloc[i]
                object_bd : str = logDf[LoggingDict.object_bd.value].iloc[i]
                fail : str = logDf[LoggingDict.fail.value].iloc[i]
                description : str = logDf[LoggingDict.description.value].iloc[i]
                
                Connection.session.execute('[FRAUD].[saveCargaLog] :NUM_TAREA, :NOM_TAREA, :NOM_PROCESO, :OBJETO_PY, :OBJETO_BD, :FALLO, :DESCRIPCION', [{'NUM_TAREA': int(id_tarea), 'NOM_TAREA': nom_tarea, 'NOM_PROCESO': nom_proceso, 'OBJETO_PY':object_py, 'OBJETO_BD':object_bd, 'FALLO':fail, 'DESCRIPCION':description}])
                Connection.session.commit()
                
                i = i +1
                
            response:ResponseInsert = ResponseInsert(response=True)
                
        except exc.SQLAlchemyError as errorBD:
            response:ResponseInsert = str(errorBD)     
            
        except Exception as ex:
            
            Connection.session.rollback()
            response:ResponseInsert = str(ex)

        return response