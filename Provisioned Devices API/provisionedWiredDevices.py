import urllib3
import json
import requests
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()

#FILL IN THE DATA (DNAC IP ADDRESS, DNAC USERNAME & PASSWORD, AND DEVICE MANAGEMENT IP ADDRESS)

DNAC_IP_ADDRESS = 'X.X.X.X'
DNAC_USERNAME = "USERNAME"
DNAC_PASSWORD = "PASSWORD"

DEVICE_MANAGEMENT_IP_ADDRESS = "X.X.X.X"

#getting the token:
tokenurl = f"https://{DNAC_IP_ADDRESS}/dna/system/api/v1/auth/token"

response = requests.request(
    "POST",
    tokenurl,
    auth=HTTPBasicAuth(DNAC_USERNAME, DNAC_PASSWORD),
    verify=False,
)

token = ""

tokenDict = response.json()
for key,value in tokenDict.items():
  token += value




######################################################################
#   API CALL TO RETRIEVE INFORMATION ABOUT THE PROVISIONED DEVICE    #
######################################################################

url = f"https://{DNAC_IP_ADDRESS}/dna/intent/api/v1/business/sda/provision-device?deviceManagementIpAddress={DEVICE_MANAGEMENT_IP_ADDRESS}"


headers = {"x-auth-token": token, 'Content-Type': 'application/json'}
response = requests.request("GET", url, headers=headers, verify=False)
print(json.dumps(response.json(), indent= 4))




################################################
#   API CALL TO DELETE A PROVISIONED DEVICE    #
################################################

#url = f"https://{DNAC_IP_ADDRESS}/dna/intent/api/v1/business/sda/provision-device?deviceManagementIpAddress={DEVICE_MANAGEMENT_IP_ADDRESS}"


#headers = {"x-auth-token": token, 'Content-Type': 'application/json'}
#response = requests.request("DELETE", url, headers=headers, verify=False)
#print(json.dumps(response.json(), indent= 4))
