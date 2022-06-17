from src.data.connection import Connection
from src.domain.request.globalParametersRequest import GlobalParametersRequest as gpRequest
from src.domain.response.globalParametersResponse import GlobalParametersResponse
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from sqlalchemy import exc

class ProcessesRepository:
    
    @classmethod
    def getFileList (cls) -> GlobalParametersResponse:
    
        try:
            validaterows:int = 0
            response = Connection.session.execute('[FRAUD].[getParameter] :proceso, :nom_parametro', {'proceso': gpRequest.globalProcess.value, 'nom_parametro': gpRequest.processes.value })
            for row in response:
                validaterows = 1
                processesResp: GlobalParametersResponse = GlobalParametersResponse(processes = row['VAL_PARAMETRO'])
                
            if validaterows == 0 :
                processesResp: GlobalParametersResponse = None
                LoggingHandler.emit(*LogCodification.processes_not_defined())
                return processesResp
            
            if processesResp.processes == '':
                LoggingHandler.emit(*LogCodification.process_is_empty())
                processesResp : GlobalParametersResponse = None
                return processesResp
            
            LoggingHandler.emit(*LogCodification.processes_success())
             
        except exc.SQLAlchemyError as errorBD:
            processesResp: GlobalParametersResponse = None
            LoggingHandler.emit(*LogCodification.bd_error(errorBD))
            
        except Exception as ex:
            processesResp: GlobalParametersResponse = None
            Connection.session.rollback()
            error = str(ex)
            LoggingHandler.emit(*LogCodification.process_other_exception(error = error))
        
        return processesResp