import requests
import queue
import json

endpoint = input("Enter the vault endpoint (eg. https://vault.example.com:8200): ")
token = input("Enter the Vault token: ")
kvengine = input("Enter the name of the KV engine: ")
prefix = input("Enter the prefix to dump (use / for all): ")

destination = input("Enter the export destination: ")

requests.packages.urllib3.disable_warnings() 

export = {}

q = queue.Queue()
q.put(prefix)

all_keys = set()

while not q.empty():
    path = q.get()
    
    tree = requests.request("LIST", f"{endpoint}/v1/{kvengine}/metadata{path}", headers={
        'X-Vault-Token': token
        }, verify=False).json()

    subkeys = tree["data"]["keys"]
    for key in subkeys:
        if key.endswith("/"): # this is a folder
            q.put(path + key)
        else:
            all_keys.add(path + key)

for key in all_keys:
    tree = requests.get(f"{endpoint}/v1/{kvengine}/data{key}", headers={
        'X-Vault-Token': token
        }, verify=False).json()
    export[key] = tree["data"]["data"]

with open(destination, "w") as f:
    json.dump(export, f)

print(f"Sucessfully exported data to {destination}.")
