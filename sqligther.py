import sqlite3
import datetime


class SQLighter():
    def __init__(self, database):
        self.data = sqlite3.connect(database)
        self.cur = self.data.cursor()

    def save_results(self, expression, result, time):
        self.cur.execute('''INSERT INTO [history] (expression, result, time) VALUES (?, ?, ?)''',
                         (expression, result, time))
        self.data.commit()

    def show_results(self):
        result = self.cur.execute('''SELECT * FROM [history]''').fetchall()
        return result

    def remove_results(self, ids):
        for i in ids:
            self.cur.execute('''DELETE FROM [history]
                                WHERE id=?''', (i,))
            self.data.commit()
