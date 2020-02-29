import requests
import json

"""{
  "_id": "string",
  "first_name": "string",
  "last_name": "string",
  "address": {
    "street_number": "string",
    "street_name": "string",
    "city": "string",
    "state": "string",
    "zip": "string"
  }"""
class GetCustomerInfoResponse():
	def __init__(self, response_text: requests.models.Response):
		self._response_data = json.loads(response_text.text)[0]

	def get_id(self):
		return self._response_data['_id']

	def get_first_name(self):
		return self._response_data['first_name']

	def get_last_name(self):
		return self._response_data['last_name']

"""{
  "_id": "string",
  "type": "Credit Card",
  "nickname": "string",
  "rewards": 0,
  "balance": 0,
  "account_number": "string",
  "customer_id": "string"
}"""
class GetCustomerAccountResponse():
	def __init__(self, response_text: requests.models.Response):
		self._response_data = json.loads(response_text.text)[0]
		
	def get_id(self):
		return self._response_data['_id']

	def get_type(self):
		return self._response_data['type']

	def get_nickname(self):
		return self._response_data['nickname']

	def get_balance(self):
		return self._response_data['balance']

	def get_account_number(self):
		return self._response_data['account_number']

	def get_customer_id(self): 
		return self._response_data['customer_id']

class GetAllWithdrawlsResponse():
	pass

class GetAllDepositsResponse():
	pass


