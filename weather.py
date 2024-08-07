import requests
import os
import argparse


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
    print(json)
    return json


def make_widget(json,now):
    icons = [ "" , "" , "" , "" , "" , "" , "" , "󰅟" , "" , "" , "" , "" , "" , "" , "" , "󰼶" , "󰼴" , "󰼴" , "󰼶" , "" , "󰼴" ]
    for line in json:
        if now:
            tempC = line['Temperature']['Metric']['Value']
        else:
            # The next hour forecast json object only provides temps in Fahrenheit
            # Fahrenheit to Celcius formula C = 5/9 x (F-32)
            tempC = round(5/9 * (line['Temperature']['Value']-32),1)

        output = f"{tempC}C {icons[line['WeatherIcon'] - 1]}"
        return output

def main():
    parser = argparse.ArgumentParser(description="Gets the next hour forecast (default) or the current forecast")
    parser.add_argument("--now",action="store_true")
    parser.add_argument("--next-hour",dest="now", action="store_false")
    parser.add_argument("--location", type=str,default="327336")
    # Default to next hour forecast
    parser.set_defaults(now = False)
    args = parser.parse_args()
    
    api_key = get_api_key_from_file()
    location = args.location
    now = args.now
    
    json = get_weather_json(api_key,location,now)
    
    print(make_widget(json,now))


if __name__ == "__main__":
    main()
    
