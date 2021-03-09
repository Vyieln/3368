import requests
import json
import keys
#import hello


city = input('Enter city name: ')
state = input('Enter state code: ')


# weather_response = requests.get("api.openweathermap.org/data/2.5/weather?q=%s,%s&appid=%s" % (city,state,keys.Keys.getweatherapikey())) #put your own api key in this static function in keys.py
link = "http://api.openweathermap.org/data/2.5/weather?q=London,uk&units=imperial&appid=%s" % (keys.Keys.getweatherapikey())
weather_response = requests.get(link)
print(weather_response)

json_weather_response = weather_response.json()
print(json_weather_response)

print("------------------------------------")
print('City: %s \nCountry: %s'% (json_weather_response['name'],json_weather_response['sys']['country']))
print('Weather: %s \n    description: %s' % (json_weather_response['weather'][0]['main'],json_weather_response['weather'][0]['description']))
print('Temperature (Fahrenheit): %s\n    Min:%s\n    Max:%s' % (json_weather_response['main']['temp'],json_weather_response['main']['temp_min'],json_weather_response['main']['temp_max']))
print('Wind: %s mph' % json_weather_response['wind']['speed'])
print("------------------------------------")


onnection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

query = "INSERT INTO weather (city,country,weather,disc,temp,wind) VALUES ('%s','%s','%s','%s','%s','%s')" % ()
execute_query(connection, query)


# Day 1 --------------------------------------------------------------------------------------------------------------
#   Setup the user inputs for city and state, so that the user can input those two variables and choose on their own
# Then I created the request to get information from the api link using the key i got from the openweathermap website.
# After I got the information I had to convert it into json format and then parse it in order to read it better
# After that I created the print statements for City,Country,Weather,desc,Temp, and Wind
# Finally i created the format for the connection for the database and the query code.
# --------------------------------------------------------------------------------------------------------------------