import argparse
from cli import init, getId, Get, Store, Update, Delete, List
def main():


    parser = argparse.ArgumentParser(
        description="A command-line interface for managing secrets in a secure vault."
    )

    subparsers = parser.add_subparsers(
        title="commands", dest="command", help="Available commands"
)
# init
    init_parser = subparsers.add_parser(
    "init", help="Initialize the CLI with the API key for Pangea."
)
    init_parser.add_argument("key", help="The API token obtained from the Pangea website.")
# getid
    getid_parser = subparsers.add_parser(
    "getid", help="Retrieve the ID of a secret by its name."
)
    getid_parser.add_argument(
    "--name", required=True, help="The name of the secret for which to retrieve the ID."
)


# get
    get_parser = subparsers.add_parser("get", help="Retrieve a stored secret by its name.")
    get_parser.add_argument(
    "--name",
    help="The name of the secret you want to retrieve. Required.",
    required=True,
)

# store
    store_parser = subparsers.add_parser("store", help="Store a new secret in the vault.")
    store_parser.add_argument("value", help="The secret value to store.")
    store_parser.add_argument("-n", "--name", help="A unique name to identify the secret.")
    store_parser.add_argument(
    "-k",
    "--key_type",
    help="The type of the key (default is 'secret').",
    default="secret",
)
    store_parser.add_argument(
    "-f", "--folder", help="The folder where the secret will be stored."
)
    store_parser.add_argument(
    "-m",
    "--metadata",
    help="Additional metadata for the secret in the format 'key:value'.(format=>[key1:data,key2:data]) (eg:[name:abc,product:xcompany]))",
    type=meta_type,
)
    store_parser.add_argument(
    "-t",
    "--tags",
    help="Tags to categorize the secret, separated by commas.(format=>[tags1,tags2])",
    type=arr_type,
)

# list
    list_parser = subparsers.add_parser(
    "list", help="List all secrets in the specified directory."
)
    list_parser.add_argument("-f", "--folder", help="The folder containing the secrets.")
    list_parser.add_argument(
    "-t",
    "--tags",
    help="Tags to filter the secrets by, separated by commas.(format=>[tags1,tags2])",
    type=arr_type,
)
    list_parser.add_argument(
    "-n", "--name_contains", help="Filter by secrets whose names contain this value."
)
    list_parser.add_argument(
    "-c", "--created_at", help="Filter by secrets created after this date (ISO format)."
)
    list_parser.add_argument(
    "-s",
    "--size",
    help="Maximum number of items to return (default is 50).",
    default=50,
)
    list_parser.add_argument(
    "-o",
    "--order",
    help="Order of results (ascending or descending).",
    choices=["asc", "desc"],
)
    list_parser.add_argument(
    "-ob",
    "--order_by",
    help="Property to order the results by (e.g., 'created_at', 'name').",
    choices=["created_at", "name", "id", "folder"],
)
    list_parser.add_argument(
    "-l", "--last", help="ID of the last item from a previous query, for pagination."
)
    list_parser.add_argument(
    "-i",
    "--include_secrets",
    help="Whether to include the secret values in the results.",
    type=bool,
    choices=[True, False],
    default=False,
)

# update
    update_parser = subparsers.add_parser(
    "update", help="Update an existing secret by its ID."
)
    update_parser.add_argument("id", help="The ID of the secret to update.")
    update_parser.add_argument("-n", "--name", help="New name for the secret.")
    update_parser.add_argument("-f", "--folder", help="New folder to move the secret to.")
    update_parser.add_argument(
    "-m",
    "--metadata",
    help="New metadata for the secret in the format 'key:value'.(format=>[key1:data,key2:data]) (eg:[name:abc,product:xcompany]))",
    type=meta_type,
)
    update_parser.add_argument(
    "-t",
    "--tags",
    help="New tags to assign to the secret, separated by commas.",
    type=arr_type,
)

# delete
    delete_parser = subparsers.add_parser("delete", help="Delete a secret by its ID.")
    delete_parser.add_argument("id", help="The ID of the secret to delete.")

# args = parser.parse_args()


    args = parser.parse_args()

# init
    if args.command == "init":
        init(args.key)

# getid

    if args.command == "getid":
        getId(args.name)

# get

    if args.command == "get":
        Get(args.name)

# store
    if args.command == "store":
        Store(
        {
            "value": args.value,
            "key_type": args.key_type,
            "name": args.name,
            "folder": args.folder,
            "metadata": args.metadata,
            "tags": args.tags,
        }
    )

# list
    if args.command == "list":
        List(
        {
            "folder": args.folder,
            "tags": args.tags,
            "name_contains": args.name_contains,
            "size": args.size,
            "order": args.order,
            "order_by": args.order_by,
            "last": args.last,
            "include_secrets": args.include_secrets,
        }
    )

# update
    if args.command == "update":
        Update(
        {
            "id": args.id,
            "name": args.name,
            "folder": args.folder,
            "metadata": args.metadata,
            "tags": args.tags,
        }
    )

# delete
    if args.command == "delete":
        Delete({"secret_id": args.id})



def arr_type(string):
    return [element.strip() for element in string.strip("[]").split(",")]


def meta_type(meta):

    meta_pairs = meta.strip("[]").split(",")
    meta_dict = {}

    for pair in meta_pairs:
        key, value = pair.split(":")
        meta_dict[key.strip()] = value.strip()

    return meta_dict

if __name__ == '__main__':
    main()