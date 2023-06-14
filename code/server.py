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

server.py: This file is launching the uvicorn webserver for the Meross2Alluvio api

Required 3rd components:
    - pip install meross_iot==0.4.5.9
    - pip install fastapi
    - pip install 'uvicorn[standard]'
    - pip install cryptography
    
"""

import uvicorn
import json

# Load config.json 
with open("config.json") as json_data_file:
    data = json.load(json_data_file)

# Launch WebServer with config.json parameter
if __name__ == "__main__":
    uvicorn.run("main:app", host=data['webserver']['host'],
                            port=int(data['webserver']['port']),
                            reload=False, 
                            log_level=data['webserver']['loglevel'],
                            workers=int(data['webserver']['workers']), 
                            limit_concurrency=int(data['webserver']['limit_concurrency']),
                            limit_max_requests=int(data['webserver']['limit_max_requests'])
                            )
    
