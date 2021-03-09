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



connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "cis3368")

dob = datetime.datetime(2000,1,20)
str_dob = dob.date().isoformat()
query = "INSERT INTO users (firstname, lastname, dateofbirth) VALUES ('jane2','doe2','2002-02-02')"
execute_query(connection, query)  

select_users = "SELECT * FROM users"
users = execute_read_query(connection, select_users)

for user in users:
    dob = user[3]
    today = date.today()
    dayinterval = today - dob
    print(user[1] + " is " + str(dayinterval.days) + " days old")

