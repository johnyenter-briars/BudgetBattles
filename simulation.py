# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

class NewCustomerPostResponseObject(object):
	def __init__(self, response_text):
		self._response_data = json.loads(response_text)['objectCreated']

	def get_id(self):
		return self._response_data['_id']

customer1 = {
  "first_name": "john2",
  "last_name": "doe",
  "address": {
    "street_number": "1234",
    "street_name": "mont",
    "city": "glen",
    "state": "IL",
    "zip": "60025"
  }
}
customerId = '3463784693478'
apiKey = open("apikey.txt").read()

url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)

payload = customer1
# Create a Savings Account
response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

if response.status_code == 201:
	print(NewCustomerPostResponseObject(response.text).get_id())