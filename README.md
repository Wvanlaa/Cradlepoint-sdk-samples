# Cradlepoint-sdk-samples
Inspiration based on the Cradlepoint OpenSource SDK's
----------

This directory contains the NCOS SDK tools and sample applications mainly based on the Cradlepoint GitHub.
- For the originals please visit: [Cradlepoint GitHub Pages](https://github.com/cradlepoint/sdk-samples/tree/master)


## Documents

- **README.html**
    - This README file.

## Sample Application Directories

- **ibr200lan_status**
    - Display the port status of the LAN port on an IBR200 in the Asset Identifier field in NCM to quickly identify (dis)connected Industrial Computer
    - Obviously this works for other routers to monitor the LAN port

- **5GSpeed_API**
    - Run speedtest (that can be triggered using API towards NCM) and display the result in the Asset_ID field.
    - But also create a "custom alert" with the results so it can be send to a system that accepts Webhook API calls (push-API)
    - It runs on the "active WAN" connection regardless what it is, and does not impact services.
    - If "the fastest" sim needs to be picked there are other SDK's that can do that.

- **lan_clients**
    - Display connected LAN clients (wired or wireless) MAC address on the Asset Identifier field in NCM
 
- **built_apps**
    - Built and ready to use versions of the apps
