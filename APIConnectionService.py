from models.ResponseModels import *
import requests
import json


class ApiConnectionService():

    def __init__(self):
        self._apiKey = open("apikey.txt").read()
        self._baseurl = "http://api.reimaginebanking.com/"

    def GetAllValidOpponents(self, initiator_id):
        url = self._baseurl + "customers?key={0}".format(self._apiKey)
        response = requests.get( 
            url, 
            headers={'content-type':'application/json'},
        )

        if response.status_code == 200:
            customers = json.loads(response.text)
            target_customers = [
                customer for customer in customers 
                if customer['_id'] != initiator_id and self.GetAccountInformation(customer['_id']) != None]
            return target_customers
        else:
            print(response.status_code)
            return None


    def SearchForCustomerId(self, customer_first: str, customer_last: str):
        url = self._baseurl + "customers?key={0}".format(self._apiKey)
        response = requests.get( 
            url, 
            headers={'content-type':'application/json'},
        )

        if response.status_code == 200:
            customers = json.loads(response.text)
            target_customers = [customer for customer in customers if customer['first_name'] == customer_first and customer['last_name'] == customer_last]
            if len(target_customers) == 1:
                return target_customers[0]['_id']
            else:
                print("Duplicate customers in database!")
                return None
        else:
            print(response.status_code)
            return None

    def GetCustomerInformation(self, customer_id: str) -> GetCustomerInfoResponse:
        url = self._baseurl + "customers/{0}?key={1}".format(customer_id, self._apiKey)
        response = requests.get( 
            url, 
            headers={'content-type':'application/json'},
        )

        if response.status_code == 200:
            return GetCustomerInfoResponse(response)
        else:
            print(response.status_code)

    def GetAccountInformation(self, customer_id: str) -> GetCustomerAccountResponse:
        url = self._baseurl + "customers/{0}/accounts?key={1}".format(customer_id, self._apiKey)
        response = requests.get( 
            url, 
            headers={'content-type':'application/json'},
        )
        if json.loads(response.text) == []:
            return None
        elif response.status_code == 200:
            print("This person has an account!")
            return GetCustomerAccountResponse(response)
        else:
            return None

    def GetAllWithdrawals(self, customer_id):
        
        account_id = self.GetAccountInformation(customer_id).get_account_number()
        
        url = self._baseurl + "accounts/{0}/withdrawals?key={1}".format(account_id, self._apiKey)
        response = requests.get( 
            url, 
            headers={'content-type':'application/json'},
        )

        if response.status_code == 200:
            return GetAllWithdrawalsResponse(response)
        else:
            print(response.status_code)
    
    def GetAllDeposits(self, customer_id):
        
        account_id = self.GetAccountInformation(customer_id).get_account_number()
        
        url = self._baseurl + "accounts/{0}/deposits?key={1}".format(account_id, self._apiKey)
        response = requests.get( 
            url, 
            headers={'content-type':'application/json'},
        )

        if response.status_code == 200:
            return GetAllDepositsResponse(response)
        else:
            print(response.status_code)
