import urllib3
import json
import requests
from requests.auth import HTTPBasicAuth
import datetime
import time

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

### Set the time range (start time & end time). This is needed for Tx Power, & Rogue, APIs

epochStart = (datetime.datetime(2023, 3, 17, 11, 0, 0).timestamp())*1000 #format: Y,M,D  H,M,S
epochEnd = (datetime.datetime(2023, 3, 23, 11, 1, 0).timestamp())*1000 #format: Y,M,D  H,M,S
epochStart = int(epochStart)
epochEnd = int(epochEnd)



#####################################################################################################




url = f'https://{DNAC_IP}/api/assurance/v1/network-device?fields=location,deviceHealth&startTime={epochStart}&endTime={epochEnd}&limit=100&offset=1&sortBy=managementIpAddress&order=asc'

payload = '''{"filters":{},"role":"UNIFIED AP"}'''
headers = {"x-auth-token": token, 'content-type': 'application/json'}
response = requests.request("POST", url, headers=headers, data = payload, verify=False)


for i in response.json()['response']:

    print(i['name'])
    print(i['clCount'])
    print('\n')


#print(json.dumps(response.json(), indent = 4))

