from unicodedata import name
from src.domain.response.fileParametersResponse import FileParametersResponse
import shutil
import os
import time

class MoveFile():
    def moveProcess(parameters:FileParametersResponse, process:str):
        if parameters.inputFileName.__contains__('%'):
            shutil.move(parameters.inputPath+ parameters.inputFileName.replace('%FechaSistema%',time.strftime("%Y%m%d"))+ parameters.inputFileType, parameters.processPath+ parameters.inputFileName.replace('%FechaSistema%',time.strftime("%Y%m%d"))+ parameters.inputFileType)
        else: 
            shutil.move(parameters.inputPath+ parameters.inputFileName+ parameters.inputFileType, parameters.processPath+ parameters.inputFileName+ parameters.inputFileType)

        return 0