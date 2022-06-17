from src.data.connection import Connection
from src.domain.response.fileParametersResponse import ParameterResponse
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from sqlalchemy import exc

class ParametersRepository:
    
    @classmethod
    def getParameter(cls, process:str, value:str) -> ParameterResponse:
        try:
            validaterows:int = 0
            response = Connection.session.execute('[FRAUD].[getParameter] :proceso, :nom_parametro', {'proceso': process, 'nom_parametro': value})
            for row in response:
                validaterows = 1
                processesResp: ParameterResponse = ParameterResponse(parameter = row['VAL_PARAMETRO'])
                
            if validaterows == 0 :
                processesResp: ParameterResponse =  ParameterResponse(parameter = None)
                 
        except exc.SQLAlchemyError as errorBD:
            processesResp: ParameterResponse = None
            LoggingHandler.emit(*LogCodification.bd_error(errorBD))
            
        except Exception as ex:
            print(ex)
            processesResp: ParameterResponse = None
            Connection.session.rollback()
            LoggingHandler.emit(*LogCodification.parameters_other_exception(process=process, parameter=value, error = str(ex)))
        
        return processesResp    