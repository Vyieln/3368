import requests
import json
import keys
import hello
import datetime

# creating a connection with the database. Using hello.create_connection since the code is in another file
connection = hello.create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

# in this function we will create a variable that contains the SQL code which will be sent to my database using the execute_query
def store():
    query = "INSERT INTO results (city,country,weather,descr,temp,wind,dates) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (city, country, weather, desc, temp, wind,time)
    hello.execute_query(connection, query)

# In this function the user will be able to delete a location
# the menu of location will first pop up and then the user can choose the location by entering the id
def delete():
    results_id_user = int(input('Enter contact ID \n'))
    delete_user = "DELETE FROM results WHERE id = %s" % (results_id_user)
    hello.execute_query(connection,delete_user)

# Here the results of the database will be displayed
def display():
    results_dis = "SELECT * FROM results;"
    results = hello.execute_read_query(connection, results_dis)
    for res in results:
        ins = "%s - City: %s - Country: %s - Weather: %s - Description: %s - Temperature: %s f - Wind Speed: %s mph Date: %s" % (res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7])
        print(ins)
    print("------------------------------------")

# Here the user will be able to see the results but they
# will be in order by the temperature field
def tempframe():
    results_temp = "SELECT * FROM results ORDER BY temp;"
    temp_result = hello.execute_read_query(connection, results_temp)
    for temps in temp_result:
        inst = "%s - City: %s - Country: %s - Weather: %s - Description: %s - Temperature: %s f - Wind Speed: %s mph" % (temps[0],temps[1],temps[2],temps[3],temps[4],temps[5],temps[6])
        print(inst)
    print("------------------------------------")

# In windspeed() the user will be able to see the results from the database 
# but they will be displayed in order by wind
def windspeed():
    results_wind = "SELECT * FROM results ORDER BY wind;"
    wind_result = hello.execute_read_query(connection, results_wind)
    for winds in wind_result:
        inst = "%s - City: %s - Country: %s - Weather: %s - Description: %s - Temperature: %s f - Wind Speed: %s mph" % (winds[0],winds[1],winds[2],winds[3],winds[4],winds[5],winds[6])
        print(inst)
    print("------------------------------------")

# Here in this function it will display our menu. It is a while function which will go on until x is changed.
# x will only change if the user chooses the option q which will make x = 'exit'
# If an option is choosen it will say that it was chosen and then it will call the function
def menu():

    x = 'continue'

    while x == 'continue':
        print('a - Store Data in DB')
        print('b - Delete a location')
        print('c - Display data')
        print('d - Sort by Temperature')
        print('e - Sort by Wind Speed')
        print('q - exit')
        print("------------------------------------")
        option = input('Enter option: ')

        if option.lower() == 'a':
            print('Option a was chosen')
            print("------------------------------------")
            store()
        if option.lower() == 'b':
            print('Option b was chosen')
            print("------------------------------------")
            display()
            delete()
        if option.lower() == 'c':
            print('Option c was chosen')
            print("------------------------------------")
            display()
        if option.lower() == 'd':
            print('Option d was chosen')
            print("------------------------------------")
            tempframe()
        if option.lower() == 'e':
            print('Option e was chosen')
            print("------------------------------------")
            windspeed()
        if option.lower() == 'q':
            x = 'exit'

# Allowing the user to input the city and country of their location        
cityin = input('Enter city name (ex: London): ')
countryin = input('Enter country code(ex: uk): ')


# creating the api link, using the inputs from the user and inserting them inside of the api link using %s
link = "http://api.openweathermap.org/data/2.5/weather?q=%s,%s&units=imperial&appid=%s" % (cityin, countryin.lower(), keys.Keys.getweatherapikey())

# here we recevie the data from the api and convert it into json form
weather_response = requests.get(link)
json_weather_response = weather_response.json()
print(json_weather_response)
# creating variables for every category that we are going to use city, country, weather, etc...
# makes it much easier than entering json_weather_respon[] inside of the print statement
city = json_weather_response['name']
country = json_weather_response['sys']['country']
weather = json_weather_response['weather'][0]['main']
desc = json_weather_response['weather'][0]['description']
temp = json_weather_response['main']['temp']
temp_min = json_weather_response['main']['temp_min']
temp_max = json_weather_response['main']['temp_max']
wind = json_weather_response['wind']['speed']
time = datetime.datetime.now()
# printing out the results 
print("------------------------------------")
print('City: %s \nCountry: %s'% (city, country))
print('Weather: %s \n    description: %s' % (weather, desc))
print('Temperature (Fahrenheit): %s\n    Min:%s\n    Max:%s' % (temp, temp_min, temp_max))
print('Wind: %s mph' % (wind))
print(time)
print("------------------------------------")

# calling the menu
menu()


# Day 1 --------------------------------------------------------------------------------------------------------------
#   Setup the user inputs for city and state, so that the user can input those two variables and choose on their own
# Then I created the request to get information from the api link using the key i got from the openweathermap website.
# After I got the information I had to convert it into json format and then parse it in order to read it better
# After that I created the print statements for City,Country,Weather,desc,Temp, and Wind
# Finally i created the format for the connection for the database and the query code.
# --------------------------------------------------------------------------------------------------------------------
# Day 2 -------------------------------------------------------------------------------------------------------------- 
# Created the table in my AWS database 
# Created the menu that will come up in the command line when the program starts
# --------------------------------------------------------------------------------------------------------------------
# Day 3 --------------------------------------------------------------------------------------------------------------
# Finised up the def for storing the data in the db, deleting a location if needed, displaying data, displaying data
# by temp, and displaying data by wind speed. Made sure that the connection was working from the hello.py file.
# made variables instead of calling using "json_weather_response[][]", made it much easier and cleaner/readable
# cleaned up the output by adding lines that seperates each section
# Day 4 --------------------------------------------------------------------------------------------------------------
# Finally made sure to add the user inputs like "cityin" and "countryin" into the api link. Since i was using a 
# pre-made link instead of "%s"
# When I was testing the code, i ran into the error "TypeError: 'float' object is not callable" and wasn't sure what was
# causing it. Until i realized that for the definiton "def temp():" had the same name as my variable "temp" that 
# contained the temperature infomation from the json data. So i changed the name to "tempframe" and "windspeed"
# --------------------------------------------------------------------------------------------------------------------
# Day 5 --------------------------------------------------------------------------------------------------------------
# Adding comments
# also added a date to the database so that the user can tell when the location was called and what the weather was 
# that day
# --------------------------------------------------------------------------------------------------------------------