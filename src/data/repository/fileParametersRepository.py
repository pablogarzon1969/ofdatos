from src.domain.request.fileParametersRequest import FileParametersRequest
from src.data.connection import Connection
from src.domain.response.fileParametersResponse import FileParametersResponse, ParameterResponse
from src.domain.request.fileParametersRequest import FileParametersRequest
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from src.data.repository.parametersRepository import ParametersRepository
from sqlalchemy import exc
from src.domain.response.globalParametersResponse import GlobalParametersResponse

class FileParametersRepository:

    @classmethod
    def getFileParameters(cls, process: str) -> FileParametersResponse:
        try:
            validaterows: int = 0
            dct = {i.name: i.value for i in FileParametersRequest}
            parameters = {}
            for key, value in dct.items():
                currentParameter:str = value #Se guarda el parámetro que se está consultando, para registrarlo en log si no está.
                if currentParameter in ['FS_USUARIOS_PATH', 'FS_OUTPUT_PATH']:
                    response: ParameterResponse = ParametersRepository.getParameter(process='GLOBAL', value = value)
                else:
                    response: ParameterResponse = ParametersRepository.getParameter(process=process, value = value)
                if isinstance(response, ParameterResponse):
                    parameters[key] = response.parameter
                    validaterows: int = 1
                else:
                    parametersResp : FileParametersResponse = None
                    return parametersResp
            parametersResp: FileParametersResponse = FileParametersResponse(**parameters)

            if validaterows == 0:
                parametersResp: FileParametersResponse = None
                
            LoggingHandler.emit(*LogCodification.parameters_success(process))

        except exc.SQLAlchemyError as errorBD:
            parametersResp: GlobalParametersResponse = None
            LoggingHandler.emit(*LogCodification.bd_error(errorBD))        
        
        except Exception as error:
            parametersResp: FileParametersResponse = None
            Connection.session.rollback()
            LoggingHandler.emit(*LogCodification.parameters_missing(process=process, parameter=currentParameter))

        return parametersResp