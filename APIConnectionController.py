from models.ResponseModels import *
import requests
import json


class ApiConnectionController():

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