import requests
import json
from requests.auth import HTTPBasicAuth
import config

# Disable warnings for insecure connections
requests.packages.urllib3.disable_warnings()

def get_auth_token():
    """Authenticate and get the token from Cisco DNA Center."""
    token_url = f"https://{config.DNAC_IP}/dna/system/api/v1/auth/token"
    response = requests.post(
        token_url,
        auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD),
        verify=False,
    )
    response.raise_for_status()
    try:
        token = response.json().get('Token')
        if not token:
            print("Failed to retrieve token")
        return token
    except json.JSONDecodeError:
        print("Failed to decode JSON response")
        return None

def make_request():
    """Make a GET request to the specified API endpoint."""
    url = f"https://{config.DNAC_IP}/api/v1/siteprofile"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": get_auth_token()
    }
    params = {
        "populated": "false",
        "exludeSettings": "true",
        "namespace": "switching", #IT WILL ONLY SHOW SWITCHING PROFILES
        "sort": "name",
        "sortOrder": "asc",
        "offset": "1",
        "limit": "25"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        verify=False
    )
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(json.dumps(data, indent=4))
        except json.JSONDecodeError:
            print("Failed to decode JSON response")
    else:
        print(f"Request failed with status code {response.status_code}")

if __name__ == "__main__":
    make_request()