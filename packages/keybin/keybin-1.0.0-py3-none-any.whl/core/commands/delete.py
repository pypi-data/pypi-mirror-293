import requests
import json

def delete(_id,access_token):
    url="https://vault.aws.us.pangea.cloud/v1/delete"
    payload= json.dumps({
        "id":_id
        })
    headers = {
        'Authorization':f"Bearer {access_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST",url,headers=headers,data=payload)
    print(response.text)
    return(response.text)


