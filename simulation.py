import requests
import json

apiKey = open("apikey.txt").read()

def create_customer(customer):
  url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)

  response = requests.post( 
	url, 
	data=json.dumps(customer),
	headers={'content-type':'application/json'},
)	

  if response.status_code == 201:
    print("Customer Successfully Added")
  

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
  {
    "first_name": "Tony",
    "last_name": "Stark",
    "address": {
      "street_number": "1234",
      "street_name": "mont",
      "city": "glen",
      "state": "IL",
      "zip": "60025"
    }
  },
  {
    "first_name": "Kind",
    "last_name": "T'Challa",
    "address": {
      "street_number": "1234",
      "street_name": "mont",
      "city": "glen",
      "state": "IL",
      "zip": "60025"
    }
  }
]

for customer in customers:
	create_customer(customer)


for customer in customers:
	# add an account for each customer	
	pass

# add more transactions in here

for customer in customers:
	# delete each customer's account and then their profile
	pass

