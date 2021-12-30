import SQL_interface
import re
from datetime import datetime


def create_user(account_variables):
    """"Create a new user, performs validation, then adds to sql table"""

    sql_database = SQL_interface.sqlInterface('test.db')
    sql_database.create_connection()

    def create_table():
        """Creates user table"""

        sql_create_user_table = """ CREATE TABLE IF NOT EXISTS users (
                                "id" INTEGER,
                                first_name TEXT NOT NULL,
                                second_name TEXT NOT NULL,
                                year_group TEXT NOT NULL,
                                form_group TEXT NOT NULL,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL,
	                            PRIMARY KEY("id" AUTOINCREMENT)
                            ); """
        sql_database.create_table(sql_create_user_table)

    def write_user():
        """Write variable to database table"""

        sql_database.insert_data("INSERT INTO users(first_name, second_name, year_group, form_group, username, password) VALUES(?, ?, ?, ?, ?, ?);", (
            account_variables['first_name'], account_variables['second_name'], account_variables['year_group'], account_variables['form_group'], account_variables['username'], account_variables['password']))

    for key, value in account_variables.items():

        if validation.len_check(value, 20) == False:
            return False, key, 'Length check, check field is not empty and is under 20 characters '

        if key == 'first_name' or key == 'second_name':
            if validation.string_check(value) == False:
                return False, key, 'Alpha check'
    if account_variables['password'] != account_variables['password_repeat']:
        return False, 'password', "Passwords don't match"

    if validation.password_strength(account_variables['password']) == False:
        return False, 'password', 'Password not strong enough. Use >= 7 characters and both upper and lower case letters'
    
    create_table()

    common_usernames = sql_database.get_data(
        "SELECT username FROM users WHERE username=?", (account_variables['username'],))
    if len(common_usernames) != 0:
        return False, 'username', 'Username is not unique'

    write_user()
    return True


def check_login_creds(input_username, input_password):
    pass

def search_users(search_terms):
    """Searches the user tables with the dictonary provided in args"""

    # if no terms are provided, return all users
    if len(search_terms) != 0:
        sql_search = "SELECT * FROM users WHERE "
        # takes keys, values, formats value, joins them with '=', and then adds AND between dict keys
        # adds ; to end sql statment
        sql_search += ' AND '.join('='.join((key, "'{}'".format(value))) for key, value in search_terms.items()) + ';'
    else: 
        sql_search = "SELECT * FROM users;"

    # create SQL connection
    sql_database = SQL_interface.sqlInterface('test.db')
    sql_database.create_connection()
    # execute and return sql search
    return sql_database.get_data(sql_search)


class validation():
    """Class containing validation"""

    def string_check(input):
        """Checks if a string contains digits or special characters"""

        regex_arguement = re.compile('\d+|[@;:()]')
        try:
            regex_return = re.search(regex_arguement, input)
            if regex_return:
                return False
            return True
        except TypeError:
            print('Variable is not string')
            return False

    def len_check(input, max_len):
        """Checks length of string
            input: variable to check
            max_len: int maximum length to return true
        """
        if len(input) <= 0 or len(input) > max_len:
            return False
        return True

    def validate_num(input, min_num=None):
        """Checks if input is int
            input: variable to check
            min_num: optionial, input can not be lower than value"""
        try:
            converted_input = int(input)
            if min_num == None:
                return True
            return converted_input > min_num
        except ValueError:
            return False

    def password_strength(input):
        """Check password is >= 7 characters, contains lower and upper case """
        if len(input) < 7:
            return False

        if input.isupper() == False and input.islower() == False:
            return True
        return False


def get_date_time():
    """Returns date and time"""

    unformatted_datetime = datetime.now()
    date_str = unformatted_datetime.strftime('%d/%m/%Y')
    time_str = unformatted_datetime.strftime('%H:%M:%S')
    return date_str, time_str


def sign_in_school():
    date_str, time_str = get_date_time()
