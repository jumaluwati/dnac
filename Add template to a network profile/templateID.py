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

def fetch_templates(token):
    """Fetch all templates from Cisco DNA Center."""
    url = f"https://{config.DNAC_IP}/api/v1/template-programmer/extendedTemplates"
    headers = {"x-auth-token": token, "content-type": "application/json"}
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()  # This will handle errors like 401
    return response.json().get('response', [])

def extract_template_info(templates):
    """Extract specific fields from each template."""
    filtered_templates = []
    for template in templates:
        filtered_template = {
            "id": template.get("id"),
            "name": template.get("name"),
            "description": template.get("description"),
            "tags": template.get("tags"),
            "deviceTypes": template.get("deviceTypes"),
            "softwareType": template.get("softwareType"),
            "softwareVariant": template.get("softwareVariant"),
            "templateContent": template.get("templateContent")
        }
        filtered_templates.append(filtered_template)
    return filtered_templates

if __name__ == "__main__":
    token = get_auth_token()
    if token:
        templates = fetch_templates(token)
        filtered_templates = extract_template_info(templates)
        print(json.dumps(filtered_templates, indent=4))
    else:
        print("Authentication failed.")