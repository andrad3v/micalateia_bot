import requests
from cogs.utils.config import APIS


title = "Overgeared"
req = requests.get(f"{APIS['mangadex']['base_url']}/manga",
                   params={"title": title})
print([manga["id"]["title"] for manga in req.json()["data"]])