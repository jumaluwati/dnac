# Copyright (c) 2016-2022 Cisco and/or its affiliates
# by/ jalluwat@cisco.com
#
# this code generates a custom Excel report for selected end user/s managed by Cisco DNA Center
#
#Please downlaod first the DNACenterSDK by typing on your terminal/powershell : pip install dnacentersdk


import urllib3
from dnacentersdk import DNACenterAPI
import json
import time
import pandas as pd
import xlsxwriter
import requests
from datetime import datetime
import schedule

urllib3.disable_warnings()

#DNA Center credentials and URL (fill the blanks)

dnac = DNACenterAPI(username = '',
					password = '',
					base_url = 'https://10.147.26.90:443',
					version = '2.2.3.3',
					verify = False)


def collection():

	#adding time
	current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

	#user mac addresses of interest
	macAddress = ['02:35:12:F0:00:11', '02:35:12:F0:00:12'] #Add MAC addresses like how its done
	count = 0
	for i in macAddress:
		
		headers = {
	    	'entity_type': "mac_address",
	    	'entity_value': i
	    	}

		#The parameters used in this example are: user ID, connection status, ssid, location and AP type. Feel free to add more according to whats available
		data = dnac.users.get_user_enrichment_details(headers)
		userId = data[0]['userDetails']['userId']
		connectionStatus = data[0]['userDetails']['connectionStatus']
		ssid = data[0]['userDetails']['ssid']
		location = data[0]['userDetails']['location']
		apDetails = data[0]['connectedDevice'][0]['deviceDetails']['type']

		count +=1
		print(f'{count}: \n')

		if userId == None:
			print(f"User ID: User ID doesn't exit, but the MAC Address is: {i}")
			userId = i
		else:
			print(f'User ID: {userId}')
		print(f'Connection Status: {connectionStatus}')
		print(f'SSID: {ssid}')
		print(f'Locatoin: {location}')
		print(f'AP Name: {apDetails}')

		print('----------------------------')
		print('\n')


		#data = requests.get(api_url).json()

		#Adding data to excel file called Testing.xlsx (THE FILE MUST EXIST BEFORE RUNNING THE CODE)

		my_columns = ['Time', 'User ID', 'Connection Status', 'SSID', 'Location', 'AP Connected To']
		final_dataframe = pd.read_excel('Testing.xlsx')

		final_dataframe = final_dataframe.append(
		    pd.Series(
		        [
		            current_time,
		            userId,
		            connectionStatus,
		            ssid,
		            location,
		            apDetails
		        ],
		        index=my_columns),
		    ignore_index=True
		)

		writer = pd.ExcelWriter('Testing.xlsx', engine='xlsxwriter')
		final_dataframe.to_excel(writer, 'AKER', index=False)

		#background_color = '#000000'
		#font_color = '#E8130F'

		writer.save()

#The option to have this code runs every X amoutn of time

'''
schedule.every(10).seconds.do(collection)

while 1:
    schedule.run_pending()



    time.sleep(1)

'''
collection()
