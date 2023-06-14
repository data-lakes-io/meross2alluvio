"""
Copyright 2013, Data-Lakes.io, Oliver Oehlenberg

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the “Software”), to deal in the Software without 
restriction, including without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---------------------------------------------------------------------------------------------

Please launch the service via the server.py file. This file is the main file to provide
the web/api services.

"""

import models as models

from fastapi import FastAPI, Header
from merossconsumption import requestInstantConsumption
from merossconsumption import requestDailyConsumption
from tokenhandler import requestBuildCredentials
from tokenhandler import isTokenValid
from tokenhandler import getCredentials
from typing import Annotated



app = FastAPI()

@app.get("/status")
def read_status():
    return {"Ready":"True"}

@app.post("/admin/buildcredentials")
async def create_request_build_credentials(model: models.RequestCredentials):
    return await requestBuildCredentials(model)

@app.post("/consumption")
async def create_request_consumption(model: models.RequestConsumption,
                                     nonce: Annotated[list[str] | None, Header()] = None,  
                                     token: Annotated[list[str] | None, Header()] = None,
                                     connectionstring: Annotated[list[str] | None, Header()] = None):
    # Check all parameter
    if (token is None):
        return { "Invalid Request: Token Header missing" }    
    if (connectionstring is None):
        return { "Invalid Request: Connection Header missing" }
    if (nonce is None):
        return { "Invalid Request: Nonce Header missing" }

    if (await isTokenValid(token[0]) == 0):
        return {"Invalid Request: Invalid Token"}

    # Get Credentials
    credentials = await getCredentials(connectionstring[0],nonce[0],token[0])
    if (credentials[0] == ""):
        return {"Invalid Request: Credentials can not be found" }
    
    return await requestInstantConsumption(model,credentials[0],credentials[1])


@app.post("/daily")
async def create_request_consumption(model: models.RequestConsumption,
                                     nonce: Annotated[list[str] | None, Header()] = None,  
                                     token: Annotated[list[str] | None, Header()] = None,
                                     connectionstring: Annotated[list[str] | None, Header()] = None):
    
    # Check all parameter
    if (token is None):
        return { "Invalid Request: Token Header missing" }    
    if (connectionstring is None):
        return { "Invalid Request: Connection Header missing" }
    if (nonce is None):
        return { "Invalid Request: Nonce Header missing" }

    if (await isTokenValid(token[0]) == 0):
        return {"Invalid Request: Invalid Token"}

    # Get Credentials
    credentials = await getCredentials(connectionstring[0],nonce[0],token[0])
    if (credentials[0] == ""):
        return {"Invalid Request: Credentials can not be found" }

    return await requestDailyConsumption(model,credentials[0],credentials[1])

