from enum import Enum

class FileParametersRequest(Enum):
    
    #Parámetros de rutas
    inputPath = 'FS_USUARIOS_PATH'
    outputPath = 'FS_OUTPUT_PATH'
    processPath = 'PROCESS_FILE_PATH'
    
    #Parámetros generales
    inputFileName = 'INPUT_FILE'
    inputFileType = 'INPUT_FORMAT'
    inputFileColRange = 'INPUT_FILE_COL_RANGE'
    inputFileHeader = 'INPUT_FILE_HEADER'
    outputFileName = 'OUTPUT_FILE'
    outputFileType = 'OUTPUT_FORMAT'
    fileSheet = 'INPUT_FILE_SHEET_NAME'
    fileColumnNames = 'FILE_COLUMNS'
    fileRequired = 'FILE_REQUIRED'

    #Parámetros de limpieza
    textColumns = 'TEXT_COLUMNS'
    numericColumns = 'NUMERIC_COLUMNS'
    dateColumns = 'DATE_COLUMNS'