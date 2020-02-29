from APIConnectionService import ApiConnectionService
import datetime
connection = ApiConnectionService()
import matplotlib
import matplotlib.pyplot as plt
from typing import Any
import os
import sys


class ReportingService:
    
    def __init__(self):
        self.deposits:Any
        self.withdrawals:Any
        print()
    def getCurentHistory(self, id):
        transactions = []
        balances = []
        initialBalance = 100
        currentBalance = initialBalance
        goalBalance = 69

        self.withdrawals = connection.GetAllWithdrawals(id).get_withdrawals()
        self.deposits = connection.GetAllDeposits(id).get_deposits()
        self.withdrawals.sort(key=lambda x: datetime.date(int(x['transaction_date'].split('-')[0]),int(x['transaction_date'].split('-')[1]),int(x['transaction_date'].split('-')[0][2])), reverse=True)
        self.deposits.sort(key=lambda x: datetime.date(int(x['transaction_date'].split('-')[0]),int(x['transaction_date'].split('-')[1]),int(x['transaction_date'].split('-')[0][2])), reverse=True)
        
        transactions = transactions+self.withdrawals
        transactions = transactions+self.deposits
        transactions.sort(key=lambda x: datetime.date(int(x['transaction_date'].split('-')[0]),int(x['transaction_date'].split('-')[1]),int(x['transaction_date'].split('-')[0][2])), reverse=True)

        for transaction in transactions:
            if transaction['type'] == 'deposit':
                currentBalance+=transaction['amount']
            elif transaction['type'] == 'withdrawal':
                currentBalance-=transaction['amount']
            balances.append((currentBalance, transaction['transaction_date']))
        # calls plot generation function
        self.generatePlot(self.withdrawals,'withdrawal')
        self.generatePlot(self.deposits,'deposit')
        self.generateBalancePlot(balances)
    #generates generalized plot for withdrawals or deposits
    def generatePlot(self,list,type):
        plt.switch_backend('Agg')
        amounts = []
        dates = []
        for element in list:
            amounts.append(element['amount'])
            dates.append(element['transaction_date'])
        plt.plot(dates,amounts)
        plt.xlabel('Dates')
        plt.ylabel(type+' Amount ($)')
        plt.savefig('static/'+type+'.png')
    #creates plot for balance over time
    def generateBalancePlot(self, list):
        plt.switch_backend('Agg')
        amounts = []
        dates = []
        for element in list:
            print(element)
            amounts.append(element[0])
            dates.append(element[1])
        plt.plot(dates,amounts)
        plt.xlabel('Dates')
        plt.ylabel('Balance Amount ($)')
        plt.savefig('static/balance.png')