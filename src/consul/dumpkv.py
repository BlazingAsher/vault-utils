import requests
import json

endpoint = input("Enter the Consul endpoint (eg. https://consul.example.com:8501): ")
token = input("Enter the Consul token: ")
prefix = input("Enter the prefix to dump (use / for all): ")

destination = input("Enter the export destination: ")

requests.packages.urllib3.disable_warnings() 

export = {}

values = requests.get(f"{endpoint}/v1/kv{prefix}", params={
    'recurse': True
    }, headers={
        'X-Consul-Token': token
        }, verify=False).json()

for value in values:
    export[prefix+value["Key"]] = value["Value"]

with open(destination, "w") as f:
    json.dump(export, f)
