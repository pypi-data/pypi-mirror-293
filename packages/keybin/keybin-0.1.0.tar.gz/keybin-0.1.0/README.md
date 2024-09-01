
# KeyBin

`keybin` is a command-line interface tool built with python for secure management of API and secret keys using the Panega Vault service.



## Initial Setup

Before using keybin, you need to perform the initial setup to configure your Panega Vault API token.

### Get Panega Vault API Token:

- Go to [Panega Vault](https://console.pangea.cloud/service/vault).
- Obtain your API token from the dashboard.

### MongoDb Token:
- Get you `MongoDb` URL 
- Add it in the `.env` file with the name of `URL`
## Installation

Install my-project with npm

```bash
pip install keybin
```
    
## Features

- 🔐 Secure Secret Management: Store, retrieve, update, and delete secrets securely.
- 🛠️ Flexible Metadata: Add and update metadata in key-value pairs.
- 🏷️ Tag Management: Categorize secrets with tags for easy retrieval and management


## General Guide

### Initinializing your API key

Use `init` command to intialize your API key

### Guide to Update and Delete
- Get the id of your secret which you want to update or delete from 'getid' command
- Now use to id with `commands`
## Usage

### Getting Help
```bash
keybin --help [COMMAND]
```
Repale `[COMMAND]` with the command you need help with 

### Adding a Secret

Add a secret to the vault

```bash
keybin store <SECRET_VALUE> [-n <SECRET_NAME>] [-k <KEY_TYPE>] [-f <FOLDER>] [-m <METADATA>] [-t <TAGS>]
```
* Arguments
    - `value`: The secret value to store.
    - -n, --name: A unique name to identify the secret.
    - -k, --key_type: The type of the key (default is 'secret').
    - -f, --folder: The folder where the secret will be stored.
    - -m, --metadata: Additional metadata for the secret in the  format key:value (e.g., [name:abc,product:xcompany]).
    - -t, --tags: Tags to categorize the secret, separated by commas (e.g., [tags1,tags2]).

 ### Listing the Secrets
 ```bash
 keybin list [-f <FOLDER>] [-t <TAGS>] [-n <NAME_CONTAINS>] [-c <CREATED_AT>] [-s <SIZE>] [-o <ORDER>] [-ob <ORDER_BY>] [-l <LAST>] [-i <INCLUDE_SECRETS>]
```
* Arguments
    - -f, --folder: The folder containing the secrets.
    - -t, --tags: Tags to filter the secrets by, separated by commas (e.g., [tags1,tags2]).
    - -n, --name_contains: Filter by secrets whose names contain this value.
    - -c, --created_at: Filter by secrets created after this date (ISO format).
    - -s, --size: Maximum number of items to return (default is 50).
    - -o, --order: Order of results (asc or desc).
    - -ob, --order_by: Property to order the results by (e.g., created_at, name).
    - -l, --last: ID of the last item from a previous query, for pagination.
    - -i, --include_secrets: Whether to include the secret values in the results (true or false).

### Getting Id of a secret
```bash
keybin getid --name <SECRET_NAME>
```

* Arguments
    - `--name`: The name of the secret you want to retrieve
### Updating Secret
```bash
keybin update <ID> [-n <NAME>] [-f <FOLDER>] [-m <METADATA>] [-t <TAGS>]
```
* Arguments
    - `id`: The ID of the secret to update.
    - -n, --name: New name for the secret.
    - -f, --folder: New folder to move the secret to.
    - -m, --metadata: New metadata for the secret in the format  key:value (e.g., [name:abc,product:xcompany]).
    - -t, --tags: New tags to assign to the secret, separated by commas (e.g., [tags1,tags2]).

### Deleting Secret
```bash
keybin delete <ID>
```
* Arguments
    - `id`: The ID of the secret to delete.