import sqlite3
import typing

class DatabaseService:
    
    def add_user(self, userId: int, userName: str, userPass: str) -> bool:
        with sqlite3.connect("bank_buds.db") as conn:
            """ register user within system """
            conn.execute("""INSERT INTO user 
                (userId, userName, userPass) VALUES (?, ?, ?)""",
                (userId, userName, userPass))
            conn.execute("""INSERT INTO user_record
                (rec_id, wins, losses) VALUES (?, ?, ?)""",
                (userId, 0, 0))
            conn.commit()
        return f"User {userName} added to the database"

    def get_user(self, userId: int) -> list:
        """ fetches all information about every user. returns a list
            of tuples with userid, username, userpassword """
        with sqlite3.connect("bank_buds.db") as conn:
            curr = conn.cursor()
            curr.execute("""SELECT * FROM user
                WHERE userId = ?""", (userId,))
            rows = curr.fetchall()
        return rows

    def update_win_loss(self, userId: int, result: bool) -> list:
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

    def create_challenge(self, conn: sqlite3.Connection, challenge_id: int) -> list:
        """ initalize a challenge by passing in an id """
        pass

    def update_challenge_status(self, conn: sqlite3.Connection, result: dict) -> bool:
        """ update challenge by passing in a bool result if 0 ==> makes current_user loser """
        pass

