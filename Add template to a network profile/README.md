# Cisco DNA Center Automation Scripts

This repository contains three Python scripts designed to interact with Cisco DNA Center. These scripts are used to fetch template and network profile IDs and then assign a template to a network profile. The scripts use a separate configuration file to manage credentials.

## Overview

1. **[templateID.py](./templateID.py)**: Fetches template IDs and related data from Cisco DNA Center.
2. **[networkProfileID.py](./networkProfileID.py)**: Retrieves network profile IDs and related data.
3. **[AssignTemplateToProfile.py](./AssignTemplateToProfile.py)**: Uses the IDs obtained from the first two scripts to assign a template to a network profile.
4. **[config.py](./config.py)**: Contains configuration settings and credentials used by the other scripts.

## Prerequisites

- Python 3.x
- `requests` library (install using `pip install requests`)
- This is tested on Cisco DNA Center version 2.3.5.5
- Network connectivity to the Cisco DNA Center

## Configuration

Create a `config.py` file in the same directory as the scripts. This file should contain the following variables:

```python
# config.py

DNAC_IP = "1.1.1.1"
USERNAME = "user"
PASSWORD = "pass"
```
Make sure to replace the placeholders with your actual Cisco DNA Center IP address and credentials.

## Usage

### 1. Fetching Template IDs

Run `templateID.py` to retrieve all templates available in the Cisco DNA Center.



This script will print a list of template IDs and other details in JSON format.

### 2. Fetching Network Profile IDs

Run `networkProfileID.py` to get network profile IDs.



This script will display network profile details, focusing on switching profiles.

### 3. Assigning a Template to a Network Profile

Before running `AssignTemplateToProfile.py`, update the `SITE_PROFILE_ID` and `TEMPLATE_ID` variables using the output from the previous scripts.



The script updates the specified network profile with the selected template.

## Important Comments

- **templateID.py**: Comments in uppercase indicate areas where the script handles errors like failed authentication or JSON parsing issues.
- **networkProfileID.py**: Highlights the exclusive focus on switching profiles.
- **AssignTemplateToProfile.py**: Notes the placeholders for `SITE_PROFILE_ID` and `TEMPLATE_ID` that need to be replaced with actual values.

**Disclaimer**: Ensure all credentials and IP addresses are secured and handled in compliance with your organization's security policies.

## License

This project is licensed under the MIT License.
