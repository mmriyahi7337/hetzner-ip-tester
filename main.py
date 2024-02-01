from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType

client = Client(token="cYmsCNvC8s4nvkvmfGfISAVe487dGe9ijmd9t2eMSLo1dsAfYIPfH7w2PMdRtA7A")

response = client.servers.create(
    name="my-server",
    server_type=ServerType(name="cx11"),
    image=Image(name="ubuntu-22.04"),
)
server = response.server
print(f"{server.id=} {server.name=} {server.status=}")
print(f"root password: {response.root_password}")