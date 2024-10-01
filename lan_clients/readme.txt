Application Name
================
lan_clients


Application Version
===================
1.0


NCOS Devices Supported
======================
ALL


External Requirements
=====================
None


Application Purpose
===================
Get the lan client stats and put in asset ID to be sync'd to NCM

If line 28 is uncommented it is also possible to generate a "Custom Alert" to show the clients.
this however can be very verbose as this would be logged every 90 seconds

Expected Output
===============
LAN client stats in "Asset Identifier" field of NCM
Updates every 90 seconds

