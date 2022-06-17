from enum import Enum

class SsisParametersRequest(Enum):
    
    #Parámetros SSIS
    jobname = 'JOBNAME'
    timelimit = 'TIMELIMIT'
    debug = 'DEBUG'
    status = 'STATUS'