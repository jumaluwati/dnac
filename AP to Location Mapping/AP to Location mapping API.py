import urllib3
import json
import requests
from dnacentersdk import DNACenterAPI



urllib3.disable_warnings()

#credentials
DNAC_IP = ''
USERNAME = ''
PASSWORD = ''


#DNA Center credentials and URL
dnac = DNACenterAPI(username = USERNAME,
					password = PASSWORD,
					base_url = f'https://{DNAC_IP}:443',
					version = '2.3.3.0',
					verify = False)


#####################################################################################################

### Device UUID is needed for this APIs

# Getting all the Devices (APs) IDs along with their names


ap_id = []

apToLocationMapping = []
apToLocationMapping_zipped = []

apName = []
apLocation = []

data = dnac.devices.get_device_list(family = 'Unified AP')
for i in data['response']:
    ap_id.append(i['id'])
    print('\n')



#Getting all the APs names and location via device UUIDs taken from previou API

for i in ap_id:

	data = dnac.devices.get_device_detail(identifier = 'uuid', search_by = i)

	apToLocationMapping.append(data['response']['location'])
	apToLocationMapping.append(data['response']['nwDeviceName'])



# Pairing data in a dictionary (key, value pairs)

data_pairs = zip(apToLocationMapping[::2],apToLocationMapping[1::2])
for i in data_pairs:
	apToLocationMapping_zipped.append(i)


mydict = dict()

for line in apToLocationMapping_zipped:
    if line[0] in mydict:
        # append the new number to the existing array at this slot
        mydict[line[0]].append(line[1])
    else:
        # create a new array in this slot
        mydict[line[0]] = [line[1]]

for k in mydict:

    apName.append(k)
    apLocation.append(mydict[k])

# Printing the result

result = json.dumps(mydict, indent=4)
print(result)












