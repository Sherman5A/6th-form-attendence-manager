import sqlite3
from sqlite3.dbapi2 import Cursor, Error


class sqlInterface:

    def __init__(self, file):
        self.file = file
    
    def create_connection(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect(self.file)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)
      
    def create_table(self, sql_command):       
        try:
            self.cursor.execute(sql_command)
        except Error as e:
            print(e)
    
    def get_data(self, sql_command, values=None):
        # Overloading
        # Allows user to put values in string or as a seperate argument.
        if values is None:
            try:
                self.cursor.execute(sql_command)
                return self.cursor.fetchall()
            except Error as e:
                print(e)
        else:  # Values argument is not left blank
            try:
                self.cursor.execute(sql_command, values)
                return self.cursor.fetchall()
            except Error as e:
                print(e)

    def insert_data(self, sql_command, values=None):
        # Overloading
        # Allows user to put values in string or as a seperate argument.
        if values is None:
            try:
                self.cursor.execute(sql_command)
                self.connection.commit()
            except Error as e:
                print(e)
        else:  # Values argument is not left blank
            try:
                self.cursor.execute(sql_command, values)
                self.connection.commit()
            except Error as e:
                print(e)
            