# bitwarden-to-keepass

This project backups all passwords from a bitwarden (compatible) server into a single KeePass (kdbx) file.

The required environment variables are:

```shell
export BITWARDEN_URL="foo"
export BITWARDEN_EMAIL="bar"
export BITWARDEN_PASSWORD="baz"
export KEEPASS_PASSWORD="123456"
export KEEPASS_FILE="backup.kdbx"
```

## Development

### venv

Create new virtual environment (venv):

```shell
python3 -m venv venv
```

Use venv:

```shell
source venv/bin/activate
```

### Dependencies

Install requirements:

```shell
pip install -r requirements.txt
```

Update current dependencies into `requirements.txt`:

```shell
pip freeze > requirements.txt
```