import datetime
import time
import flask
from flask import jsonify
from flask import request, make_response
import mysql.connector
from mysql.connector import Error
import random
# setting up an application name
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# creates the connection with the AWS database by taking the user database name, username, password, and the host name
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

# Takes in the users query provided by the user and executes it by first connecting to the database and then executing the given query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# First taking the the query that instructs the database to return data to display then it returns the given data
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")




friends = []

def databasedata():
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "SELECT * FROM friend"
    dbdata = execute_read_query(connection, query)
    for row in dbdata:
        results = {"id":row[0], "fname":row[1], "lname":row[2]}
        car.append(results)
    return car
friends = databasedata()





# default url without any routing as GET request / returns the html code to the default url
@app.route("/", methods=["GET"])
def home(): 
    return "<h1> WELCOME TO OUR FIRST API! </h1>"

@app.route('/api/cars/all', methods=["GET"]) #endpoint to get all the cars
def api_all():
    return jsonify(friends)

@app.route('/api/cars',methods=['GET']) # endpoint to get a single car by id
def api_id():
    if 'id' in request.args: # only if an id is provided as an argument proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'
    
    results = [] # resulting car(s) to to return
    for car in friends:
        if car['id'] == id:
            results.append(car)
    return jsonify(results)

@app.route('/api/users',methods=['GET']) #api to get a user from teh db table in AWS b id as a JSON response
def api_users_id():
    if 'id' in request.args: # only if an id is provided as an argument proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'

    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    for user in rows:
        if user['id'] == id:
            results.append(user)
    return jsonify(results)



#----------- Movie Selector -----------

# Example to use POST as your method type, sending parameters as payload from POSTMAN (raw, JSON)
# Here using the POSTMAN, the user will send in the data to the endpoint then it will append that data to the friends list
# displaying the data in the url /post-example where it is visible
# This is not connected to the database so the data will reset back to the data prior to when the server was started
@app.route('/api/users/all', methods=['POST'])
def post_example():
    # request the data from the user in json format/ storing the data in the variable request_data 
    request_data = request.get_json()
    
    # These are the variables that will be used to insert data
    # The user must input the id, fname, and lname into POST in format ex: {"id": 1, "fname": example, "lname": example}
    newid = request_data['id'] # id
    newfname = request_data['fname'] # first name
    newlname = request_data['lname'] # last name

    friends.append({'id': newid, 'fname': newfname, 'lname' : newlname}) #adding a new user to the friend list

    # if I go check the /api/users/all route in the browser now, I should see this user added to the returned JSON list of users
    return 'POST REQUEST WORKED' # Returns the string 'POST REQUEST WORKED' In order to make sure it works

# This endpoint will delete the user from the list given the id in POSTMAN
@app.route('/api/users/delete', methods=['DELETE'])
def api_delete():
    # request the id from the user in order to start the process
    request_data = request.get_json()
    delid = request_data['id']
    # This for statement will go through the list and will find the user that has the same id 
    # then it will delete it from the list
    for x in friends:
        if delid == x['id']: # find if the id provided is the same as the id in the list
            friends.remove(x) 
    # returns 'DELETE REQUEST WORKED' in order to make sure it worked
    return 'DELETE REQUEST WORKED'

# endpoint that will update the information for the given user       
@app.route('/api/users/update',methods=['PUT'])
def api_update():
    # takes the id of the user then the fname and the lname
    request_data = request.get_json()
    updid = request_data['id'] # id of updated user
    updfname = request_data['fname'] # first name
    updlname = request_data['lname'] # last name

    # for loop that will check if the id matches then update the information with the informatin given
    # the y variable is there in order to count where the loop stops and measures where the user is inside of the list
    # so that it replaces the selected user poisiton with the new data
    y = 0
    for x in friends:
        if updid == x['id']:
            friends[y] = {'id': updid , 'fname': updfname, 'lname': updlname }
        y = y + 1 # increases y by 1
    return 'PUT REQUEST WORKED' # Returns PUST REQUEST WORKED to make sure it worked

