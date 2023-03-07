# Copyright (c) 2016-2023 Cisco and/or its affiliates
#
# by/ jalluwat@cisco.com
#
# This is an API call that maps Cisco DNA Center clients to the Access Points the clients are connected to


import urllib3
import json
import time
import requests
from requests.auth import HTTPBasicAuth
import datetime

urllib3.disable_warnings()

#credentials
DNAC_IP = ''
USERNAME = ''
PASSWORD = ''


#getting the token:
tokenurl = f"https://{DNAC_IP}/dna/system/api/v1/auth/token"

response = requests.request(
    "POST",
    tokenurl,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    verify=False,
)

token = ""

tokenDict = response.json()
for key,value in tokenDict.items():
  token += value




### Set the time range (start time & end time). This is needed for the API call

epochStart = (datetime.datetime(2023, 3, 6, 11, 0, 0).timestamp())*1000 #format: Y,M,D  H,M,S
epochEnd = (datetime.datetime(2023, 3, 6, 11, 30, 0).timestamp())*1000 #format: Y,M,D  H,M,S
epochStart = int(epochStart)
epochEnd = int(epochEnd)

############################################################



url = f'https://{DNAC_IP}/api/assurance/v1/host'

payload = f'''{{
    "startTime":{epochStart},
    "endTime":{epochEnd},
    "limit":100,
    "offset":1,
    "filters":{{
        "devType":[
            "WIRELESS"
        ],
        "scoreType":[],
        "kpi":[],
        "typeIdList":[]
    }}
}}'''


clientToApMapping = []
clientToApMapping_zipped = []

headers = {"x-auth-token": token, 'content-type': 'application/json'}
response = requests.request("POST", url, headers=headers, data = payload, verify=False)

for i in response.json()['response']:

	clientToApMapping.append(i['clientConnection'])
	clientToApMapping.append(i['hostMac'])



data_pairs = zip(clientToApMapping[::2],clientToApMapping[1::2])
for i in data_pairs:
	clientToApMapping_zipped.append(i)


mydict = dict()

for line in clientToApMapping_zipped:
    if line[0] in mydict:
        # append the new number to the existing array at this slot
        mydict[line[0]].append(line[1])
    else:
        # create a new array in this slot
        mydict[line[0]] = [line[1]]
result = json.dumps(mydict, indent=4)

print(result)




