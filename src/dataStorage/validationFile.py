from os import listdir
from os.path import isfile, join, getmtime
from src.infraestructure.log.loggingHandler import LoggingHandler
from src.infraestructure.log.logCodification import LogCodification
from src.agentservices.mail.mailParametersDB import MailParametersDb
from src.agentservices.mail.mailManagement import MailManagement
from src.domain.response.mailSendResponse import MailSendResponse
from pandas.core.frame import DataFrame
from time import time


#El objetivo del siguiente bloque de codigo es recorrer el directorio de input, excluir todo lo que no
#es un archivo, posteriormente se crea una lista de archivos validos la cual contiene archivos que cumplen
#con el formato especificado para la presente fuente, es decir que el nombre del archivo debe ser igual a
#input_file y la extension debe ser igual a input_file_format. 
#Si se encuentran varios archivos que cumplen con la condicion (que no deberia ser ya que se espera solo
#un archivo por fuente por carga), se carga el archivo mas reciente. 

class ValidationFile():
    
    @classmethod
    def validationFileName(cls, filePath:str, formatFile:str, fileName:str,fileRequired:str, process:str) -> str:
     #   try:
        validFileList= list()
        files = [f for f in listdir(filePath) if isfile(join(filePath, f))]

        try:
            if len(files) >=1:
                    
                filesInDirectory=list()
                for file in files:
                    if '.' in file and '~'not in file and '$' not in file:
                        filesInDirectory.append(file)
                    
                for file in range(len(filesInDirectory)):
                    name= filesInDirectory[file].split('.')[0]
                    name= name.lstrip().rstrip()

                    extension_archivo= filesInDirectory[file].split('.')[1]
                    extension_archivo= '.' + extension_archivo
                        
                    if fileName.upper() in name.upper() and  formatFile == extension_archivo:
                        validFileList.append(filesInDirectory[file])
                validationResponse=validFileList[-1]
                                                                        
            else:
                if  fileRequired == "1":
                    LoggingHandler.emit(*LogCodification.import_file_not_in_path(process=process, objectPy=fileName+formatFile, path = filePath))
                    mailParameters = MailParametersDb.getMsgParameters(process='MNS001D.MSG01')
                    if isinstance(mailParameters, MailSendResponse):
                        MailManagement.enviar_correo_ws(mailParameters) 
                return None
            
        except:
            if  fileRequired == "1":
                LoggingHandler.emit(*LogCodification.import_file_not_in_path(process=process, objectPy=fileName+formatFile, path = filePath))
                mailParameters = MailParametersDb.getMsgParameters(process='MNS001D.MSG01')
                if isinstance(mailParameters, MailSendResponse):
                    MailManagement.enviar_correo_ws(mailParameters)
            return None

        return validationResponse
        