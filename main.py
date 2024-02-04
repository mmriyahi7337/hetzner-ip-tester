import os
import requests
from dotenv import load_dotenv
from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

load_dotenv()
Token = os.getenv("Token")

client = Client(token=Token)
#TODO: add check host section

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


def create_vps():
    response = client.servers.create(
        name="my-server",
        server_type=ServerType(name="cx11"),
        image=Image(name="ubuntu-22.04"),
    )
    server = response.server
    print(f"{server.id=} {server.ip=} {server.status=}")
    print(f"root password: {response.root_password}")
# TODO: add multi server for checking or multi tread



#TODO: add a var for number of ip check or clean ip
#TODO: add array for holding ips and counter

def show_vps_inf():
    servers = client.servers.get_by_id(42819738)
    print(servers.public_net.ipv4.ip)


show_vps_inf()