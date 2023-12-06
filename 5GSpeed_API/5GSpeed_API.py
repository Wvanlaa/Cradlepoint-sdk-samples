"""5GSpeed_API runs Ookla speedtests and puts results into the asset_id field.  Designed to enable NCM API support for Ookla speedtests.

Info:
=====
Based on Speedtest-CLI from Matt Martz (https://github.com/sivel) and __version__ = '2.1.4b1'
Upload is done first, because that has the highest likelyhood of failing and making the script "loop".
So IF that happens no unneeded download cycles are wasted.
To prevent "NCM Sync Issues" a 10 second pause is used before the results are pushed to the Asset_ID field


Steps to use:
=============
Clear the asset_id by performing any of the following:

1. Use NCM API PUT router request to clear the asset_id field and to run the SDK speedtest. Wait for 1 min, and run NCM API Get router request to get the result.

2. Clear the asset_id in NCM > Devices tab (click pencil icon)

3. Go to device console and clear results field:
put config/system/asset_id ""

Sample result:
DL:52.54Mbps - UL:16.55Mbps - Ping:9.715ms - Server:Telstra - ISP:Vocus Communications - TimeGMT:2023-04-11T01:06:43.758382Z - URL:http://www.speedtest.net/result/14595594656.png

Retrieve Results via NCM API:
=============================
Generate NCM API v2 API Keys on the Tools page > NetCloud API tab in NCM.
Use those keys in the headers of an HTTP GET request to https://www.cradlepointecm.com/api/v2/routers/{router_id/
router_id can be found in NCM or at CLI: get status/ecm/client_id
The results are in the asset_id field.

Clear results and run new test via NCM API:
===========================================
Use API keys in headers of an HTTP PUT request to https://www.cradlepointecm.com/api/v2/routers/{router_id/
Content-Type: application/json
Body contains blank asset_id field:
{"asset_id": ""}

In a few minutes, new results should populate.
"""

from csclient import EventingCSClient
from speedtest import Speedtest
import time

results_path = "config/system/asset_id"


def results_field_check(path, results, *args):
    try:
        if not results:
            cp.log('Initiating Speedtest due to cleared results...')
            speedtest()
        else:
            cp.log(f'5GSpeed ready. To start speedtest: put {results_path} ""')
        return
    except Exception as e:
        cp.logger.exception(e)

def speedtest():
    try:
        cp.log('Starting Speedtest...')
        s = Speedtest()
        server = s.get_best_server()
        cp.log(f'Found Best Ookla Server: {server["sponsor"]}')
        # Always run "upload" first! If upload fails it does not consume unneeded download cycles.
        time.sleep(5)
        cp.log("Performing Ookla Upload Test...")
        u = s.upload(pre_allocate=False)
        time.sleep(5)
        cp.log("Performing Ookla Download Test...")
        d = s.download()
        download = '{:.2f}'.format(d / 1000 / 1000)
        upload = '{:.2f}'.format(u / 1000 / 1000)
        cp.log('Ookla Speedtest Complete! Results:')
        cp.log(f'Client ISP: {s.results.client["isp"]}')
        cp.log(f'Ookla Server: {s.results.server["sponsor"]}')
        cp.log(f'Ping: {s.results.ping}ms')
        cp.log(f'Download Speed: {download}Mb/s')
        cp.log(f'Upload Speed: {upload} Mb/s')
        cp.log(f'Ookla Results Image: {s.results.share()}')
        text = f'DL:{download}Mbps - UL:{upload}Mbps - Ping:{s.results.ping}ms - Server:{s.results.server["sponsor"]} - ISP:{s.results.client["isp"]} - TimeGMT:{s.results.timestamp} - Img:{s.results.share()}'
        time.sleep(10)
        # 10 second wait is put in to allow proper sync with NCM
        cp.put(results_path, text)
        cp.alert(text)
        return
    except Exception as e:
        cp.logger.exception(e)

cp = EventingCSClient('5GSpeed_API')
try:
    cp.log('Starting...')
    while not cp.get('status/wan/connection_state') == 'connected':
        time.sleep(2)
    cp.on('put', results_path, results_field_check)
    boot_results = cp.get(results_path)
    results_field_check(None, boot_results, None)
    time.sleep(999999)
except Exception as e:
    cp.logger.exception(e)
