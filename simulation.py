import requests
import json

apiKey = open("apikey.txt").read()

class CustomerObject():

  def __init__(self, customerId, customerData):
    self._customerId = customerId
    self._customerData = customerData
    self._customerAccountId = None



def create_customer(customer):
  url = 'http://api.reimaginebanking.com/customers?key={0}'.format(apiKey)

  response = requests.post( 
    url, 
    data=json.dumps(customer),
    headers={'content-type':'application/json'},
  )	

  if response.status_code == 201:
    print("Customer Successfully Added")

  return json.loads(response.text)['objectCreated']['_id']


def create_account(customer_id: str, customer_name: str = "test", rewards: int=0, balance:int=0):
  account = {
    "type": "Checking",
    "nickname": customer_name + "_Checking",
    "rewards": rewards,
    "balance": balance
  }

  url = 'http://api.reimaginebanking.com/customers/{0}/accounts?key={1}'.format(customer_id, apiKey)

  response = requests.post( 
    url, 
    data=json.dumps(account),
    headers={'content-type':'application/json'},
  )	

  if response.status_code == 201:
    print("Customer account for {0} Successfully Added".format(customer_id))

  return json.loads(response.text)['objectCreated']['_id']

def delete_account(accountId):
  url = 'http://api.reimaginebanking.com/accounts/{0}?key={1}'.format(accountId, apiKey)

  response = requests.delete( 
    url, 
    headers={'content-type':'application/json'},
  )	

  if response.status_code == 204:
    print("Customer account for {0} Successfully Deleted".format(customer_id))


customers = [
  {
    "first_name": "Steve",
    "last_name": "Rogers",
    "address": {
      "street_number": "1234",
      "street_name": "mont",
      "city": "glen",
      "state": "IL",
      "zip": "60025"
    }
  },
  # {
  #   "first_name": "Tony",
  #   "last_name": "Stark",
  #   "address": {
  #     "street_number": "1234",
  #     "street_name": "mont",
  #     "city": "glen",
  #     "state": "IL",
  #     "zip": "60025"
  #   }
  # },
  # {
  #   "first_name": "King",
  #   "last_name": "T'Challa",
  #   "address": {
  #     "street_number": "1234",
  #     "street_name": "mont",
  #     "city": "glen",
  #     "state": "IL",
  #     "zip": "60025"
  #   }
  # }
]

customerData = []

for customer in customers:
  customer_id = create_customer(customer)
  customerData.append(CustomerObject(customer_id, customer))


for customer in customerData:
  accountId = create_account(customer._customerId, customer._customerData['first_name'], 100, 100)
  
  print("Data: ", accountId)
  customer._customerAccountId = accountId

# add more transactions in here

for customer in customerData:
  # delete each customer's account and then their profile
  delete_account(customer._customerAccountId)