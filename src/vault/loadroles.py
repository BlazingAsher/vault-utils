import requests
import json

endpoint = input("Enter the Vault endpoint (eg. https://vault.example.com:8200): ")
token = input("Enter the Vault token: ")
auth_name = input("Enter the name of the Kubernetes auth method: ")

source = input("Enter the import source file: ")

requests.packages.urllib3.disable_warnings() 

sdata = None

with open(source, "r") as f:
    sdata = json.load(f)

print("Loaded the following roles: ")
for role in sdata:
    roleName = role["name"]
    print(f"  - {roleName}")

ctn = input("Continue with the import (y/n)?\nWARNING: EXISTING DATA WILL THE OVERWRITTEN!\n")

if ctn.lower() == "y":
    nkeys = len(sdata)
    print(f"Beginning import of {nkeys} roles.")

for role in sdata:
    roleName = role["name"]
    del role["name"]
    requests.post(f"{endpoint}/v1/auth/{auth_name}/role/{roleName}", headers={
        'X-Vault-Token': token
        }, json=role, verify=False).text

print("Finished.")
