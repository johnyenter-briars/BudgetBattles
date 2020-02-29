from models.ResponseModels import *
import requests
import json


class ApiConnectionService():

    def __init__(self):
        self._apiKey = open("apikey.txt").read()
        self._baseurl = "http://api.reimaginebanking.com/"


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
