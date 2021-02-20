from user import User
from contacts import Contacts
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


# create connection to database 

connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")


# adding a contact

def option_addcontact():
    select_contacts = "SELECT * FROM contacts"
    contacts = execute_read_query(connection, select_contacts)

    # Created a list for the ids
    # This will allow to make sure that whenever a user adds a new contact
    # It uses a new id by adding +1 to the previous number

    contact_list = [0]
    for contact in contacts:
        id = contact[0]
        contact_list.append(id)
    print(contact_list)
    
    contacts_from_user = (contact_list[-1] + 1)
    
    print('Enter Contact Details: \n')
    contacts_First = input('Enter First Name: \n')
    contacts_Last = input('Enter Last Name: \n')
    contacts_phone = input('Enter Phone Number in format XXX-XXX-XXXX : \n')

    # combines the first and last name into one variable

    contacts_details = '%s %s' % (contacts_First,contacts_Last)
    
    # asks for the date in seperate variables (Y/M/D) and then combines it into one

    print('Enter date in format (Y/M/D) XXXX-XX-XX: \n')
    contacts_year = input('Enter Year: \n')
    contacts_month = input('Enter Month: \n')
    contacts_day = input('Enter Day: \n')
    contacts_date = '%s-%s-%s' % (contacts_year,contacts_month,contacts_day)
    
    query = "INSERT INTO contacts (id,contactDetails,creationDate,phoneNum) VALUES (%s,'%s','%s','%s')" % (contacts_from_user,contacts_details,contacts_date,contacts_phone)
    execute_query(connection,query)

# removing a contact

def option_delcontact():
    print("List of Contacts: \n")

    # Selects all contacts from database and displays it to the user 
    # in order for them to pick one to update

    select_contacts = "SELECT * FROM contacts"
    contacts = execute_read_query(connection, select_contacts)
    for cont in contacts:
        print(cont[0],cont[1],cont[2])
    contacts_id_user = int(input('Enter contact ID \n'))
    delete_user = "DELETE FROM contacts WHERE id = %s" % (contacts_id_user)
    execute_query(connection,delete_user)

# update a contact

def option_updcontact():
    y = 'no'
    
    print("\n List of Contacts: ")
    select_contacts = "SELECT * FROM contacts"
    contacts = execute_read_query(connection, select_contacts)
    for cont in contacts:
        print(cont[0],cont[1],cont[2],cont[3])

    upd_id = int(input("Enter contact ID:\n"))
    upd_details = input("Enter new Contact Details: \n")
    upd_phone = input('Enter new Phone Number in format XXX-XXX-XXXX : \n')
    response = input("Do you want to update Creation Date:   Yes / No \n")
    
    # asks user if they want to update date aswell 

    if response == ('Yes' or 'yes'):
        upd_date = input("Enter new date in format: (Y/M/D) XXXX-XX-XX \n")
        y = 'yes'

    # created 2 if statments, one for no date, the other with date

    if y == 'no':
        upd_contacts_query = """
        UPDATE contacts
        SET contactDetails = '%s', phoneNum = '%s'
        WHERE id = %s """ % (upd_details, upd_phone, upd_id)
        execute_query(connection,upd_contacts_query)
    if y == 'yes':
        upd_contacts_query = """
        UPDATE contacts
        SET contactDetails = '%s', phoneNum = '%s', creationDate = '%s'
        WHERE id = %s """ % (upd_details,upd_phone, upd_date, upd_id)
        execute_query(connection,upd_contacts_query)

# output contacts by alphabetical order

def option_alpha():
    contacts_alpha = "SELECT * FROM contacts ORDER BY contactDetails ASC;"
    contacts = execute_read_query(connection, contacts_alpha)
    for cont in contacts:
        print(cont[0],cont[1],cont[2])

# output contacts by creation date

def option_date():

    # tells the DB to select all from "contacts" and order it by the Date

    contacts_date = "SELECT * FROM contacts ORDER BY creationDate;"
    contacts = execute_read_query(connection, contacts_date)
    for cont in contacts:
        print(cont[0],cont[1],cont[2])

# out all contacts

def option_all():

    # this command tells the database to select all contacts from the table

    contacts_all = "SELECT * FROM contacts"
    contacts = execute_read_query(connection, contacts_all)
    for cont in contacts:
        print(cont[0],cont[1],cont[2])
    
# Creating the menu

def menu():
    x = 'continue'

    # Created a while loop for the menu
    # it will not break unless the user selects Q
    # which will change the variable x to 'break'

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

        # Whevener the user selects a option, it will first say that it was chosen
        # and then it will call onto the function

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
            option_alpha()

        if option == 'c':
            print('Option Output date order was choosen')
            option_date()

        if option == 'o':
            print('Output all was choosen')
            option_all()

        if option == 'q':
            print('Option Quit was choosen')
            x = 'break'


select_users = "SELECT * FROM contacts"
users = execute_read_query(connection, select_users)

menu()
         
#refrences
# Used code from Professor Otto code that was done during class
# used this in order to figure out how to order by alphabetical order in SQL https://learnsql.com/cookbook/how-to-order-alphabetically-in-sql/
# in order to order by alphabetical order, need to use ASC at the end

# Day 3
# modified the add contact function. So that when someone adds a new contact the id is not one that has already been used.
# i used the for loop that was in Professor ottos code and changed it in order to add the id number to a list. 
# when someone adds a contact the function looks at the last number in the list and adds +1 to it.
# Reminder: If the user deletes a contact. Figure out how to add a new contact with that id that was deleted.

#Day 4
#added all of the output functions ( alphabetical,creationdate, all)
#Reminder: Modify the outputs( add titles: "ID,NAME,DATE" above them)

#Day 5
# Added the phone number column and instead of asking for the first name and last name
# in one string and split it, so that it asks for first name first then the last name.
# Also did the same for creation date( year/month/day)
# When updating a contact i added an option to choose if they want to update the date aswell
