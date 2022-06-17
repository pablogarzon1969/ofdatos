from typing import Any

from src.infraestructure.log.logData import LogData
from src.data.repository.logRepository import LogRepository

class LogManagement:

    @classmethod
    async def saveLogAsync(cls, log: LogData):
        await LogRepository.saveLog(log)

    @classmethod
    async def saveLog(cls, log: LogData):
        await LogRepository.saveLog(log)