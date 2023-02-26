import os

from bitwarden_client import BitWardenClient, BitWardenEntry
from keepass_client import KeePassClient, KeePassEntry


bitwarden_url = os.getenv('BITWARDEN_URL')
bitwarden_email = os.getenv('BITWARDEN_EMAIL')
bitwarden_password = os.getenv('BITWARDEN_PASSWORD')
keepass_password = os.getenv('KEEPASS_PASSWORD')
keepass_file = os.getenv('KEEPASS_FILE') or 'backup.kdbx'

if bitwarden_password is None or bitwarden_email is None or bitwarden_url is None or keepass_password is None:
    print("BITWARDEN_URL or BITWARDEN_EMAIL or BITWARDEN_PASSWORD or KEEPASS_PASSWORD is None")
    exit(1)


def _map(entry: BitWardenEntry) -> KeePassEntry:
    return KeePassEntry(
        title=entry.name,
        username=entry.username,
        password=entry.password,
        url=entry.uri,
        notes=entry.notes,
        otp=entry.totp,
        group=entry.folder,
    )


def backup():
    bitwarden = BitWardenClient(bitwarden_url, bitwarden_email, bitwarden_password)
    keepass = KeePassClient(keepass_file, keepass_password)

    entries = bitwarden.get_entries()
    for entry in entries:
        mapped = _map(entry)
        keepass.add_entry(mapped)

    keepass.save()


backup()
