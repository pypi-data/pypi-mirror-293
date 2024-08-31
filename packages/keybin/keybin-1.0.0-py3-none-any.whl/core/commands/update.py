import requests
import json

def update(_id,access_token,name=None,_folder=None,_metadata=None,_tags=None):
    url="https://vault.aws.us.pangea.cloud/v1/update"
    payload= {
        "id":_id
        }
    
    if(name is not None):
        payload["name"] = name
    if(_folder is not None):
        payload["folder"] = _folder
    if(_metadata is not None):
        payload["metadata"] = _metadata
    if(_tags is not None):
        payload["tags"] = _tags
    payload =json.dumps(payload)

    headers = {
        'Authorization':f"Bearer {access_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST",url,headers=headers,data=payload)
    return response.text
