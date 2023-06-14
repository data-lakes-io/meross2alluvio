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

Please launch the service via the server.py file. This py file is performing the rest api 
requests to the moeross backend.

"""

import models as models
import os

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager


async def requestInstantConsumption(model: models.RequestConsumption, EMAIL: str, PASSWORD: str):
    
    # Init Meross API
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Search for Device
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_name=model.deviceName)
    if len(plugs) < 1:
        print(f"Requested Device {model.deviceName} not found in Meross Device List")
        return "DEVICENAME_NOT_FOUND_OR_ONLINE"
    else:
        dev = plugs[0]
        await dev.async_update()

        # Request Consumption 
        instant_consumption = await dev.async_get_instant_metrics()  
      
    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

    return  {               
               "powerWatt" : instant_consumption.power,
               "voltage" : instant_consumption.voltage,
               "currentAmp" : instant_consumption.current
            }




async def requestDailyConsumption(model: models.RequestConsumption, EMAIL: str, PASSWORD: str):
    
    # Init Meross API
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Search for Device
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_name=model.deviceName)
    if len(plugs) < 1:
        print(f"Requested Device {model.deviceName} not found in Meross Device List")
        return "DEVICENAME_NOT_FOUND_OR_ONLINE"
    else:
        dev = plugs[0]
        await dev.async_update()

        # Request Consumption 
        daily_consumption = await dev.async_get_daily_power_consumption()             

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

    return daily_consumption
            
