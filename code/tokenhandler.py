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

Please launch the service via the server.py file. This file is managing the token requests

"""

import models as models
import json
import logging
import hashlib
import base64

from cryptography.fernet import Fernet



async def requestBuildCredentials(model: models.RequestCredentials):
    # Validate Token
    token = await validateToken(model.token)    
    if (token[0] == ""):
        return { "credentials" : "", "status" : "Failed, invalid token"}
    
    # Load Config
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)

    # Prepare Credentials
    credentials = { "email": model.cloudEmail, "pwd": model.cloudPwd }
    credentialsJson = json.dumps(credentials).encode('utf-8')

    # Build Encryptior
    secret = ("%s%s%s" % (model.nonce, data['common']['salt'], token[0])).encode('utf-8')    
    secretHash = base64.urlsafe_b64encode(hashlib.shake_256(secret).hexdigest(16).encode('utf-8'))
    f = Fernet(secretHash)
    enc = base64.urlsafe_b64encode(f.encrypt(credentialsJson))

    return { "credentials" : enc, "status" : "OK"}

async def getCredentials(connectionString: str, nonce: str, tokenstr: str):

    try:

        # Validate Token
        token = await validateToken(tokenstr)    
        if (token[0] == ""):
            return "", ""

         # Load Config
        with open("config.json") as json_data_file:
            data = json.load(json_data_file)
    
        # Decrypt
        secret = ("%s%s%s" % (nonce, data['common']['salt'], token[0])).encode('utf-8')    
        secretHash = base64.urlsafe_b64encode(hashlib.shake_256(secret).hexdigest(16).encode('utf-8'))
        f = Fernet(secretHash)
        dec = (f.decrypt(base64.urlsafe_b64decode(connectionString))).decode('utf-8')
        credJson = json.loads(dec)
        return credJson["email"],credJson["pwd"]

    except:
        logging.warning("Credential can not extracted from connection string!")
        return "", ""

async def isTokenValid(token: str):
    result = await validateToken(token)
    if (result[0] == ""):
        return 0
    return 1

async def validateToken(token: str):
    
    # Load config.json 
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)

    for t in data['tokens']:
        cToken = data['tokens'][t]
        cOwner = t
        if cToken == token:
            logging.info("\tRequest Token successful validated")
            return cOwner, cToken
    
    logging.warning(f"\tInvalid Request Token {token}")
    return "",""


