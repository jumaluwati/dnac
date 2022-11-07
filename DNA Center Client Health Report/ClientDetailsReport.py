# Copyright (c) 2016-2022 Cisco and/or its affiliates
# by/ jalluwat@cisco.com
# for detailed explanation, please refer to the documentation 
#
# this code generates a client detail report on dna center USING DNACENTERSDK librbary
#
#Please downlaod first the SDK by typing down on your terminal/powershell : pip install dnacentersdk



import urllib3
from dnacentersdk import DNACenterAPI
import json

urllib3.disable_warnings()

dnac = DNACenterAPI(username = '', #add dnac username
                    password = '', #add dnac password
                    base_url = 'https://{DNAC URL}:443', #add dnac url
                    version = '2.2.3.3',
                    verify = False)


#REPORT CREATION

deliveries = [

{
         "type":"NOTIFICATION",
         "subscriptionId":"None",
         "notificationEndpoints":[
            {
               "type":"EMAIL",
               "emailAddresses":[
                  "test@cisco.com"
               ],
               "emailSubscriptionEndpointId":"None",
               "emailSubscriptionEndpointInstanceId":"None"
            }
         ],
         "emailAttach":True
         #"default":false
      }

]

#API Parameters (fill in: 1- unique name, 2- when to schedule (default value is SCHEDULE NOW))

name = "ADD A UNIQUE NAME"

schedule = {"type":"SCHEDULE_NOW"}

tags = []

view = {
        "name":"Client Detail",
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
                  "name":"ipv6",
                  "displayName":"IPv6 Address"
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
                  "name":"averageHealthScore_min",
                  "displayName":"Min Health Score"
               },
               {
                  "name":"averageHealthScore_max",
                  "displayName":"Max Health Score"
               },
               {
                  "name":"averageHealthScore_median",
                  "displayName":"Median Health Score"
               },
               {
                  "name":"usage_sum",
                  "displayName":"Usage (MB)"
               },
               {
                  "name":"connectedDeviceName",
                  "displayName":"Connected Device Name"
               },
               {
                  "name":"frequency",
                  "displayName":"Band"
               },
               {
                  "name":"rssi_median",
                  "displayName":"RSSI (dBm)"
               },
               {
                  "name":"snr_median",
                  "displayName":"SNR (dB)"
               },
               {
                  "name":"site",
                  "displayName":"Last Location"
               },
               {
                  "name":"lastUpdated",
                  "displayName":"Last Seen"
               },
               {
                  "name":"apGroup",
                  "displayName":"AP Group"
               },
               {
                  "name":"ssid",
                  "displayName":"SSID"
               },
               {
                  "name":"vlan",
                  "displayName":"VLAN ID"
               },
               {
                  "name":"vnid",
                  "displayName":"VNID"
               },
               {
                  "name":"onboardingEventTime",
                  "displayName":"Onboarding Time"
               },
               {
                  "name":"assocDoneTimestamp",
                  "displayName":"Association Time"
               },
               {
                  "name":"authDoneTimestamp",
                  "displayName":"Authentication Time"
               },
               {
                  "name":"aaaServerIp",
                  "displayName":"Authentication Server"
               },
               {
                  "name":"dhcpDoneTimestamp",
                  "displayName":"Last DHCP Request"
               },
               {
                  "name":"maxDhcpDuration_max",
                  "displayName":"DHCP Response Time (ms)"
               },
               {
                  "name":"dhcpServerIp",
                  "displayName":"DHCP Server"
               },
               {
                  "name":"linkSpeed",
                  "displayName":"Link Speed (Mbps)"
               },
               {
                  "name":"txRate_min",
                  "displayName":"Min Tx Rate (bps)"
               },
               {
                  "name":"txRate_max",
                  "displayName":"Max Tx Rate (bps)"
               },
               {
                  "name":"txRate_avg",
                  "displayName":"Average Tx Rate (bps)"
               },
               {
                  "name":"rxRate_min",
                  "displayName":"Min Rx Rate (bps)"
               },
               {
                  "name":"rxRate_max",
                  "displayName":"Max Rx Rate (bps)"
               },
               {
                  "name":"rxRate_avg",
                  "displayName":"Average Rx Rate (bps)"
               },
               {
                  "name":"txBytes_sum",
                  "displayName":"Tx (MB)"
               },
               {
                  "name":"rxBytes_sum",
                  "displayName":"Rx (MB)"
               },
               {
                  "name":"dataRate_median",
                  "displayName":"Data Rate (Mbps)"
               },
               {
                  "name":"dot11Protocol",
                  "displayName":"Client Protocol"
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
                "type":"SINGLE_SELECT_ARRAY",
                "name":"DeviceType",
                "displayName":"Device Type",
                "value":[
                    {
                        "value":"Wireless",
                        "displayValue":"Wireless"
                    }
                ]
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
            },
            {
                "type":"MULTI_SELECT",
                "name":"SSID",
                "displayName":"SSID",
                "value":[{

                        "value":"", #add ssid name
                        "displayValue":"" #add ssid name
                    }
                ]
            }
        ],
        "format":{
            "name":"JSON",
            "formatType":"JSON"
            
        },
        "viewInfo":None,
        "viewId":"e8e66b17-4aeb-4857-af81-f472023bb05e"
    }


   
viewGroupId = "d7afe5c9-4941-4251-8bf5-0fb643e90847"

viewGroupVersion = "2.0.0"

headers = {'headers': {}}

payload = {}

active_validation = False


#The API call

data = dnac.reports.create_or_schedule_a_report(deliveries=deliveries, name=name, schedule=schedule, tags=tags, view=view, viewGroupId=viewGroupId, viewGroupVersion=viewGroupVersion, headers=headers, payload=payload, active_validation=active_validation)
