from src.domain.response.fileParametersResponse import FileParametersResponse
from pandas.core.frame import DataFrame
from src.dataStorage.file import File

class FileManagement:
    
    @classmethod
    def importFile(cls, process:str, parameters:FileParametersResponse) -> DataFrame:
        print('Inicio Importación del archivo: ', parameters.inputFileName or 'None')
        file:DataFrame = File.getFile(parameters=parameters, process=process)
        return file
    
    @classmethod
    def exportFile(cls, file:DataFrame, process:str, parameters:FileParametersResponse) -> DataFrame:
        print('Inicio Exportación del archivo:' + parameters.outputFileName or 'None')
        File.writeFile(file = file, process = process, parameters = parameters)
        