# Adding a user to my database table named friend
@app.route('/api/db/adduser', methods=['POST'])
def adduser_db():
    # calls onto the function databasedate() in order to return data from the db
    databasedata()

    # request data from the user in order to input it into the database
    # here it requires the first name and last name
    # but if the lname is not provided it returns that the last name was not provided 
    # then it leaves the lname blank only having a fname for the user
    request_data = request.get_json()
    addfname = request_data["fname"]
    if "lname" in request_data:
        addlname = request_data["lname"]
    else: # if the user does not provide a last name
        print('Last Name was not provided')
        addlname = ""

    # creates the connection with the my AWS database
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    # Creates a query in order to inser the values given from the user into the friend table, the user id is not need since 
    # it has the auto incremenet option
    query = "INSERT INTO friend (firstname, lastname) VALUES ('"+addfname+"','"+addlname+"')"
    execute_query(connection, query)  # executes the query and places the values into the database
    return 'ADD USER REQUEST WORKED' # returns string to make sure it worked

# Delete a user from the databas named friend
@app.route('/api/deleteuser',methods=['DELETE'])
def deleteuser_db():
    # takes the data from the user and takes in the "id" field
    request_data = request.get_json()
    delid = request_data["id"]

    # Create a connection with the database by providing the address,name, and password
    # Also write the SQL code in order to give instructions to the database
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "DELETE FROM friend WHERE id = %s" % (delid) # deletes from the friend table given where the id matches
    execute_query(connection,query) 
    return 'DELETE USER REQUEST WORKED' # returns string to make sure it worked

# Update a user from the database named friend
@app.route('/api/updateuser',methods=['PUT'])
def updateuser_db():
    
    # Request data from the user in POSTMAN in order to update the information
    request_data = request.get_json()

    # requires the id, fname, and lname in order to update the information
    upid = request_data["id"]
    upfname = request_data['fname']
    uplname = request_data['lname']

    # creates the connection between my AWS db
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "UPDATE friend SET firstname = '"+upfname+"', lastname = '"+uplname+"' WHERE id = %s" % (upid) # will update the friend list values firstname,lastname, where the id matches the one chosen
    execute_query(connection,query) # executes query
    return 'UPDATE USER REQUEST WORKED' # returns string to make sure it works

# Adds a movie list to the given user
@app.route('/api/movies/add', methods=['POST'])
def usermovies():

    # request data given by the user from POSTMAN
    request_data = request.get_json()

    # Requires the friend id / user id to be given 
    # then it allows the users to be input the movies that the want to add all the way up to 10
    # if not all movies are provided then it fill the rest with 'none' instead of blank
    fid = request_data['fid']
    if 'movie1' in request_data:
        movie1 = request_data['movie1']
    else:
        movie1 = "none"
    if "movie2" in request_data:
        movie2 = request_data["movie2"]
    else:
        movie2 = 'none'
    if "movie3" in request_data:
        movie3 = request_data['movie3']
    else:
        movie3 = 'none'
    if "movie4" in request_data:
        movie4 = request_data['movie4']
    else:
        movie4 = 'none'
    if "movie5" in request_data:
        movie5 = request_data['movie5']
    else:
        movie5 = 'none'
    if "movie6" in request_data:
        movie6 = request_data['movie6']
    else:
        movie6 = 'none'
    if "movie7" in request_data:
        movie7 = request_data['movie7']
    else:
        movie7 = 'none'
    if "movie8" in request_data:
        movie8 = request_data['movie8']
    else:
        movie8 = 'none'
    if "movie9" in request_data:
        movie9 = request_data['movie9']
    else:
        movie9 = 'none'
    if "movie10" in request_data:
        movie10 = request_data['movie10']
    else:
        movie10 = 'none'
    
    # creates a connection between the AWS db
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

    # A query in order to insert the movies for the friendid into the table movielist
    query = "INSERT INTO movielist (movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9, movie10,friendid) VALUES ('"+movie1+"','"+movie2+"','"+movie3+"','"+movie4+"','"+movie5+"','"+movie6+"','"+movie7+"','"+movie8+"','"+movie9+"','"+movie10+"',%s)" % (fid)
    execute_query(connection,query) # executes the query
    return 'MOVIE LIST REQUEST WORKED' # returns string if it worked

