import sqlite3
import typing

class DatabaseService:

    def initialize_database() -> sqlite3.Connection:
        """Create a sqlite3 database stored in memory with two tables to hold
        users, records and history. Returns the connection to the created database."""
        conn = sqlite3.connect("bank_buds.db")

        conn.execute("""CREATE TABLE IF NOT EXISTS user(
            userId INTEGER PRIMARY KEY NOT NULL,
            userName TEXT NOT NULL,
            userPass TEXT NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS user_record(
            rec_id INTEGER REFERENCES user NOT NULL,
            wins INTEGER NOT NULL,
            losses INTEGER NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS challenge_history(
            challenge_id INTEGER NOT NULL,
            challenge_winner REFERENCES user NOT NULL,
            challenge_loser REFERENCES user NOT NULL,
            is_active NUMERIC NOT NULL )""")
        
        return conn
 
    def add_user(conn: sqlite3.Connection, userId: int, userName: str, userPass: str) -> bool:
        """ register user within system """
        conn.execute("""INSERT INTO user 
            (userId, userName, userPass) VALUES (?, ?, ?)""",
            (userId, userName, userPass))
        conn.execute("""INSERT INTO user_record
            (rec_id, wins, losses) VALUES (?, ?, ?)""",
            (userId, 0, 0))

        conn.commit()
        return f"User {userName} added to the database"

    def get_user(conn: sqlite3.Connection, userId: int) -> list:
        """ fetches all information about every user. returns a list
            of tuples with userid, username, userpassword """
        curr = conn.cursor()
        curr.execute("""SELECT * FROM user
            WHERE userId = ?""", (userId,))
        rows = curr.fetchall()
        return rows

    def update_win_loss(conn: sqlite3.Connection, userId: int, result: bool) -> list:
        """ update user win loss record based on result """
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

    def get_user_record(conn: sqlite3.Connection, recId: int) -> list:
        """ returns user record given an recordId """
        curr = conn.cursor()
        curr.execute("""SELECT * from user_record
            WHERE rec_id = ?""", (recId,))
        rows = curr.fetchall()
        return rows

    def create_challenge(conn: sqlite3.Connection, challenge_id: int) -> list:
        """ initalize a challenge by passing in an id """
        pass

    def update_challenge_status(conn: sqlite3.Connection, result: dict) -> bool:
        """ update challenge by passing in a bool result if 0 ==> makes current_user loser """
        pass


    if __name__ == "__main__":
        conn = initialize_database()
        print("--adding users--")
        '''
        print(add_user(conn, 100, "joe", "joePass"))
        print(add_user(conn, 200, "bill", "billPass"))
        '''
        print("--get registered user info--")
        print(get_user(conn, 100))
        print("--pre win loss record--")
        print(get_user_record(conn, 100))
        print("--add wins--")
        print(update_win_loss(conn, 100, 1))
        print(update_win_loss(conn, 100, 1))
        print(update_win_loss(conn, 100, 1))
        print("--add losses--")
        print(update_win_loss(conn, 100, 0))
        print(update_win_loss(conn, 100, 0))
        print(update_win_loss(conn, 100, 0))
        print("--post win loss record--")
        print(get_user_record(conn, 100))
    

