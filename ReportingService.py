from APIConnectionService import ApiConnectionService
import datetime
import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate
from typing import Any
import os
import sys


connection = ApiConnectionService()


class ReportingService:
    
    def __init__(self):
        self.deposits:Any
        self.withdrawals:Any
        
    def generateUserHistory(self, id):
        transactions = []
        balances = []
        initialBalance = 100
        currentBalance = initialBalance
        goalBalance = 69

        self.withdrawals = connection.GetAllWithdrawals(id).get_withdrawals()
        self.deposits = connection.GetAllDeposits(id).get_deposits()
        self.withdrawals.sort(key=lambda x: datetime.date(int(x['transaction_date'].split('-')[0]),int(x['transaction_date'].split('-')[1]),int(x['transaction_date'].split('-')[2])), reverse=False)
        self.deposits.sort(key=lambda x: datetime.date(int(x['transaction_date'].split('-')[0]),int(x['transaction_date'].split('-')[1]),int(x['transaction_date'].split('-')[2])), reverse=False)
        
        transactions = transactions+self.withdrawals
        transactions = transactions+self.deposits
        transactions.sort(key=lambda x: datetime.date(int(x['transaction_date'].split('-')[0]),int(x['transaction_date'].split('-')[1]),int(x['transaction_date'].split('-')[2])), reverse=False)
       
        for transaction in transactions:
            print(transaction)
            if transaction['type'] == 'deposit':
                currentBalance+=transaction['amount']
            elif transaction['type'] == 'withdrawal':
                currentBalance-=transaction['amount']
            balances.append((currentBalance, transaction['transaction_date']))

        # calls plot generation function
        self.generatePlot(self.withdrawals,'withdrawal', id)
        self.generatePlot(self.deposits,'deposit', id)
        self.generateBalancePlot(balances, id)

    #generates generalized plot for withdrawals or deposits
    def generatePlot(self,list,type, user_id):
        plt.switch_backend('Agg')
        amounts = []
        dates = []
        for element in list:
            amounts.append(element['amount'])
            dates.append(element['transaction_date'])
        plt.figure(figsize=(15,10))
        plt.plot(dates,amounts)

        plt.xlabel('Dates')
        plt.ylabel(type+' Amount ($)')
        plt.savefig('static/'+type+"_"+user_id+'.png')

    #creates plot for balance over time
    def generateBalancePlot(self, list, user_id):
        plt.switch_backend('Agg')
        amounts = []
        dates = []
        for element in list:
            # print(element)
            amounts.append(element[0])
            dates.append(element[1])
        plt.figure(figsize=(15,10))
        plt.plot(dates,amounts)
        plt.xlabel('Dates')
        plt.ylabel('Balance Amount ($)')
        plt.savefig('static/balance_' +user_id+'.png')