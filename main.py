from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

client = Client(token="cYmsCNvC8s4nvkvmfGfISAVe487dGe9ijmd9t2eMSLo1dsAfYIPfH7w2PMdRtA7A")
def create_vps():
    response = client.servers.create(
        name="my-server",
        server_type=ServerType(name="cx11"),
        image=Image(name="ubuntu-22.04"),
    )
    server = response.server
    print(f"{server.id=} {server.ip=} {server.status=}")
    print(f"root password: {response.root_password}")




def show_vps_inf():
    servers = client.servers.get_by_id(42819738)
    print(servers.public_net.ipv4.ip)


show_vps_inf()