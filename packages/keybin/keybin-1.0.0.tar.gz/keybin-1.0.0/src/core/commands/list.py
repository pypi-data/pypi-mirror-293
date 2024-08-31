import json
import requests
def list(access_token,_folder=None,_tags=None,_name=None,_created_at=None,_size=None,_order=None,_order_by=None,_last=None,_include_secrets=None):
    url = "https://vault.aws.us.pangea.cloud/v1/list"

    # Initialize the payload dictionary
    payload = {}
    if(_folder is not None):
        payload["filter"] = {"folder":_folder}
    if(_tags is not None):
        payload["filter"] = {"tags":_tags}
    if(_name is not None):
        payload["filter"] = {"name__contains":_name}
    if(_created_at is not None):
        payload["filter"] = {"created_at__gt":_created_at}  
    if(_size is not None):
        payload["size"] = _size
    if(_order is not None):
        payload["order"] = _order
    if(_order_by is not None):
        payload["order_by"] = _order_by
    if(_last is not None):
        payload["last"] = _last 
    if(_include_secrets is not None):
        payload["include_secrets"] = _include_secrets
    
    payload = json.dumps(payload)
    
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST",url,headers=headers,data=payload)
    return(response.text)

# {
#     "request_id": "prq_bvmgelzt535dyt6fthejfsjakn6hfzvm",
#     "request_time": "2024-08-30T15:46:33.496814Z",
#     "response_time": "2024-08-30T15:46:33.499626Z",
#     "status": "Unauthorized",
#     "summary": "Not authorized to access this resource",
#     "result": null
# }