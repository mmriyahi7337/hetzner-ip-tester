from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType
from dotenv import load_dotenv
import os

load_dotenv()
Token = os.getenv("Token")

#TODO: add secret file
client = Client(token=Token)
#TODO: add check host section
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

def show_vps_inf():
    servers = client.servers.get_by_id(42819738)
    print(servers.public_net.ipv4.ip)


show_vps_inf()