from src.data.connection import Connection
from src.domain.response.msgResponse import MsgParametersResponse
from src.domain.request.msgRequest import MsgParametersRequest
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from src.domain.response.fileParametersResponse import ParameterResponse
from src.data.repository.parametersRepository import ParametersRepository
from sqlalchemy import exc

class MsgParametersRepository:
    
    #Este método obtiene todos los parametros definidos para el proceso MSG
    @classmethod
    def getMsgParameters(cls, process: str) -> MsgParametersResponse:
        try:
            validaterows: int = 0
            dct = {i.name: i.value for i in MsgParametersRequest}
            parameters = {}
            for key, value in dct.items():
                currentParameter:str = value #Se guarda el parámetro que se está consultando, para registrarlo en log si no está.
                response: ParameterResponse = ParametersRepository.getParameter(process=process, value = value)
                if isinstance(response, ParameterResponse):
                    parameters[key] = response.parameter
                    validaterows: int = 1
                else:
                    parametersResp : MsgParametersResponse = None
                    return parametersResp
            parametersResp: MsgParametersResponse = MsgParametersResponse(**parameters)

            if validaterows == 0:
                parametersResp: MsgParametersResponse = None
                
            LoggingHandler.emit(*LogCodification.parameters_success(process))
            
        except exc.SQLAlchemyError as errorBD:
            parametersResp: MsgParametersResponse = None
            LoggingHandler.emit(*LogCodification.bd_error(errorBD)) 

        except Exception as error:
            parametersResp: MsgParametersResponse = None
            Connection.session.rollback()
            LoggingHandler.emit(*LogCodification.parameters_missing(process=process, parameter=currentParameter))

        return parametersResp