from dataclasses import dataclass

from pykeepass import create_database
from pykeepass.group import Group


@dataclass
class KeePassEntry:
    title: str = None
    username: str = None
    password: str = None
    url: str = None
    group: str = None
    notes: str = None
    tags: str = None
    otp: str = None


class KeePassClient:

    def __init__(self, file: str, password: str):
        self.client = create_database(file, password)

    def get_or_create_group(self, group_name: str) -> Group:
        if group_name is None:
            return self.client.root_group

        groups = self.client.find_groups_by_name(group_name=group_name)
        if groups is None or len(groups) == 0:
            return self.client.add_group(destination_group=self.client.root_group, group_name=group_name)
        return groups[0]

    def add_entry(self, entry: KeePassEntry):
        if entry.username is None or entry.title is None or entry.password is None:
            return

        self.client.add_entry(
            destination_group=self.get_or_create_group(entry.group),
            password=entry.password,
            username=entry.username,
            notes=entry.notes,
            title=entry.title,
            otp=entry.otp,
            url=entry.url,
            tags=entry.tags,

        )

    def save(self):
        self.client.save()