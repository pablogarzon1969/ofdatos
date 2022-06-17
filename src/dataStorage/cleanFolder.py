from unicodedata import name
from src.domain.response.fileParametersResponse import FileParametersResponse
import shutil
import os
import time

class CleanFolder():
    def cleanProcess(parameters:FileParametersResponse, process:str):
        for filename in os.listdir(parameters.outputPath):
            file_path = os.path.join(parameters.outputPath, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        return 0
 
    