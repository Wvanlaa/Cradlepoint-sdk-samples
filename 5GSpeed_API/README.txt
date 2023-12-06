Application Name
================
5GSpeed_API

Application Purpose
===================
5GSpeed_API runs Ookla speedtests and puts results into the asset_id field.  Designed to enable NCM API support for Ookla speedtests.

Steps to use:
=============
Clear the asset_id by performing any of the following:

1. Use NCM API PUT router request to clear the asset_id field and to run the SDK speedtest. Wait for 1 min, and run NCM API Get router request to get the result.

2. Clear the asset_id in NCM > Devices tab (click pencil icon)

3. Go to device console and clear results field:
put config/system/asset_id ""

Sample result:
DL:52.54Mbps - UL:16.55Mbps - Ping:9.715ms - Server:Telstra - ISP:Vocus Communications - TimeGMT:2023-04-11T01:06:43.758382Z - URL:http://www.speedtest.net/result/<somenumber>.png

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