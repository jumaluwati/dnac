import datetime
import logging
import os
import time
import urllib3
import json
import requests

from datetime import datetime
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings



DNAC_URL = "https://10.147.26.90" #ADD YOUR DNAC URL
DNAC_USER = "USERNAME"
DNAC_PASS = "PASSWORD"

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings


DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

REPORT_CATEGORY = 'Client'
VIEW_NAME = 'Client Detail'
REPORT_NAME = 'Client Report Detail Token Testing 3.0'


def pprint(json_data):
    """
    Pretty print JSON formatted data
   :param json_data: data to pretty print
   :return None
    """
    print(json.dumps(json_data, indent=4, separators=(', ', ': ')))


tokenurl = "https://10.147.26.90:443/dna/system/api/v1/auth/token" #CHANGE THE TOKEN URL
response = requests.request ( 
    "POST", 
    tokenurl, 
    auth = DNAC_AUTH,
    verify = False 
) 

token = "" #TOKEN PLACEHOLDER 
tokenDict = response.json() 
for key,value in tokenDict.items(): 
    token += value


def get_report_view_groups(dnac_auth):
    """
    This function will return the report view groups
   :param dnac_auth: Cisco DNA Center Auth
   :return: report view groups
    """
    url = DNAC_URL + '/dna/intent/api/v1/data/view-groups'
    header = {'Content-Type': 'application/json', 'X-Auth-Token': dnac_auth}
    response = requests.get(url, headers=header, verify=False)
    report_view_groups = response.json()
    return report_view_groups


def get_report_view_ids(view_group_id, dnac_auth):
    """
    This function will get return the views for the groups id {view_group_id}
   :param view_group_id: report view group id
   :param dnac_auth: Cisco DNA Center Auth
   :return: the report view ids
    """
    url = DNAC_URL + '/dna/intent/api/v1/data/view-groups/' + view_group_id
    header = {'Content-Type': 'application/json', 'X-Auth-Token': dnac_auth}
    response = requests.get(url, headers=header, verify=False)
    report_view_ids = response.json()
    return report_view_ids


def get_detailed_report_views(view_id, group_id, dnac_auth):
    """
    This function will retrieve the view details for the view group id {group_id} and the view id {view_id}
   :param view_id: report view id
   :param group_id: report group id
   :param dnac_auth: Cisco DNA Center Auth
   :return: the report report view details
    """
    url = DNAC_URL + '/dna/intent/api/v1/data/view-groups/' + group_id + '/views/' + view_id
    header = {'Content-Type': 'application/json', 'X-Auth-Token': dnac_auth}
    response = requests.get(url, headers=header, verify=False)
    report_detailed_views = response.json()
    return report_detailed_views


def create_report(payload, dnac_auth):
    """
    This function will create a new Client Detail report
   :param payload: request payload
   :param dnac_auth: Cisco DNA Center Auth
   :return: return the API response
    """
    url = DNAC_URL + '/dna/intent/api/v1/data/reports'
    header = {'Content-Type': 'application/json', 'X-Auth-Token': dnac_auth}
    response = requests.post(url, headers=header, data=json.dumps(payload), verify=False)
    return response
  
    

