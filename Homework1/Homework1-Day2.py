from user import User
import datetime
from datetime import date
import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")



connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

dob = datetime.datetime(2000,1,20)
str_dob = dob.date().isoformat()
query = "INSERT INTO users (firstname, lastname, dateofbirth) VALUES ('jane2','doe2','2002-02-02')"
# execute_query(connection, query)  

select_users = "SELECT * FROM users"
users = execute_read_query(connection, select_users)

for user in users:
    dob = user[3]
    today = date.today()
    dayinterval = today - dob
    print(user[1] + " is " + str(dayinterval.days) + " days old")



# adding a contact
def option_addcontact():
    contacts_from_user = 2
    contacts_details = 'Thomas Alexzander'
    contacts_date = '2001-12-01'
    query = "INSERT INTO contacts (id,contactDetails,creationDate) VALUES (%s,'%s','%s')" % (contacts_from_user,contacts_details,contacts_date)
    execute_query(connection,query)

# removing a contact

def option_delcontact():
    contacts_id_user = 1
    delete_user = "DELETE FROM contacts WHERE id = %s" % (contacts_id_user)
    execute_query(connection,delete_user)

# update a contact


def option_updcontact():
    upd_id = 2
    upd_details = "Thomas Hendderson"
    #upd_date = "2011-12-01"
    upd_contacts_query = """
    UPDATE contacts
    SET contactDetails = '%s'
    WHERE id = %s """ % (upd_details,upd_id)
    execute_query(connection,upd_contacts_query)


# Creating the menu

def menu():
    x = 'continue'
    while x == 'continue':

        print('Menu')
        print('a - Add contact')
        print('d - Remove contact')
        print('u - Update contact details')
        print('b - Output all contacts in alphabetical order')
        print('c - Output all contacts by creation date')
        print('o - Output all contacts')
        print('q - Quit')

        option = input('Choose an option:\n')
        if option == 'a':
            print('Option Add contact was choosen')
            option_addcontact()
            
        if option == 'd':
            print('Option Remove contact was choosen')
            option_delcontact()
        if option == 'u':
            print('Option Update contact was choosen')
            option_updcontact()
        if option == 'b':
            print('Option Output alphabetical order was choosen')

        if option == 'c':
            print('Option Output date order was choosen')

        if option == 'o':
            print('Output all was choosen')

        if option == 'q':
            print('Option Quit was choosen')
            x = 'break'


select_users = "SELECT * FROM contacts"
users = execute_read_query(connection, select_users)

menu()
         
#refrences
# Used code from Professor Otto code that was done during class