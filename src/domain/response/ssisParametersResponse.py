from pydantic import BaseModel

class SsisParametersResponse (BaseModel):
    jobname : str
    timelimit: str
    debug : str
    status : str