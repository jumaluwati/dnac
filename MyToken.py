import requests
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()
url = "https://10.147.26.90/dna/system/api/v1/auth/token"

response = requests.request(
    "POST",
    url,
    auth=HTTPBasicAuth("USERNAME", "PASSWORD"),
    verify=False,
)

print(response.json())