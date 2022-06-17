from pandas.core.frame import DataFrame
from src.clean.dateClean import CleanDate
from src.clean.stringClean import CleanString
from src.clean.numericClean import CleanNumeric
from src.clean.stringAlphabeticClean import CleanAlphabetic
from src.clean.stringAlphanumericClean import CleanAlphanumeric
from src.clean.numericIntegerClean import CleanInteger
from src.clean.numericDecimalClean import CleanDecimal
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from src.domain.response.fileParametersResponse import FileParametersResponse

class DataCleaning():
    
    @classmethod
    def cleanData(cls, df : DataFrame, process :str, parameters : FileParametersResponse) -> DataFrame:
        print('Inicio Limpieza del archivo:' + parameters.inputFileName)
        try:
            objectPy = parameters.inputFileName + parameters.inputFileType
            validaterow : int = 0
            for col_name in df.columns:
                if col_name in parameters.textColumns:
                    CleanString.cleanString(df, col_name)
                elif col_name in parameters.dateColumns:
                    CleanDate.cleanDate(df, col_name)
                elif col_name in parameters.numericColumns:
                    CleanNumeric.cleanNumeric(df, col_name)
                else:
                    validaterow = 1
                    LoggingHandler.emit(*LogCodification.cleanUnspecifiedDataType(process=process, objectPy=objectPy, col_name=col_name))
           
            if validaterow == 0: #Si no ocurrieron errores, se crea el registro de que no falló
                LoggingHandler.emit(*LogCodification.clean_success(process=process, objectPy=objectPy))
            else:
                raise #No sé que hacer aún
            return df
        
        except Exception as ex: #Se llama este error en otro caso
            error:str = str(ex)
            LoggingHandler.emit(*LogCodification.clean_other_exception(process=process, objectPy=objectPy, error=error))