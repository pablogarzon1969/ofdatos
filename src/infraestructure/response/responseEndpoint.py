from typing import Any


class ResponseEndPoint:

    @classmethod
    def structureResponse(cls, result) -> dict[str, Any]:
        return {"msgRsHdr": {"error": None}, "body": {"result": result}}

    @classmethod
    def structureResponseError(cls, statusDesc: str, category: str, additionalstatusDesc: str, serverStatusCode: int) -> dict[str, Any]:
        return {"msgRsHdr":
                {"error":
                 {"statusCode": 200,
                  "severity": None,
                  "statusDesc": statusDesc,
                  "additionalStatus":
                  {"serverStatusCode": serverStatusCode,
                   "category": category,
                   "statusDesc": additionalstatusDesc}}},
                "body": {"result": None}}
