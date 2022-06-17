
from src.data.repository.processesRepository import ProcessesRepository
from src.data.repository.parametersRepository import ParametersRepository
from src.domain.response.fileParametersResponse import FileParametersResponse
from src.infraestructure.error.errorCategory import ErrorCategory
from typing import List

#Eliminar este archivo
class ParametersDataStorage():

    @classmethod
    def getFileParameters(cls, process: str) -> FileParametersResponse:
        responseRepository = None
        responseRepository = ParametersRepository.getParameters(process)
        if responseRepository == None:
            return ErrorCategory.Business
        return responseRepository
    
    @classmethod
    def getFileList(cls) -> List:
        responseRepository = None
        responseRepository = ProcessesRepository.getFileList()
        if responseRepository == None:
            return ErrorCategory.Business
        filelist = responseRepository['processes'].split(', ')
        return filelist