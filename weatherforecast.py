import requests
import proxy
 #Contributed by : Dean Sebial
 #city.list.json.gz is a requirement for this file 
API_key = "d90447162b645108c9ffae4cd1442ee6"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


if __name__ == "__main__":
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

#classified for compatibility - Lily
class Weather():
    def __init__():
        pass

    def fetch(city_name,units,p):
        url = base_url + "appid=" + API_key + "&q=" + city_name

        if p == True:
            print("USING PROXY")
            weather_data = requests.get(url, proxies=proxy.proxies).json()
        else:
            weather_data = requests.get(url).json()

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
        temp_c = int(temp) - 273.15
        temp_f = (temp_c*1.8)+32

        if "metric"==units: 
            output = (
                f'City : {city_name}'
                f'\nTemperature: {temp_c:.2f} C'
                f'\nWind Speed : {wind_speed:.2f} m/s'
                f'\nDescription : {description}'
                f'\nLatitude : {latitude}'
                f'\nLongitude : {longitude}'
            )
        elif "imperial"==units:
            output = (
                f'City : {city_name}'
                f'\nTemperature(Celsius) : {temp_f:.2f} F'
                f'\nWind Speed : {(wind_speed*2.23694):.2f} mph'
                f'\nDescription : {description}'
                f'\nLatitude : {latitude}'
                f'\nLongitude : {longitude}'
            )
        else:
            output = "UNIT ERROR"
        return output