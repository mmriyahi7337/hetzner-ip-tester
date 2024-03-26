import os
import time

import requests
from dotenv import load_dotenv
from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType
from hcloud.servers import ServersClient
from hcloud.primary_ips import PrimaryIPsClient

load_dotenv()
Token = os.getenv("Token")

client = Client(token=Token)
serverclient = ServersClient(client=client)
primaryips = PrimaryIPsClient(client=client)


# TODO: tidy up code
def testip(ip):
    url = f"https://check-host.net/check-tcp?host={ip}:22"

    payload = {}
    headers = {'Accept': 'application/json'}

    response = requests.request("GET", url, headers=headers, data=payload)
    respose = response.json()
    result = respose['request_id']
    url = f"https://check-host.net/check-result/{result}"
    res = requests.request("GET", url, headers=headers, data=payload)
    r = res.json()
    filtered_nodes = []
    for node in r:
        if node.startswith('ir'):
            filtered_nodes.append(node)
    approve = 0
    denied = 0

    try:
        for i in filtered_nodes:
            time = r[i][-1]['time']
            if time > 0:
                approve = approve + 1
            else:
                continue
        if approve >= 3:
            return True


    except:
        denied = 0
        for i in filtered_nodes:
            if r[i] == None:
                denied = denied + 1
        if denied <= 3:
            return False


# TODO: error handle for this section
def unaasign_ip(server, primaryip):
    response = serverclient.power_off(server)
    time.sleep(10)
    rs = primaryips.unassign(primaryip)


# TODO : error handle
# TODO : datacenters loc id or name
def assign_ip(server, primaryip, datacenter):
    # rs_ip = primaryips.create(name="primary", type="ipv4", datacenter=datacenter)
    rs_ip = primaryips.get_by_name("primary")
    pp = primaryips.assign(primary_ip=rs_ip, assignee_id=server.id)
    serverclient.power_on(server)
    return pp


def create_vps():
    response = client.servers.create(
        name="my-server",
        server_type=ServerType(name="cx11"),
        image=Image(name="ubuntu-22.04"),
    )
    server = response.server
    # print(f"{server.id=} {server.ip=} {server.status=}")
    # print(f"root password: {response.root_password}")
    return server


# TODO: add multi server for checking or multi tread


# TODO: add a var for number of ip check or clean ip
# TODO: add array for holding ips and counter
# TODO: delete the extra ips

# TODO: delete this section
def show_vps_inf(id):
    servers = client.servers.get_by_id(id)
    return servers.public_net.ipv4.ip


# server = create_vps()
server = serverclient.get_by_id(45012665)
# server_ip_by_id = server.public_net.primary_ipv4.id
d = primaryips.get_by_id(54841603)
dc = d.datacenter
# print(server_ip_by_id)
# print(server_id)
# server_id = '45012095'
# ip = show_vps_inf(server.id)
# print(testip(ip))
# time.sleep(30)
# print(unaasign_ip(server,d))
print(assign_ip(server, d, dc))
