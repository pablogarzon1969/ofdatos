from src.data.connection import Connection
from src.domain.response.wsResponse import WsParametersResponse
from src.infraestructure.error.errorCategory import ErrorCategory
from src.domain.request.wsParametersRequest import wsParametersRequest
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from src.domain.response.fileParametersResponse import ParameterResponse
from src.data.repository.parametersRepository import ParametersRepository
from sqlalchemy import exc

class WsParametersRepository:
    
    #Este método obtiene todos los parametros definidos para el proceso WS
    @classmethod
    def getWsParameters(cls, process: str) -> WsParametersResponse:
        try:
            validaterows: int = 0
            dct = {i.name: i.value for i in wsParametersRequest}
            parameters = {}
            for key, value in dct.items():
                currentParameter:str = value #Se guarda el parámetro que se está consultando, para registrarlo en log si no está.
                response: ParameterResponse = ParametersRepository.getParameter(process=process, value = value)
                if isinstance(response, ParameterResponse):
                    parameters[key] = response.parameter
                    validaterows: int = 1
                else:
                    parametersResp : WsParametersResponse = None
                    return parametersResp
            parametersResp: WsParametersResponse = WsParametersResponse(**parameters)

            if validaterows == 0:
                parametersResp: WsParametersResponse = None
                
            LoggingHandler.emit(*LogCodification.parameters_success(process))
            
        except exc.SQLAlchemyError as errorBD:
            parametersResp: WsParametersResponse = None
            LoggingHandler.emit(*LogCodification.bd_error(errorBD)) 

        except Exception as error:
            parametersResp: WsParametersResponse = None
            Connection.session.rollback()
            LoggingHandler.emit(*LogCodification.parameters_missing(process=process, parameter=currentParameter))

        return parametersResp