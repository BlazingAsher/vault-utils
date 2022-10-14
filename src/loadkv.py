import requests
import queue
import json

endpoint = input("Enter the Vault endpoint (eg. https://vault.example.com:8200): ")
token = input("Enter the Vault token: ")
kvengine = input("Enter the name of the KV engine: ")
prefix = input("Enter the prefix to load (use / for none): ")

source = input("Enter the import source file: ")

requests.packages.urllib3.disable_warnings() 

sdata = None

with open(source, "r") as f:
    sdata = json.load(f)

print("Loaded the following keys: ")
for key in sdata:
    print(f"  - {key}")

ctn = input("Continue with the import (y/n)?\nWARNING: EXISTING DATA WILL THE OVERWRITTEN!\n")

if ctn.lower() == "y":
    nkeys = len(sdata.keys())
    print(f"Beginning import of {nkeys} keys.")
    

for key in sdata:
    value = sdata[key]

    requests.post(f"{endpoint}/v1/{kvengine}/data{key}", headers={
        'X-Vault-Token': token
        }, json={
            'data': value
            }, verify=False).json()
print("Finished.")
