import sqlite3
import hashlib
import typing
import random
from APIConnectionService import ApiConnectionService


class DatabaseService:
 
    def add_user(self, customer_id: str, firstName:str, lastName:str, userName: str, userPass: str, balance: int) -> bool:
        """ add a user to the database """
        with sqlite3.connect("bank_buds.db") as conn:
            """ register user within system """
            conn.execute("""INSERT INTO user 
                (customer_id, firstName, lastName, userName, userPass, balance) VALUES (?, ?, ?, ?, ?, ?)""",
                (customer_id, firstName, lastName, userName, userPass, balance))
            conn.execute("""INSERT INTO user_record
                (rec_id, wins, losses) VALUES (?, ?, ?)""",
                (userName, 0, 0))
            conn.commit()
        return f"User {userName} added to the database"

    def get_user(self, userName: str) -> list:
        """ fetches all information about every user. returns a list
            of tuples with userid, username, userpassword """
        with sqlite3.connect("bank_buds.db") as conn:
            curr = conn.cursor()
            curr.execute("""SELECT * FROM user
                WHERE userName = ?""", (userName,))
            rows = curr.fetchall()
        return rows

    def update_win_loss(self, userId: str, result: bool) -> list:
        """ update user win loss record based on result """
        with sqlite3.connect("bank_buds.db") as conn:
            curr = conn.cursor()
            wins = curr.execute("""SELECT wins FROM user_record WHERE rec_id = ?""", (userId,)).fetchall()
            losses = curr.execute("""SELECT losses FROM user_record WHERE rec_id = ?""", (userId,)).fetchall()
            if result == 1:
                # win
                curr.execute(""" UPDATE user_record
                    SET wins = wins + 1
                    WHERE rec_id = ?""", (userId,))
                conn.commit()
            elif result == 0:
                # loss
                curr.execute(""" UPDATE user_record
                    SET losses = losses + 1
                    WHERE rec_id = ?""", (userId,))
                conn.commit()
            else:
                print("Enter a Value 0 or 1")

        return [wins, losses]

    def get_user_record(self, recId: int) -> list:
        """ returns user record given an recordId """
        with sqlite3.connect("bank_buds.db") as conn:
            curr = conn.cursor()
            curr.execute("""SELECT * from user_record
                WHERE rec_id = ?""", (recId,))
            rows = curr.fetchall()
        return rows

    def create_challenge(self, challenge_starter: str, challenge_opponent: str) -> list:
        """ initalize a challenge by passing in an challenge starter and opponent """
        with sqlite3.connect("bank_buds.db") as conn:
            curr = conn.cursor()
            combo = random.randrange(1000, 10000000)
            challenge_id = abs(hash(challenge_starter + challenge_opponent))
            curr.execute(""" INSERT into challenge_history
                    (challenge_id, challenge_starter, challenge_opponent, 
                    challenge_winner, challenge_loser, is_active) VALUES (?, ?, ?, ?, ?, ?)""",
                    (challenge_id, challenge_starter, challenge_opponent, "None", "None", 1))
            conn.commit()
        return challenge_id


    def update_challenge_status(self, challenge_id: int, result: dict) -> bool:
        """ update challenge by passing in a bool result where key is username and val is 0 or 1 """
        with sqlite3.connect("bank_buds.db") as conn:
            for key, value in result.items():
                if value == 0:
                    conn.execute(""" UPDATE challenge_history
                        SET challenge_loser = ?
                        WHERE challenge_id = ? """, (key, challenge_id))
                    conn.commit()
                if value == 1:
                    conn.execute(""" UPDATE challenge_history
                        SET challenge_winner = ?,
                            is_active = ?
                        WHERE challenge_id = ?""", (key, 0, challenge_id))
                    conn.commit()
                else:
                    print("Values must be 0 or 1")
        return "Challenge Updated"

    def get_challenge(self, challenge_id: str) -> list:
        """ given a challenge_id return all that users active challenges """
        with sqlite3.connect("bank_buds.db") as conn:
            curr = conn.cursor()
            curr.execute("""SELECT * FROM challenge_history
                WHERE challenge_id = ?""", (challenge_id,))
            rows = curr.fetchall()
        return rows

    def get_user_challenges(self, username: str) -> list:
        """ given a username returns all challenges """
        with sqlite3.connect("bank_buds.db") as conn:
            curr = conn.cursor()
            curr.execute("""SELECT * FROM challenge_history
                INNER JOIN user
                ON challenge_history.challenge_starter = user.userName
                WHERE user.userName = ?""", (username,))
            rows = curr.fetchall()
        return rows

    def get_user_balance(self, customer_id: str) -> int:
        """ returns the user's balance given a customer id"""
        apiService = ApiConnectionService()
        balance = apiService.GetAccountInformation(customer_id).get_balance()
        return balance