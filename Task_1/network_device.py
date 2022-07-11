# #!/usr/bin/env python

import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from prettytable import PrettyTable
import getpass

command = input('Enter \'/device\' for information about devices: ')
if '/device' in command:
    dnac = {
            'host': 'sandboxdnac.cisco.com',
            'port': 443,
            #'username': input('Entet username: '),
            #'password': getpass.getpass('Entet password: '),
            'username': 'devnetuser',
            'password': 'Cisco123!'
            }

    print ('\nConnecting to https://sandboxdnac.cisco.com \n')
    dnac_devices = PrettyTable(['Hostname','IP Address','Platform Id','Software Type','Software Version','Up Time','Serial No' ])
    dnac_devices.padding_width = 1

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    headers = {
                'content-type': 'application/json',
                'x-auth-token': ''
            }
    
    def dnac_login(host, username, password):
        url = 'https://{}/api/system/v1/auth/token'.format(host)
        response = requests.request('POST', url, auth=HTTPBasicAuth(username, password),
                                    headers=headers, verify=False)
        return response.json()['Token']

    def network_device_list(dnac, token):
        url = 'https://{}/api/v1/network-device'.format(dnac['host'])
        headers['x-auth-token'] = token
        response = requests.get(url, headers=headers, verify=False)
        data = response.json()
        #print(data)
        for item in data['response']:
            dnac_devices.add_row([item['hostname'],item['managementIpAddress'],item['platformId'],item['softwareType'],item['softwareVersion'],item['upTime'],item['serialNumber']])


    login = dnac_login(dnac['host'], dnac['username'], dnac['password'])
    network_device_list(dnac, login)

    print(dnac_devices)
else:
    print('Wrong command.')

input('press Enter for quit: ')