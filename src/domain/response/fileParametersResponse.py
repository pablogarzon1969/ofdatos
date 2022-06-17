from pydantic import BaseModel

class FileParametersResponse (BaseModel):
    
    #Parametros Globales
    inputPath : str    
    outputPath : str
    processPath : str
    
    #Parámetros Generales
    inputFileName : str
    inputFileType : str
    inputFileColRange : str
    inputFileHeader : str
    outputFileName : str
    outputFileType : str
    fileSheet : str
    fileColumnNames : str
    fileRequired : str

    #Parámetros de Limpieza
    textColumns : str
    numericColumns : str
    dateColumns : str
    
class ParameterResponse (BaseModel):
    parameter : str
    