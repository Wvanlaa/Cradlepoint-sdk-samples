import time
from csclient import EventingCSClient
cp = EventingCSClient('ports-status')

APP_NAME = 'PORTS_STATUS'
DEBUG = True
MODELS_WITHOUT_WAN = ['CBA', 'W200', 'W400', 'L950', 'IBR200', '4250', 'W185']

if DEBUG:
    cp.log("DEBUG ENABLED")

if DEBUG:
    cp.log("Getting Model")

"""Get model number, since some models don't have ethernet WAN"""
model = ''
model = cp.get('/status/product_info/product_name')
if DEBUG:
    cp.log(model)

while True:
    try:
        ports_status = ""

        wans = cp.get('/status/wan/devices')

        ports_status += "LAN:"

        ports = cp.get('/status/ethernet')
        """Get status of all ethernet ports"""
        if ports:
            for port in ports:
                """Ignore ethernet0 (treat as WAN) except for IBR200/CBA"""
                if (port['port'] == 0 and any(x in model for x in MODELS_WITHOUT_WAN)) or (port['port'] >= 1):
                    if port['link'] == "up":
                        ports_status += " 🟢 "
                    else:
                        ports_status += " 🔴 "
                        
                  

        """Write string to description field"""
        if DEBUG:
            cp.log("WRITING DESCRIPTION")
            cp.log(ports_status)
        cp.put('config/system/asset_id', ports_status)
        

    except Exception as err:
        cp.log("Failed with exception={} err={}".format(type(err), str(err)))

    """Wait 5 seconds before checking again"""
    time.sleep(60)
    
   