# Displays users and their coresponding movielist
@app.route('/api/movies/all', methods=['GET'])
def show_movies():

    # first creates the connection between the aws database 
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

    # fetches the data from the database and returns it in rows.
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM movielist"
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    # for loop in order to append each row to the list 'results' then it returns the returns to the 
    # endpoint /api/movies/all and displays the data when you type the url
    for user in rows:
        results.append(user)

    return jsonify(results) # returns data to url

# Displays a selected users movielist
@app.route('/api/movies',methods=['GET'])
def user_movies():

    # checks if an id was provided if not it returns an error and tells the user that no id was provided
    if 'id' in request.args: # only if an id is provided as an argument proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'
    # creates a connection to the AWS db
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

    # fetches the data using the query 'sql' in order to select everything from the movielist
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM movielist" # selects all the data from the table movielist
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = [] # table to hold data

    # for loop that checks the data rows to first match the id then it appends that user to the results liust
    for user in rows:
        if user['friendid'] == id:
            results.append(user) # appends data to list
    return jsonify(results) # returns the specified user data

# Adds the users that were selected choose at random to a database
# this endpoint will give the user to option to select the users that want thier movies
# to be selected 
@app.route('/api/movies/insert', methods=['POST'])
def norm_str():
    ids = [] # list for the ids provided

    # request data needed for the query
    request_data = request.get_json()
    num_users = request_data['num'] # number of user that are going to be used
    """
    if "user1" in request_data:
        User1 = request_data['user1']
    if "user2" in request_data:
        User2 = request_data['user2']
    if "user3" in request_data:
        User3 = request_data['user3']
    """

    # while loop that uses the number given (which is the amount of user that are going to be used)
    # then it will run that loop for that many users
    # the loop will append the user id that is going to be provided by the person that inserts the data
    # so for example if i want to only use to users i would {"num": 2, "user1": 1, "user2": 4} <-- the number that corresponds to the user(X) is going to be 
    # the id that is given to the user in the first table 

    x = 1
    while x <= num_users:
        y = "user%s" % (x)
        if y in request_data:
            ids.append(request_data[y])
        x = x + 1

    norm_str = ""  # this string is going to turn eventually to the ids of the user --> id = [1,2,4]
    
    # converts the numbers from the list into string and creates a tuple in order to insert it into the query
    # this allows the us to insert the stirng of users into the database
    # the table that we will be using will be a single row/column that only contains the string of users
    # this data will be used in the next endpoint
    x = 1
    while x <= num_users:
        if (num_users - x != 0):
            num = "%s," % (str(ids[x - 1]))
            norm_str += num
        else: 
            norm_str += str(ids[x-1])
        x = x + 1
    
    # creates the connection with the AWS database
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "UPDATE selected SET list = '%s' WHERE id = 1" % (norm_str)  # this query will update the 1 row/column to the string of users that was selected by the users for the movies
    execute_query(connection,query) 

    return 'INSERT USERS INTO DATABASE WORKED' # makes sure the users were inserted to the db

