# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

customerId = '5e59fa50322fa016762f3a20'
apiKey = '7272d9d789aacbedcbaac7768acd6fbe'

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
payload = {
  "type": "Savings",
  "nickname": "Bill Math",
  "rewards": 10000,
  "balance": 10000,	
}
# Create a Savings Account
response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)
print(response.status_code)
if response.status_code == 201:
	print('account created')