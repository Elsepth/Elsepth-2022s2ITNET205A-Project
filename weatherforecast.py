import requests
 #Contributed by : Dean Sebial
 #city.list.json.gz is a requirement for this file 
API_key = "d90447162b645108c9ffae4cd1442ee6"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 

while True:
    city_name = input("Enter City Name : ")
    if city_name == "quit" or city_name == "q":
        break
    Final_url = base_url + "appid=" + API_key + "&q=" + city_name
    weather_data = requests.get(Final_url).json()
# Accessing Temperature, temperature resides in main and its key is temp 
    temp = weather_data['main']['temp']
# Accessing wind speed, it resides in wind and its key is speed
    wind_speed = weather_data['wind']['speed']
# Accessing Description, it resides in weather and its key is description 
    description = weather_data['weather'][0]['description']
# Accessing Latitude, it resides in coord and its key is lat 
    latitude = weather_data['coord']['lat']
# Accessing Longitude, it resides in coord and its key is lon 
    longitude = weather_data['coord']['lon']
# Printing Data
    print('\nTemperature(Celsius) : ',(temp - 273.15))
    print('\nWind Speed (Meter per Second): ',wind_speed)
    print('\nDescription : ',description)
    print('\nLatitude : ',latitude)
    print('\nLongitude : ',longitude)

