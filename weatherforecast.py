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
    print("Temperature:%4.2d celcius"% (temp - 273.15))
    print("Wind Speed:%4.2d m/s"%wind_speed)
    print("Description : ",description)
    print("Latitude :%4.2d degrees"%latitude)
    print("Longitude :%4.2d degrees"%longitude)