def main():
    """
    This application will create a new Client Detail Report:
     - for the Global site
     - all client details
     - run now schedule
     - all client details
     - wired and wireless clients
    """

    # logging, debug level, to file {application_run.log}
    logging.basicConfig(
        filename='application_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\nCreate Report App Run Start, ', current_time)

    # get the Cisco DNA Center Auth token
    dnac_auth = token

    # find out the report view group id
    report_view_groups = get_report_view_groups(dnac_auth)
    for view in report_view_groups:
        if view['category'] == REPORT_CATEGORY:
            view_group_id = view['viewGroupId']
    #print('\nReport Category:', REPORT_CATEGORY)
    #print('Report View Group Id is:', view_group_id)

    # find out the report view id's
    report_view_ids = get_report_view_ids(view_group_id, dnac_auth)
    report_views = report_view_ids['views']
    for view in report_views:
        if view['viewName'] == VIEW_NAME:
            report_view_id = view['viewId']
    #print('Report View Name:', VIEW_NAME)
    #print('Report View Id is:', report_view_id)

  
    # get the detailed report views
    report_detail_view = get_detailed_report_views(report_view_id, view_group_id, dnac_auth)
    #print('\nClient Report Detail \n')
    #pprint(report_detail_view)

    # create the report request payload


    
    report_request = {
        'name': REPORT_NAME,
        'description': '',
        'dataCategory': REPORT_CATEGORY,
        'viewGroupId': view_group_id,
        'viewGroupVersion': '2.0.0',
        'schedule': {
            'type': 'SCHEDULE_NOW'
        },
        'deliveries': [
            {
                'type': "EMAIL",
               "emailAddresses":[
                  "ADDYOUREMAIL@SERVER.COM"
               ]
            }
        ],
        'view': {
            'name': VIEW_NAME,
            'viewId': report_view_id,
            'description': 'Client Report',
            'fieldGroups': [
                {
                    'fieldGroupName': 'client_details',
                    'fieldGroupDisplayName': 'Client Data',
                    'fields': [
                        {
                            'name': 'hostName',
                            'displayName': 'Host Name'
                        },
                        {
                            'name': 'username',
                            'displayName': 'User ID'
                        },
                        {
                            'name': 'macAddress',
                            'displayName': 'MAC Address'
                        },
                        {
                            'name': 'ipv4',
                            'displayName': 'IPv4 Address'
                        },
                        {
                            'name': 'ipv6',
                            'displayName': 'IPv6 Address'
                        },
                        {
                            'name': 'deviceType',
                            'displayName': 'Device Type'
                        },
                        {
                            'name': 'connectionStatus',
                            'displayName': 'Current Status'
                        },
                        {
                            'name': 'averageHealthScore_min',
                            'displayName': 'Min Health Score'
                        },
                        {
                            'name': 'averageHealthScore_max',
                            'displayName': 'Max Health Score'
                        },
                        {
                            'name': 'averageHealthScore_median',
                            'displayName': 'Median Health Score'
                        },
                        {
                            'name': 'usage_sum',
                            'displayName': 'Usage (MB)'
                        },
                        {
                            'name': 'connectedDeviceName',
                            'displayName': 'Connected Device Name'
                        },
                        {
                            'name': 'frequency',
                            'displayName': 'Band'
                        },
                        {
                            'name': 'rssi_median',
                            'displayName': 'RSSI (dBm)'
                        },
                        {
                            'name': 'snr_median',
                            'displayName': 'SNR (dB)'
                        },
                        {
                            'name': 'site',
                            'displayName': 'Last Location'
                        },
                        {
                            'name': 'lastUpdated',
                            'displayName': 'Last Seen'
                        },
                        {
                            'name': 'apGroup',
                            'displayName': 'AP Group'
                        },
                        {
                            'name': 'ssid',
                            'displayName': 'SSID'
                        },
                        {
                            'name': 'vlan',
                            'displayName': 'VLAN ID'
                        },
                        {
                            'name': 'vnid',
                            'displayName': 'VNID'
                        },
                        {
                            'name': 'onboardingEventTime',
                            'displayName': 'Onboarding Time'
                        },
                        {
                            'name': 'assocDoneTimestamp',
                            'displayName': 'Association Time'
                        },
                        {
                            'name': 'authDoneTimestamp',
                            'displayName': 'Authentication Time'
                        },
                        {
                            'name': 'aaaServerIp',
                            'displayName': 'Authentication Server'
                        },
                        {
                            'name': 'dhcpDoneTimestamp',
                            'displayName': 'Last DHCP Request'
                        },
                        {
                            'name': 'maxDhcpDuration_max',
                            'displayName': 'DHCP Response Time (ms)'
                        },
                        {
                            'name': 'dhcpServerIp',
                            'displayName': 'DHCP Server'
                        },
                        {
                            'name': 'linkSpeed',
                            'displayName': 'Link Speed (Mbps)'
                        },
                        {
                            'name': 'txRate_min',
                            'displayName': 'Min Tx Rate (bps)'
                        },
                        {
                            'name': 'txRate_max',
                            'displayName': 'Max Tx Rate (bps)'
                        },
                        {
                            'name': 'txRate_avg',
                            'displayName': 'Average Tx Rate (bps)'
                        },
                        {
                            'name': 'rxRate_min',
                            'displayName': 'Min Rx Rate (bps)'
                        },
                        {
                            'name': 'rxRate_max',
                            'displayName': 'Max Rx Rate (bps)'
                        },
                        {
                            'name': 'rxRate_avg',
                            'displayName': 'Average Rx Rate (bps)'
                        },
                        {
                            'name': 'txBytes_sum',
                            'displayName': 'Tx (MB)'
                        },
                        {
                            'name': 'rxBytes_sum',
                            'displayName': 'Rx (MB)'
                        },
                        {
                            'name': 'dataRate_median',
                            'displayName': 'Data Rate (Mbps)'
                        },
                        {
                            'name': 'dot11Protocol',
                            'displayName': 'Client Protocol'
                        }
                    ]
                }
            ],
            'filters': [
                {
                    'name': 'Location',
                    'displayName': 'Location',
                    'type': 'MULTI_SELECT_TREE',
                    'value': []
                },
                {
                    'name': 'DeviceType',
                    'displayName': 'Device Type',
                    'type': 'SINGLE_SELECT_ARRAY',
                    'value': []
                },
                {
                    'name': 'SSID',
                    'displayName': 'SSID',
                    'type': 'MULTI_SELECT',
                    'value': []
                },
                {
                    'name': 'Band',
                    'displayName': 'Band',
                    'type': 'MULTI_SELECT',
                    'value': []
                },
                {
                    'name': 'TimeRange',
                    'type': 'TIME_RANGE',
                    'displayName': 'Time Range',
                    'value': {
                        'timeRangeOption': 'LAST_24_HOURS',
                        'startDateTime': 0,
                        'endDateTime': 0
                    }
                }
            ],
            'format': {
                'name': 'JSON',
                'formatType': 'JSON',
                'default': False
            }
        }
    }

    report_status = create_report(report_request, dnac_auth)
    if report_status.status_code == 200:
        print('\nReport submitted')
    else:
        print('\nReport not submitted, ', report_status.text)
    current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\nCreate Report App Run End, ', current_time)
    
   
    #getting the reportId: 

    url = DNAC_URL + '/dna/intent/api/v1/data/reports'
    header = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    response = requests.post(url, headers=header, data=json.dumps(report_request), verify=False)
    data = json.dumps(response.json(), indent=4)
    dataPy = json.loads(data)
    reportId = dataPy['reportId']
    print(reportId)
    
    time.sleep(200)

    #getting the execution ID:

    url2 = DNAC_URL + f'/dna/intent/api/v1/data/reports/{reportId}/executions'

    headers = {"x-auth-token": token}
    response = requests.request("GET", url2, headers=headers, verify=False)

    data2 = json.dumps(response.json(), indent=4)
    dataPy2 = json.loads(data2)

    executionId = dataPy2['executions'][0]['executionId']
    
    print(executionId)


    #getting the healthscore from the report


    url3 = f"https://10.147.26.90/api/dnacaap/v1/daas/core/content/data-set/{reportId}/{executionId}"

    headers = {"x-auth-token": token}
    response = requests.request("GET", url3, headers=headers, verify=False)

    scoreslist=[]
    scoresum = 0


    data3 = json.dumps(response.json(), indent=4)
    dataPy3 = json.loads(data3)

    print(dataPy3)

    
    
    for details in dataPy3["client_details"]:
        scores = details["averageHealthScore_median"]
        #print(scores)
        #scoreslist.append(scores)
        scoresum += int(scores)


    ssid = dataPy3["filters"][3]["values"]


    length = len(scoreslist)
    averageValue = scoresum / length

    print(f"Total number of users is: {length}")
    print("\n")
    print(f"Average health score for the clients connected to the SSID: {ssid} is: {averageValue}")
    
    




if __name__ == '__main__':
    main()


