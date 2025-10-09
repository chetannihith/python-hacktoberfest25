import requests

def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            print(f"Weather in {city}:")
            print(f"Temperature: {current['temp_C']}°C")
            print(f"Feels Like: {current['FeelsLikeC']}°C")
            print(f"Description: {current['weatherDesc'][0]['value']}")
            print(f"Humidity: {current['humidity']}%")
            print(f"Wind Speed: {current['windspeedKmph']} km/h")
        else:
            print("City not found!")
    except Exception as e:
        print("Error fetching weather information:", str(e))

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)
