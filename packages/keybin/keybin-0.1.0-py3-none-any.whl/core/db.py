from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json
import os


try:
    # client = MongoClient("mongodb://192.168.206.158:27017/")#192.168.206.158
    client = MongoClient("mongodb://192.168.135.158:27017/")
    server_info = client.server_info()
    # print("Successfully connected to MongoDB", server_info["version"])
except PyMongoError as e:
    print("err:", e)

db = client["Pangea"]

# create collection of secrets
if db.get_collection("secrets") == None:
    db.create_collection("secrets")
    print("Collection created: secrets")

# create collection of keys
if db.get_collection("keys") == None:
    db.create_collection("keys")
    print("Collection created:a keys")

# funciton to insert secret (secret_id, secret_name)


def insert_secret(secret_id, secret_name):

    secrets =db.get_collection("secrets")
    secrets.insert_one({"secret_id": secret_id, "secret_name": secret_name})
    print_stamtment = json.dumps(
        {"secret_id": secret_id, "secret_name": secret_name}
    )
    print("Successfully inserted:")
    print(print_stamtment)

def delete_secret(secret_id):
    secrets = db.get_collection("secrets")
    secrets.delete_one({"secret_id":secret_id})



# function to get secret_id (secret_name)
def get_secret_id(secret_name):

    secrets = db.get_collection("secrets")
    secret = secrets.find_one({"secret_name": secret_name})
    if secret is not None:
        return secret["secret_id"]
    else:
        return TypeError


def update_secret(id,name):
        secrets=db.get_collection("secrets")
        filter = { 'secret_id': id }
        newvalues = { "$set": { 'secret_name': name } }
        secrets.update_one(filter,newvalues)

# function to set vault key (key_id)


def set_vault_key(key_id):

    keys = db.get_collection("keys")
    keys.insert_one({"key_id": key_id})





# function to get vault key
def get_vault_key() :
    keys = db.get_collection("keys")
    key = keys.find_one(sort=[("_id",-1)])
    if key is not None:
        return key['key_id']
    else:
        return key




