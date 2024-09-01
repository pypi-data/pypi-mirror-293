import requests
import json
import os


def get(_id,access_token):
    url="https://vault.aws.us.pangea.cloud/v1/get"
    payload= json.dumps({
        "id":_id,
        "version":"1",
        "version_state":"active",
        "verbose":True
        })
    headers = {
        'Authorization':f"Bearer {access_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST",url,headers=headers,data=payload)
    return(response.text)