# Takes the data from the table and picks a random movie from the given users
@app.route('/api/movies/randompick', methods=['GET'])
def random_movie():
    """
    ids = []
    request_data = request.get_json()
    print(request_data)
    num_users = request_data['num']
    if "user1" in request_data:
        User1 = request_data['user1']
    if "user2" in request_data:
        User2 = request_data['user2']
    if "user3" in request_data:
        User3 = request_data['user3']
    x = 1
    while x <= num_users:
        print(x)
        y = "user%s" % (x)
        print(y)
        if y in request_data:
            ids.append(request_data[y])
        x = x + 1
    norm_str = ""  #id = [1,2,4]
    x = 1
    while x <= num_users:
        if (num_users - x != 0):
            num = "%s," % (str(ids[x - 1]))
            norm_str += num
        else: 
            norm_str += str(ids[x])
        x = x + 1
    """
    # first creates the connection for the AWS db
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

    # this query will select that data that was inserted in the in the endpoint prior /api/movies/insert
    query = "SELECT * FROM selected WHERE id = 1"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    norm_strs = rows[0]['list']

    # once we recieve the string of ids that was provided by the insert endpoint 
    # we insert that string into this query that will return the data from those selected users
    query = "SELECT * FROM movielist WHERE friendid in (%s)" % (norm_strs) # inserts the string of user into the query
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    movies = []

    # this for loop will select the movies from the selected user and insert them into them into a list called movies
    # if the it says 'none' then it will not be inserted into the list
    for x in rows:
        y = 1
        while y <= 10:
            movie = "movie%s" % (y)
            if x[movie] != "none":
                movies.append(x[movie])
            y = y + 1
    
    # this variable uses the random module to select a random number and then select a movies
    # first it takes the length of the list of movies and sets the range for number that can be selected
    # after it selects the number in the range provided it will use that number and insert itself in the movies[x]
    # to select the movie and the variable randompick will take the movie
    randompick =  movies[random.randint(0,(len(movies)- 1))]
    return randompick # returns the movies that was randomly picked. it can be used again if the url is just refreshed





app.run()

# Day 1 -----------------------------------------------------------------------------------------
# Created some end points for the api (creating a user, deleting a user, updating a user)
# I also created some endpoints that would create the user in the database and the other CRUDs 
# Made sure that the database worked good with the code and i didn't receive any errors
# the errors that I did get, i made sure to fix them right away.
# Update function in browser (not database):
# decided to create a for statement that will find the matching id that was provided by the user
# and update the information once the for loop finds that specified user. I also did the same
# for the delete user.
# Day 2 -----------------------------------------------------------------------------------------
# Added more endpoints to the code. the firsts ones being the update and delete for the database 
# For the delete endpoint they must provide the id of the user as well for the update one
# Created the the database for the movies, created 10 fields for the movies and 1 for the friendid
# the friend ID must be provided. The first route for the movies will be to add movies to the user
# created POST that will ask for the friendid and then the movies that they want to add. if they 
# don't provided names for the rest of the fields (ex. 1-3: movies, 4-10: no movies provided)
# then it will fill the fields with "none". I then created two more 'GET' endpoints that will 
# display the infomration from the table in json form on the web. the first one will display
# all of the information from the table. Then the second 'GET' will show a specified user movies
# only. Lastly I created the endpoints to select a random movie from the database. First I created
# a 'POST' endpoint that will ask for the 'friendid' of the users that were selected. So if users
# (1,2,4) were selected then it would be {"user1": 1, "user2": 2, "user3": 4} this will be sent
# through postman. After that I created some loops that would create a list with the users ID only
# then it would convert it into a string ("1,2,4"). After that the string will be sent to the 
# database in a one line database. The last endpoint is where is the random movie is picked
# When you enter "127.0.0.1:5000/api/movies/randompick" it will display the result. This works
# by firstly taking the single string data ("1,2,4") from the database and inserting into a query
# that asks the table with all of the movies to "SELECT * from movieslist where ID in (1,2,4)' 
# returning only the rows from those with the ids specified. After that I created a loop that 
# run through all of the rows provided and insert all of the movies that were selcted into a 
# list. I used an if statement in order to not insert the "none" responses for the fields that 
# have no movies. I also imported the random module in order to select a random number from 
# the range of 0 and the length of the list with the movies
# Day 3 -----------------------------------------------------------------------------------------
# removed unecessary code that didn't affect the rest of the code
# then i added the comments to describe the code and make it easier to understand why i did
# certain things. Changed the name of certain list in order for them to make more sense, since they
# were used for different things before
# -----------------------------------------------------------------------------------------------
