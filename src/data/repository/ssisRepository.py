from src.data.connection import Connection
from src.domain.response.fileParametersResponse import ParameterResponse
from src.domain.response.ssisParametersResponse import SsisParametersResponse
from src.domain.request.ssisParametersRequest import SsisParametersRequest
from src.domain.response.ssisResponse import SsisResponse
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from src.data.repository.parametersRepository import ParametersRepository
from sqlalchemy import exc


class SSISRepository:
    
    @classmethod
    def getSSISParameters(cls, process: str) -> SsisParametersResponse:
        try:
            validaterows: int = 0
            dct = {i.name: i.value for i in SsisParametersRequest}
            parameters = {}
            for key, value in dct.items():
                currentParameter:str = value #Se guarda el parámetro que se está consultando, para registrarlo en log si no está.
                validaterows = 1
                response: ParameterResponse = ParametersRepository.getParameter(process=process, value = value)
                if isinstance(response, ParameterResponse):
                    parameters[key] = response.parameter
                else:
                    parametersResp : SsisParametersResponse = None
                    return parametersResp
            parametersResp: SsisParametersResponse = SsisParametersResponse(**parameters)

            if validaterows == 0:
                parametersResp: SsisParametersResponse = None
                
            LoggingHandler.emit(*LogCodification.parameters_success(process))

        except Exception as error:
            parametersResp: SsisParametersResponse = None
            Connection.session.rollback()
            LoggingHandler.emit(*LogCodification.parameters_missing(process=process, parameter=currentParameter))

        return parametersResp
    
    @classmethod
    def executeEtl(cls, ssisParam:SsisParametersResponse) -> SsisResponse:
        try:
            print('Inicio Ejecución ETL: ',ssisParam.jobname)
            validaterows:int = 0
            response = Connection.session.execute('[dbo].[SP_EXECUTE_JOB_SSIS] :JobName, :TimeLimit, :Debug, :Status', {'JobName': ssisParam.jobname, 'TimeLimit': ssisParam.timelimit, 'Debug':ssisParam.debug, 'Status':ssisParam.status})
            for row in response:
                validaterows = 1
                etlResponse: SsisResponse = SsisResponse(result = row['RESULT'])
                
            if validaterows == 0 :
                etlResponse: SsisResponse =  SsisResponse(result = None)
                 
        except exc.SQLAlchemyError as errorBD:
            etlResponse: SsisResponse = None
            LoggingHandler.emit(*LogCodification.bd_error(errorBD))
            
        except Exception as ex:
            etlResponse: SsisResponse = None
            Connection.session.rollback()
            LoggingHandler.emit(*LogCodification.parameters_other_exception(process='ETL', parameter='ETL', error = str(ex)))
        
        return etlResponse    