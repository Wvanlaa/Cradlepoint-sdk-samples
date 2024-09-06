import time
from csclient import EventingCSClient
cp = EventingCSClient('tunnel-status')

APP_NAME = 'tunnel_status'
DEBUG = True

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

        tunnel_status = "SC:"

        tunnels = cp.get('/status/vpn/tunnels/')
        """Get status of all VPN Tunnels"""
        if tunnels:
            for tunnel in tunnels:        
                if tunnel['state'] == "up":
                    tunnel_status += " 🟢 "
                    tunnel_status += (tunnel['name'])
                elif tunnel['state'] == "standby":    
                    tunnel_status += " 🟡 "
                    tunnel_status += (tunnel['name'])                   
                else:
                    tunnel_status += " 🔴 "
                    cp.log(tunnel['name'])
                        
                  

        """Write string to description field"""
        if DEBUG:
            cp.log("WRITING DESCRIPTION")
            cp.log(tunnel_status)
        cp.put('config/system/asset_id', tunnel_status)
        

    except Exception as err:
        cp.log("Failed with exception={} err={}".format(type(err), str(err)))

    """Wait 5 seconds before checking again"""
    time.sleep(60)
    
   
