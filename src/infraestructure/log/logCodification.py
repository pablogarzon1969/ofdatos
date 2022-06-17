
class LogCodification():
    
    #Substring
        
    #Registros BD
    def bd_error(error:str):
        return [0 ,'ERROR CONEXIÓN BASE DE DATOS', 'DB', '', '', 'SI', error]
    
    #Registros lista procesos
    def processes_success():
        return [1 ,'OBTENCION LISTA PROCESOS', 'GLOBAL', '', '', 'NO', '']
    
    def processes_not_defined():
        return [1, 'OBTENCION LISTA PROCESOS', 'GLOBAL', '', '', 'SI', 'NO ESTA DEFINIDO UN PARAMETRO PROCESSES EN BD']
    
    def process_is_empty():
        return [1 ,'OBTENCION LISTA PROCESOS', 'GLOBAL', '', '', 'SI', 'EL PARAMETRO PROCESESSES ESTA VACIO']
    
    def process_other_exception(error:str):
        return [1 ,'OBTENCION LISTA PROCESOS', 'GLOBAL', '', '', 'SI',  error]
    
    #Registros obtención parámetros
    def parameters_success(process:str):
        return [2 ,'OBTENCION PARAMETROS', process, '', '', 'NO', '']
    
    def parameters_missing(process:str, parameter:str):
        return [2 ,'OBTENCION PARAMETROS', process, '', '', 'SI', 'FALTA EL PARAMETRO ' + parameter]
    
    def parameters_other_exception(error:str, parameter:str, process:str):
        return [2 ,'OBTENCION PARAMETROS', process, '', '', 'SI', 'FALTA EL PARÁMETRO ' + parameter + ': ' + error]
    
    #Registros importacion archivo
    def import_sucess(process : str, objectPy : str):
        return [3 ,'IMPORTACION ARCHIVO', process, objectPy, '', 'NO', '']
    
    def import_invalid_file_type(process, objectPy):
        return [3 ,'IMPORTACION ARCHIVO', process, objectPy, '', 'SI', 'EL CAMPO INPUT_FILE_TYPE EN LA TABLA DE PARÁMETROS ESTÁ VACIO O NO ES XLSX O CSV']

    def import_file_not_in_path(process, objectPy, path:str):
        return [3 ,'IMPORTACION ARCHIVO', process, objectPy, '', 'SI', 'EL ARCHIVO NO ESTÁ EN LA RUTA']
    
    def import_other_exception(process, objectPy, ex):
        return [3 ,'IMPORTACION ARCHIVO', process, objectPy, '', 'SI', 'NO SE PUDO IMPORTAR EL ARCHIVO: ' + str(ex)]
    
    #Registro limpieza archivo
    def clean_success(process:str, objectPy:str):
        return [4 ,'LIMPIEZA ARCHIVO', process, objectPy, '', 'NO', '']
    
    def cleanUnspecifiedDataType(process:str, objectPy:str, col_name:str):
        return [4 ,'LIMPIEZA ARCHIVO', process, objectPy, '', 'SI', 'NO ESTÁ ESPECIFICADO EL TIPO DE DATO DE LA COLUMNA EN TABLA DE PARÁMETROS(BD): ' + col_name]
    
    def clean_other_exception(process:str, objectPy:str, error:str):
        return [4 ,'LIMPIEZA ARCHIVO', process, objectPy, '', 'SI', 'HUBO UN ERROR DURANTE LA LIMPIEZA DEL ARCHIVO: ' + error]
    
    #Registros exportacion archivo
    def export_success(process : str, objectPy : str):
        return [5 ,'EXPORTACION ARCHIVO', process, objectPy, '', 'NO', '']
    
    def export_invalid_file_type(process : str, objectPy : str):
        return [5 ,'EXPORTACION ARCHIVO', process, objectPy, '', 'SI', 'EL CAMPO OUTPUT_FILE_TYPE EN LA TABLA DE PARÁMETROS ESTÁ VACIO O NO ES XLSX O CSV']
    
    def export_other_exception(process : str, objectPy : str, ex : str):
        return [5 ,'EXPORTACION ARCHIVO', process, objectPy, '', 'NO', 'NO SE PUEDO EXPORTAR EL ARCHIVO: ' + ex]
    
    #Registros envio correo
    def email_sucess():
        return [6 ,'ENVIO DE CORREO', 'WS', '', '', 'NO', '']
    
    def email_exception(ex:str):
        return [6 ,'ENVIO DE CORREO', 'WS', '', '', 'SI', ex]
    
    #Registros subida registro a bd
    def log_into_bd_sucess():
        return [7 ,'SUBIDA LOG BD', 'BD', '', '', 'NO', '']
    
    def log_into_bd_exception(ex:str):
        return [7 ,'SUBIDA LOG BD', 'BD', '', '', 'NO', ex]
    
    #Registros etl
    def ssis_ejecution_sucess():
        return [8 ,'EJECUCIÓN ETL', 'BD', '', '', 'NO', '']
    
    def ssis_ejecution_not_success(resultEtl:str):
        return [8 ,'EJECUCIÓN ETL', 'BD', '', '', 'SI', 'LA RESPUESTA DE LA ETL ES ' + resultEtl]
    
    def ssis_ejecution_exception(ex:str):
        return [8 ,'EJECUCIÓN ETL', 'BD', '', '', 'SI', ex]
    
    #Subida logs a bd
    
    def database_log_failure(ex:str):
        return [9 ,'SUBIDA LOGS A BD', 'BD', '', '', 'SI', ex]