# Copyright (c) 2016-2022 Cisco and/or its affiliates
# by/ jalluwat@cisco.com
#
# this code generates a client detail report on dna center USING DNACENTERSDK librbary
#
#Please downlaod first the SDK by typing down on your terminal/powershell : pip install dnacentersdk
#
# checkout the SDK's guide @ https://dnacentersdk.readthedocs.io

import urllib3
from dnacentersdk import DNACenterAPI
import json
import time
import requests
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()

DNAC_IP = '10.147.26.90'
USERNAME = 'jalluwat'
PASSWORD = 'C1sco12345'

DNAC_AUTH = HTTPBasicAuth(USERNAME, PASSWORD)

dnac = DNACenterAPI(username = USERNAME,  #username
                    password = PASSWORD,  #password
                    base_url = f'https://{DNAC_IP}:443',
                    version = '2.2.3.3', #this is the version of the dnacentersdk library dnacentersdk.readthedocs.io
                    verify = False)

#token generation

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



#REPORT CREATION

deliveries = [

{
         "type":"NOTIFICATION",
         "subscriptionId":"None",
         "notificationEndpoints":[
            {
               "type":"EMAIL",
               "emailAddresses":[
                  "jalluwat@cisco.com"  #email address
               ],
               "emailSubscriptionEndpointId":"None",
               "emailSubscriptionEndpointInstanceId":"None"
            }
         ],
         "emailAttach":True
         #"default":false
      }

]

name = "November 9th Juma 4"  #Name of the report

schedule = {"type":"SCHEDULE_NOW"}

tags = []

view = {
        "name":"Client Detail",  #report type: Client details
        "description":"Client Details via APIs",
        "fieldGroups":[
            {
            "fieldGroupName":"client_details",
            "fieldGroupDisplayName":"Client Details",
            "fields":[
               {
                  "name":"hostName",
                  "displayName":"Host Name"
               },
               {
                  "name":"username",
                  "displayName":"User ID"
               },
               {
                  "name":"macAddress",
                  "displayName":"MAC Address"
               },
               {
                  "name":"ipv4",
                  "displayName":"IPv4 Address"
               },
               {
                  "name":"deviceType",
                  "displayName":"Device Type"
               },
               {
                  "name":"connectionStatus",
                  "displayName":"Current Status"
               },
               {
                  "name":"connectedDeviceName",
                  "displayName":"Connected Device Name"
               }
            ]
         }
        ],
        "filters":[


            {
                "value": {"timeRangeOption":"LAST_3_HOURS"},
                "displayName": "Time Range",
                "name": "TimeRange",
                "type": "TIME_RANGE"
            },

            {
                "type":"MULTI_SELECT",
                "name":"Band",
                "displayName":"Band",
                "value":[
                    {
                        "value":"2.4",
                        "displayValue":"2.4"
                    },
                    {
                        "value":"5",
                        "displayValue":"5"
                    }
                ]
            },
            {
                "type":"MULTI_SELECT_TREE",
                "name":"Location",
                "displayName":"Location",
                "value":[
                    {
                        "value":"sample-global-site-id",
                        "displayValue":"Global"
                    }
                ]
            }
        ],
        "format":{
            "name":"JSON",
            "formatType":"JSON",
            #"default":true
        },
        "viewInfo":None,
        "viewId":"e8e66b17-4aeb-4857-af81-f472023bb05e"
    }


   
viewGroupId = "d7afe5c9-4941-4251-8bf5-0fb643e90847"

viewGroupVersion = "2.0.0"

headers = {'headers': {}}

payload = {'dataCategory': 'Client'}

active_validation = False


data = dnac.reports.create_or_schedule_a_report(deliveries=deliveries, name=name, schedule=schedule, tags=tags, view=view, viewGroupId=viewGroupId, viewGroupVersion=viewGroupVersion, headers=headers, payload=payload, active_validation=active_validation)

######## REPORT TAKES AROUND 180 SECONDS TO GENERATE #############



time.sleep(180)



reportNum = data.reportId
excutionData = dnac.reports.get_all_execution_details_for_a_given_report(report_id =reportNum)


executionNum = excutionData["executions"][0]["executionId"]


url = f"https://{DNAC_IP}/api/dnacaap/v1/daas/core/content/data-set/{reportNum}/{executionNum}"

headers = {"x-auth-token": token}
response = requests.request("GET", url, headers=headers, verify=False)

scoreslist=[]
scoresum = 0


data = json.dumps(response.json(), indent=4)
dataPy = json.loads(data)

count = 0

for details in dataPy["client_details"]:
  hostname = details["hostName"]
  username = details["username"]
  macAddress = details["macAddress"]
  ipAddress = details["ipv4"]
  deviceType = details["deviceType"]
  connectionStatus = details["connectionStatus"]
  connectedDeviceName = details["connectedDeviceName"]
  count += 1

  print(f'{count}:')
  print('\n')
  print(f'Hostname: {hostname}')
  print(f'Username: {username}')
  print(f'MAC Address: {macAddress}')
  print(f'IPv4 Address: {ipAddress}')
  print(f'Device Type: {deviceType}')
  print(f'Connection Status: {connectionStatus}')
  print(f'Connected Device: {connectedDeviceName}')
  print('---------------------------')
  print('\n')



