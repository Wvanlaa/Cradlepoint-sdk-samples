# lan_clients - put lan clients in desc to sync to NCM
import time
from csclient import EventingCSClient
cp = EventingCSClient('LAN_Clients')
cp.log('Starting...')
while True:
    all_clients_string = ''
    clients = []
    lan_clients = cp.get('status/lan/clients')
    for client in lan_clients:
        if "fe80" not in client["ip_address"]:  # Ignore IPv6
            clients.append(client)
    wlan_clients = cp.get('status/wlan/clients')
    for i, client in enumerate(clients):
        all_clients_string += client["mac"].upper()
        for wlan_client in wlan_clients:
            if client["mac"] == wlan_client["mac"]:  # WiFi Client
                radio = ' 5Ghz' if wlan_client["radio"] else " 2.4Ghz"
                all_clients_string += f'{radio} {wlan_client["rssi0"]}'
        if i < len(clients) - 1:
            all_clients_string += ', '
    all_clients_string = f'Clients ({len(clients)}) - ' + all_clients_string
 #  select "description" or "asset ID" field by commenting out one of these lines
 #   cp.put('config/system/desc', all_clients_string[:255])
    cp.put('config/system/asset_id', all_clients_string[:255])
    cp.log(all_clients_string[:255])
 #  remove comment on following line if a "custom alert" is needed with the information of the clients connected is needed   
 #   cp.alert(all_clients_string[:255])
 #
 #  change the default timer of 90 seconds if less frequent updates are needed
    time.sleep(90)
