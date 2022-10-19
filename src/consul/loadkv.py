import requests
import json
import base64

endpoint = input("Enter the Consul endpoint (eg. https://vault.example.com:8200): ")
token = input("Enter the Consul token: ")
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

    dbytes = base64.decodebytes(value.encode("ascii"))

    requests.put(f"{endpoint}/v1/kv{key}", headers={
        'X-Consul-Token': token
        }, data=dbytes, verify=False).json()
