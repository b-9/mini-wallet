from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def response_handler(status_code, data={}, message="", status="success"):
    data = jsonable_encoder(data)
    return JSONResponse({"data": data, "status": status}, status_code=status_code)
