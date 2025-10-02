import requests
import json
import os

class WeatherApp:
    def __init__(self):
        self.api_key = self.load_api_key()
    
    def load_api_key(self):
        """Load API key from file or ask user"""
        if os.path.exists("api_key.txt"):
            with open("api_key.txt", "r") as file:
                return file.read().strip()
        else:
            api_key = input("Enter your OpenWeatherMap API key: ").strip()
            if api_key and api_key != "YOUR_API_KEY_HERE":
                with open("api_key.txt", "w") as file:
                    file.write(api_key)
                return api_key
            else:
                print("\n❌ Please get a free API key from: https://openweathermap.org/api")
                print("1. Go to the website and sign up for free")
                print("2. Verify your email")
                print("3. Go to 'API Keys' tab and copy your key")
                return None
    
    def get_weather_by_city(self, city_name):
        """Get weather data by city name"""
        if not self.api_key:
            return None
            
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return data
            else:
                error_msg = data.get('message', 'Unknown error')
                print(f"❌ Error: {error_msg}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Request timeout. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Network connection error. Check your internet.")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_weather_by_coordinates(self, lat, lon):
        """Get weather by coordinates"""
        if not self.api_key:
            return None
            
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return data
            else:
                print(f"❌ Error: {data.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def display_weather(self, weather_data, location_type):
        """Display weather information"""
        if not weather_data:
            return
        
        city = weather_data['name']
        country = weather_data['sys']['country']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        description = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        
        print(f"\n{'='*50}")
        print(f"🌤️  Weather in {city}, {country} ({location_type})")
        print(f"{'='*50}")
        print(f"🌡️  Temperature: {temp}°C")
        print(f"🤔 Feels like: {feels_like}°C")
        print(f"☁️  Conditions: {description.title()}")
        print(f"💧 Humidity: {humidity}%")
        print(f"📊 Pressure: {pressure} hPa")
        print(f"💨 Wind Speed: {wind_speed} m/s")
        print(f"{'='*50}")
    
    def run(self):
        """Main application loop"""
        if not self.api_key:
            return
        
        print("\n" + "="*50)
        print("🌤️  Welcome to Weather App!")
        print("="*50)
        
        while True:
            print("\n📝 Search Options:")
            print("1. From City Name")
            print("2. From Coordinates") 
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                city = input("Enter city name: ").strip()
                if city:
                    weather_data = self.get_weather_by_city(city)
                    if weather_data:
                        self.display_weather(weather_data, "City Search")
                else:
                    print("❌ Please enter a valid city name!")
            
            elif choice == "2":
                try:
                    lat = float(input("Enter latitude: "))
                    lon = float(input("Enter longitude: "))
                    weather_data = self.get_weather_by_coordinates(lat, lon)
                    if weather_data:
                        self.display_weather(weather_data, "Coordinate Search")
                except ValueError:
                    print("❌ Please enter valid coordinates!")
            
            elif choice == "3":
                print("👋 Thank you for using Weather App! Goodbye!")
                break
            
            else:
                print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    app = WeatherApp()
    app.run()