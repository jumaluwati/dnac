import requests
import json
import time
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

def update_site_profile():
    """Update site profile using the API."""
    token = get_auth_token()
    if not token:
        print("Authentication failed")
        return

    # URL for the API endpoint
    url = f"https://{config.DNAC_IP}/api/v1/siteprofile/{SITE_PROFILE_ID}"
    
    # Headers including the authentication token
    headers = {
        'X-Auth-Token': token,
        'Content-Type': 'application/json'
    }

    # Current timestamp in milliseconds
    current_time_milliseconds = int(time.time() * 1000)

    # Payload for the PUT request
    payload = {
        "siteProfileUuid": SITE_PROFILE_ID,
        "version": 1,
        "name": "test", #NAME OF THE NETWORK PROFILE
        "namespace": "switching",
        "lastUpdatedDatetime": current_time_milliseconds,
        "profileAttributes": [
            {
                "key": "cli.templates",
                "attribs": [
                    {
                        "key": "device.family",
                        "value": "Switches and Hubs",
                        "attribs": [
                            {
                                "key": "device.series",
                                "value": None,
                                "attribs": [
                                    {
                                        "key": "device.type",
                                        "value": None,
                                        "attribs": [
                                            {
                                                "key": "template.id",
                                                "value": TEMPLATE_ID,
                                                "attribs": [
                                                    {"key": "template.name", "value": "Repository"}, #NAME OF THE TEMPLATE
                                                    {"key": "template.version", "value": "1"},
                                                    {"key": "template.softwareType", "value": "IOS-XE"},
                                                    {"key": "template.softwareVariant", "value": "XE"}
                                                ]
                                            },
                                            {"key": "device.tag", "value": "", "attribs": []}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Make the PUT request
    response = requests.put(url, headers=headers, json=payload, verify=False)
    if response.status_code == 202:
        print("API call successful, update accepted.")
    else:
        print(f"Failed to update site profile: {response.status_code}")
        print(response.text)

# Execute the function to make the API call
update_site_profile()