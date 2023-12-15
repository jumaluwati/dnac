import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from flask import Flask, render_template, request, Response

app = Flask(__name__)

# Constants
urllib3.disable_warnings()
DNAC_IP = "" #example: 10.48.90.136
USERNAME = "" #add your catalyst center's username
PASSWORD = "" #add your catalyst center's password

# Helper function to get the access token
def get_access_token():
    token_url = f"https://{DNAC_IP}/dna/system/api/v1/auth/token"
    response = requests.post(token_url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
    token_dict = response.json()
    return token_dict.get('Token')

# Route for listing devices
@app.route('/')
def list_devices():
    token = get_access_token()
    url_device_id = f"https://{DNAC_IP}/dna/intent/api/v1/network-device"
    headers = {"x-auth-token": token, 'content-type': 'application/json'}
    response_devices = requests.get(url_device_id, headers=headers, verify=False)
    devices = response_devices.json()['response']
    return render_template('list_devices.html', devices=devices)

# Route for downloading device configuration
@app.route('/download_config/<device_id>')
def download_config(device_id):
    token = get_access_token()

    # Fetch device details to get the device name (hostname)
    url_device_details = f"https://{DNAC_IP}/dna/intent/api/v1/network-device/{device_id}"
    headers = {"x-auth-token": token, 'content-type': 'application/json'}
    response_device_details = requests.get(url_device_details, headers=headers, verify=False)
    device_name = response_device_details.json().get('response', {}).get('hostname', 'UnknownDevice')

    url_device_config = f"https://{DNAC_IP}/api/v1/network-device/{device_id}/config?"
    response_devices = requests.get(url_device_config, headers=headers, verify=False)
    response_content = response_devices.content.decode('unicode_escape')

    # Set the appropriate response headers with the device name as the filename
    response = Response(response_content, content_type="text/plain")
    response.headers["Content-Disposition"] = f"attachment; filename={device_name}.txt"

    return response

if __name__ == '__main__':
    app.run()
