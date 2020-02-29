# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

customerId = '3463784693478'
apiKey = open("apikey.txt").read()

url = 'http://api.reimaginebanking.com/customers/?key={}'.format(customerId,apiKey)
payload = {
  "first_name": "string",
  "last_name": "string",
  "address": {
    "street_number": "string",
    "street_name": "string",
    "city": "string",
    "state": "string",
    "zip": "string"
  }
}

# Create a Savings Account
response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

print(response)

if response.status_code == 201:
	print('account created')