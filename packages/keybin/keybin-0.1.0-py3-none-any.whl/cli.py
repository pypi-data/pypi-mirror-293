from core.db import insert_secret, get_secret_id, get_vault_key, set_vault_key,delete_secret,update_secret
from core.commands import get, delete, store, update, list
import os
import pyperclip
import json


def init(secret_key):
    try:
        set_vault_key(secret_key)
    except:
        print("err: error in setting key")
    result =get_vault_key()
    if result is not None:
        print("Token: ", result)
        os.environ["VAULT_ACCESS_TOKEN"] = result  # type: ignore
        print("Vault key set as env variable")


def getId(_get_id):
    result =  get_secret_id(_get_id)
    if result is not None:
        pyperclip.copy(result)
        pyperclip.paste()
        print("Secret ID: ", result)
        print("Secret ID is copied to clipboard")
    else:
        print("err:err Secret ID not found")


def Get(_get):
    access_token = get_vault_key()

    if access_token is None:
        print("Vault key not set. Please set the vault key using the init command")
        return
 
    try:
        id = get_secret_id(_get)
        try:
            result = get.get(id,access_token)
            secret = json.loads(result)["result"]["current_version"]["secret"]
            pyperclip.copy(secret)
            pyperclip.paste()
            print("Secret is copied to clipboard")
        except:
            print("status:",json.loads(result)["status"]," summary:",json.loads(result)["summary"])
    except:
        print("err:No such secret found with this name please enter the correct name of the secret")


def Store(_store):
    access_token = get_vault_key()
    if access_token is None:
        print("Vault key not set. Please set the vault key using the init command")
        return
    secret = _store["value"]
    key_type = _store.get("key_type","secret")
    name = _store.get("name",None)
    folder = _store.get("folder",None)
    metadata = _store.get("metadata",None)
    tags = _store.get("tags",None)
    try:
        result =store.store(secret,access_token, key_type, name, folder, metadata,tags)
        try:
            insert_secret(
                secret_name=name, secret_id=json.loads(result)["result"]["id"]
            )
            # print(result)
        except:
            print("err:could insert the secret_id in the local storage. Please check all information which you have entered")
    except:
        print("err:",json.loads(result)["result"]["errors"][0]['detail'])



def List(_list):
    access_token = get_vault_key()
    if access_token is None:
        print("Vault key not set. Please set the vault key using the init command")
        return
    folder = _list.get("folder",None)
    tags = _list.get("tags",None)
    name_contains = _list.get("name_contains",None)
    created_at = _list.get("created_at",None)
    size = _list.get("size",None)
    order = _list.get("order",None)
    order_by = _list.get("order_by",None)
    last = _list.get("last",None)
    include_secrets = _list.get("include_secrets",None) #verified 

    try:
        result = list.list(
            access_token,
            folder,
            tags,
            name_contains,
            created_at,
            size,
            order,
            order_by,
            last,
            include_secrets,
        )
        items = json.loads(result)["result"]["items"]
        for item in items:
            name = item.get("name",'-')
            id = item.get("id","-")
            key_type = item.get("type","-")
            created = item.get("created_at","-")
            state = item.get("current_version",{}).get("state","-")
            print(
                f"Name:{name} \nSecret ID:{id} \nType:{key_type} \nCreated:{created} \nState:{state}\n"
            )
            print(
                "--------------------------------------------------------------------------------------------------------------------"
            )
    except:
        print("Status :", json.loads(result)["status"])
        print("Summary :", json.loads(result)["summary"])



def Update(_update):
    access_token = get_vault_key()
    if access_token is None:
        print("Vault key not set. Please set the vault key using the init command")
        return
    id = _update["id"]
    name=_update.get("name",None)
    folder=_update.get("folder",None)
    metadata = _update.get("metadata",None)
    tags = _update.get("tags",None)


    result = update.update(id,access_token,name, folder, metadata, tags)
    try:
        update_secret(id,name)
    except:
        print("err while updating the secret in local storage")
    print("Status :", json.loads(result)["status"])
    print("Summary :", json.loads(result)["summary"])
    


def Delete(_delete):
    access_token = get_vault_key()
    if access_token is None:
        print("Vault key not set. Please set the vault key using the init command")
        return
    id = _delete["secret_id"]
    result = delete.delete(id,access_token)
    if(json.loads(result)["status"]=='Success'):
        delete_secret(id)
    print("Status :", json.loads(result)["status"])
    print("Summary :", json.loads(result)["summary"])


