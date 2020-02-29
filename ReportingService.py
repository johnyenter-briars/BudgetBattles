from APIConnectionService import ApiConnectionService
import datetime
connection = ApiConnectionService()
class ReportingService:
    def __init__(self):
        print()
    def getCurentHistory(self, id):
        wd = connection.GetAllWithdrawals(id)
        withdrawals = wd.get_withdrawals()
        print(withdrawals)
        initialBalance = connection.GetAccountInformation(id).get_balance()
        goalBalance = 69


        withdrawals.sort(key=lambda x: datetime.date(int(x['transaction_date'].split('-')[0]),int(x['transaction_date'].split('-')[1]),int(x['transaction_date'].split('-')[0][2])), reverse=True)

        print(withdrawals)