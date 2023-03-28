
This script uses 2 of Cisco DNA Center APIs to list Access Points and their locations in the network

The output is a dictionary of:
- keys: Locations
- values: list of AP names

This simple script utilizes the DNA Center SDK library (make sure to download it, along with the other libraries, for the script to work)

The APIs used are:
1. Get Device List
   - this API is used to extrct the devices UUIDs, then apply them in the next API call as a parameter
3. Get Device Detail
   - this API call is used to fetch for the APs and their locations



Note:
- Make sure to have the dnacentersdk library downloaded
- Add your DNA Centers IP address, username, and password
