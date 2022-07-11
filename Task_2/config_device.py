#!/usr/bin/env python

#pip install json
#pip install requests
#pip install prettytable
#pip install urllib3

import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from prettytable import PrettyTable
from pprint import pp


dnac = {
        'host': 'sandboxdnac2.cisco.com',
        'port': 830,
        'username': 'devnetuser',
        'password': 'Cisco123!'
        }

dnac_devices = PrettyTable(['Hostname','IP Address','Device Id'])
dnac_devices.padding_width = 1

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
            'content-type': 'application/json',
            'x-auth-token': ''
            }
    
def dnac_login(host, username, password):
    url = 'https://sandboxdnac2.cisco.com/api/system/v1/auth/token'
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
        dnac_devices.add_row([item['hostname'],
                                item['managementIpAddress'],
                                item['instanceUuid']])


login = dnac_login(dnac['host'], dnac['username'], dnac['password'])
network_device_list(dnac, login)
print ('\nAvailable devices:\n')
print(dnac_devices)
config = input('\nEnter \'/config\' to get device configuration: ')
while '/config' in config:
    number = input('\nEnter number of device (1 or 2 or 3 or input "quit" for exit): ')
    if str(1) in number:
        instanceUuid = 'd354c924-f8ac-425f-b167-999f157e35e8'
    elif str(2) in number:
        instanceUuid = '1c5f3896-9cac-40f8-85b3-64d2ae38f171'
    elif str(3) in number:
        instanceUuid = '420aab4f-ff7e-41e0-8f59-eb18c0b80759'
    elif str(quit) in number:
        break
    else:
        break
    def network_device_list(dnac, token):
        url = 'https://{}/api/v1/network-device/{}/config'.format(dnac['host'], instanceUuid)
        headers['x-auth-token'] = token
        response = requests.get(url, headers=headers, verify=False)
        data = response.json()
        print('\n#######################################################################################################################################')
        print('#######################################################################################################################################\n')
        pp(data)
        print('\n#######################################################################################################################################')
        print('#######################################################################################################################################\n')

        print(dnac_devices)

    login = dnac_login(dnac['host'], dnac['username'], dnac['password'])
    network_device_list(dnac, login)

else:
    print('Wrong command.')

input('press Enter for quit: ')