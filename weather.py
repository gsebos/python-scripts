
import requests
import os


def get_api_key_from_file():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f"{base_dir}/api_key_weather.txt","r") as f:
            for line in f:
                apikey=line
            return apikey.rstrip()

def get_weather_json(api_key:str,location:str,weather_now:bool):
    if weather_now:
        # current weather
        url = f"https://dataservice.accuweather.com/currentconditions/v1/{location}?apikey={api_key}"
    else:
        # next hour weather
        url =f"https://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location}?apikey={api_key}" 
    response = requests.get(url)
    json = response.json()
    return json


def make_widget(json):
    icons = [ "" , "" , "" , "" , "" , "" , "" , "󰅟" , "" , "" , "" , "" , "" , "" , "" , "󰼶" , "󰼴" , "󰼴" , "󰼶" , "" , "󰼴" ]
    for line in json:
        # Fahrenheit to Celcius formula C = 5/9 x (F-32)
        tempC = round(5/9 * (line['Temperature']['Value']-32),1)
        output = f"{tempC}C {icons[line['WeatherIcon'] - 1]}"
        return output

def main():
    location = "327336"
    api_key = get_api_key_from_file()
    json = get_weather_json(api_key,location,False)
    
    print(make_widget(json))


if __name__ == "__main__":
    main()
    
