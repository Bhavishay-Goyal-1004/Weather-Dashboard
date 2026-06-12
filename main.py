import requests
import json
import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# Loading API key
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# AQI meanings
aqi_meaning={
    1:"Good",
    2:"Fair",
    3:"Moderate",
    4:"Poor",
    5:"Very Poor"}


# AQI advisory messages
aqi_advisory={
    1: "Air quality is satisfactory.",
    2: "Air quality is acceptable.",
    3: "Sensitive individuals should reduce outdoor activity.",
    4: "Avoid prolonged outdoor exertion.",
    5: "Stay indoors if possible."}

HISTORY_FILE="history.json"

# ---------------- HISTORY FUNCTIONS ---------------- #

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_history(city,weather_data):
    history = load_history()

    history.append({
        "city" : city,
        "weather" : weather_data
    })

    # Keep only last 5 searches
    history = history[-5:]

    with open(HISTORY_FILE, "w") as file:
       json.dump(history,file,indent=4)

def show_history():
    history=load_history()

    if not history:
        print("No search history found!")
        return

    print("\n===== SEARCH HISTORY =====")

    for item in history:
        print(f"\nCity: {item['city']}")
        print(f"Temperature: {item['weather']['temp']}°C")
        print(f"Condition: {item['weather']['condition']}")

# ---------------- WEATHER FUNCTION ---------------- #

def get_weather(city):

    # Weather API
    url=(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")

    try: 
        response = requests.get(url,timeout=10)

        if response.status_code != 200:
            print(f"Error {response.status_code}: Invalid city name or API issue.")
            return

        data = response.json()

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        # AQI API
        aqi_url = (f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}")

        aqi_response = requests.get(aqi_url,timeout=10)

        aqi_data = aqi_response.json()

        aqi = aqi_data["list"][0]["main"]["aqi"]

        print("\n" + "╔" + "═" * 73 + "╗")
        print(f"║{'WEATHER DASHBOARD':^73}║")
        print("╠" + "═" * 73 + "╣")

        print(f"║ {'City':<15} : {city.title():<53} ║")
        print(f"║ {'Temperature':<15} : {str(temp) + '°C':<53} ║")
        print(f"║ {'Feels Like':<15} : {str(feels_like) + '°C':<53} ║")
        print(f"║ {'Humidity':<15} : {str(humidity) + '%':<53} ║")
        print(f"║ {'Wind Speed':<15} : {str(wind_speed) + ' m/s':<53} ║")
        print(f"║ {'Condition':<15} : {description:<53} ║")

        print("╠" + "═" * 73 + "╣")

        print(f"║ {'AQI':<15} : {str(aqi):<53} ║")
        print(f"║ {'AQI Status':<15} : {aqi_meaning.get(aqi):<53} ║")
        print(f"║ {'Advisory':<15} : {aqi_advisory.get(aqi):<53} ║")

        print("╚" + "═" * 73 + "╝")
        
        # Saving history 
        weather_data = {
            "temp" : temp,
            "condition" : description
            }
        
        save_history(city, weather_data)

    # Handling exceptions

    except requests.exceptions.ConnectionError:
        print("No internet connection.")

    except requests.exceptions.Timeout:
        print("Request timed out.")

    except Exception as e:
        print(f"Something went wrong: {e}")

# ---------------- MAIN PROGRAM ---------------- #

def main():

    history=load_history()

    if history:
        print(f"Last searched city : {history[-1]['city']}\n")

    city = input("Enter city name (or history):")

    if city.lower()=="history":
        show_history()
    else:
        get_weather(city)

if __name__=="__main__":
    main()
    