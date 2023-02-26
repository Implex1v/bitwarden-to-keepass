from dataclasses import dataclass

from bitwardentools import Client


@dataclass()
class BitWardenEntry:
    name: str = None
    username: str = None
    password: str = None
    uri: str = None
    notes: str = None
    totp: str = None
    folder: str = None


class BitWardenClient:
    client: Client
    folder_cache: dict[str, str] = {}

    def __init__(self, url: str, email: str, password: str):
        self.client = Client(url, email, password)
        self.client.sync()

    def _map(self, entry: dict) -> BitWardenEntry:
        data: dict = entry.__dict__.get("data")
        folder = self.get_folder_name(entry.__dict__.get("folderId"))
        return BitWardenEntry(
            name=data.get("name"),
            username=data.get("username"),
            password=data.get("password"),
            uri=data.get("uri"),
            notes=data.get("notes"),
            totp=data.get("totp"),
            folder=folder,
        )

    def get_entries(self) -> list[BitWardenEntry]:
        cyphers = self.client.get_ciphers()
        entries = list(map(self._map, cyphers.get("id").values()))
        return entries

    def get_folder_name(self, folder_id: str) -> str:
        if self.folder_cache.get(folder_id) is not None:
            return self.folder_cache.get(folder_id)
        token = self.client.get_token(token=None)

        response = self.client.r(f"/api/folders/{folder_id}", method="get", token=token)
        # self.client.assert_bw_response(response)
        if response.status_code in [400, 499]:
            return folder_id

        body = response.json()
        folder = self.client.decrypt(body, key=token.get("user_key"))
        folder_name = folder.get("Name")
        self.folder_cache[folder_id] = folder_name
        return folder_name
