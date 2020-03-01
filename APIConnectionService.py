from models.ResponseModels import *
import requests
import json


class ApiConnectionService():

    def __init__(self):
        self._apiKey = open("apikey.txt").read()
        self._baseurl = "http://api.reimaginebanking.com/"

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
                return target_customers[0]
            else:
                print("Duplicate customers in database!")
        else:
            print(response.status_code)



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

        if response.status_code == 200:
            return GetCustomerAccountResponse(response)
        else:
            print(response.status_code)

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
