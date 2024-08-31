import requests
import json

def store(secret,access_token, _type=None, _name = None, _folder = None, _metadata = None,_tags=None) :
    url = "https://vault.aws.us.pangea.cloud/v1/secret/store"
    payload = {
        "secret": secret
    }
    if(_type is not None):
        payload["type"] = _type
    
    if(_name is not None):
        payload["name"] = _name
    if(_folder is not None):
        payload["folder"] = _folder
    if(_metadata is not None):
        payload["metadata"] = _metadata
    if(_tags is not None):
        payload["tags"] = _tags
        
       

    payload=json.dumps(payload)


    headers = {
        'Authorization':f"Bearer {access_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response=requests.request("POST",url,headers=headers,data=payload)
    return(response.text)



# json_data={
#     "request_id": "prq_bw2s6gdsugc3n6avaluhkryk75itohwj",
#     "request_time": "2024-08-30T15:04:01.566477Z",
#     "response_time": "2024-08-30T15:04:01.670786Z",
#     "status": "ValidationError",
#     "summary": "There was 1 error(s) in the given payload: An item with the same name exists in this folder.",
#     "result": {
#         "errors": [
#             {
#                 "code": "ItemNotUnique",
#                 "detail": "An item with the same name exists in this folder.",
#                 "source": "/name"
#             }
#         ]
#     }
# }
# print(json_data["result"]["errors"][0]['detail'])