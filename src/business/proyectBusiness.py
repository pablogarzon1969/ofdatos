from pandas.core.frame import DataFrame
from src.domain.response.mailSendResponse import MailSendResponse
from src.domain.response.ssisParametersResponse import SsisParametersResponse
from src.domain.response.fileParametersResponse import FileParametersResponse
from src.clean.cleanMain import DataCleaning
from src.data.repository.ssisRepository import SSISRepository
from src.dataStorage.fileManagement import FileManagement
from src.agentservices.mail.mailParametersDB import MailParametersDb
from src.agentservices.mail.mailManagement import MailManagement
from src.agentservices.mail.mailParametersjson import MailParametersJson
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from src.data.repository.processesRepository import ProcessesRepository
from src.domain.response.globalParametersResponse import GlobalParametersResponse
from src.data.repository.fileParametersRepository import FileParametersRepository
from src.dataStorage.moveFile import MoveFile
from src.train.Score import Model
from src.train.Automatizacion import Automatizacion
from src.dataStorage.cleanFolder import CleanFolder

class ProyectBusiness:

    @classmethod
    def  execute_proyect(cls):
        try:
            filelist = ProcessesRepository.getFileList()
            if isinstance(filelist, GlobalParametersResponse):
                filelist = filelist.processes.split(', ')
                for process in filelist:
                    parameters = FileParametersRepository.getFileParameters(process = process)
                    if isinstance(parameters, FileParametersResponse):
                        file = FileManagement.importFile(process=process, parameters=parameters)
                        if isinstance(file, DataFrame):
                            DataCleaning.cleanData(df = file, process = process, parameters = parameters)
                            FileManagement.exportFile(file = file, process=process, parameters = parameters)
                            MoveFile.moveProcess(parameters=parameters, process=process)
                            
                SsisParameters = SSISRepository.getSSISParameters(process='ETL')
                if isinstance(SsisParameters, SsisParametersResponse):
                    resultEtl = SSISRepository.executeEtl(SsisParameters)
                    print(resultEtl)
                    if resultEtl.result == '1':
                        LoggingHandler.emit(*LogCodification.ssis_ejecution_sucess())
                    else:
                        LoggingHandler.emit(*LogCodification.ssis_ejecution_not_success(resultEtl = str(resultEtl.result)))
                Model.execute()
                Automatizacion.execute_aut()
                CleanFolder.cleanProcess(parameters=parameters, process=process)
                            
        finally: #Notificación
                           
            #Envio Correo WS
            try:
                mailParameters = MailParametersDb.getWSParameters(process='WS')
            except:
                mailParameters = MailParametersJson.getDefaultEmailParameters()
            MailManagement.enviar_correo_ws(mailParameters)
            try:
                LoggingHandler.insertLogIntoBd()
                LoggingHandler.emit(*LogCodification.log_into_bd_sucess())
            except Exception as ex:
                LoggingHandler.emit(*LogCodification.log_into_bd_exception(ex = str(ex)))
            finally:
                LoggingHandler.logIntoTxt()
            
