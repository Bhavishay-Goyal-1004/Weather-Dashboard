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

    print("\n" + "╔" + "═" * 55 + "╗")
    print(f"║{'SEARCH HISTORY':^55}║")
    
    for item in history:
        print("╠" + "═" * 55 + "╣")

        print(f"║ {'City':<15}: {item['city']:<36} ║")
        print(f"║ {'Temperature':<15}: {str(item['weather']['temperature']) + '°C':<36} ║")
        print(f"║ {'Humidity':<15}: {str(item['weather']['humidity']) + '%':<36} ║")
        print(f"║ {'Wind Speed':<15}: {str(round(item['weather']['wind_speed'],1)) + ' km/h':<36} ║")
        print(f"║ {'AQI':<15}: {item['weather']['aqi']:<36} ║")
        print(f"║ {'Condition':<15}: {item['weather']['condition']:<36} ║")

    print("╚" + "═" * 55 + "╝")

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

        temp = data.get("main", {}).get("temp")
        feels_like = data.get("main", {}).get("feels_like")
        humidity = data.get("main", {}).get("humidity")
        wind_speed = round((data.get("wind", {}).get("speed")) * 3.6, 1)
        condition = data.get("weather", [{}])[0].get("description")

        lat = data.get("coord", {}).get("lat")
        lon = data.get("coord", {}).get("lon")

        # AQI API
        aqi_url = (f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}")

        aqi_response = requests.get(aqi_url,timeout=10)

        aqi_data = aqi_response.json()

        aqi = aqi_data.get("list", [{}])[0].get("main", {}).get("aqi")

        print("\n" + "╔" + "═" * 73 + "╗")
        print(f"║{'WEATHER DASHBOARD':^73}║")
        print("╠" + "═" * 73 + "╣")

        print(f"║ {'City':<15} : {city.title():<53} ║")
        print(f"║ {'Temperature':<15} : {str(temp) + '°C':<53} ║")
        print(f"║ {'Feels_like':<15} : {str(feels_like) + '°C':<53} ║")
        print(f"║ {'Humidity':<15} : {str(humidity) + '%':<53} ║")
        print(f"║ {'Wind Speed':<15} : {str(wind_speed) + ' km/hr':<53} ║")
        print(f"║ {'Condition':<15} : {condition:<53} ║")
        print(f"║ {'AQI':<15} : {str(aqi):<53} ║")
        print(f"║ {'AQI Status':<15} : {aqi_meaning.get(aqi):<53} ║")
        print(f"║ {'Advisory':<15} : {aqi_advisory.get(aqi):<53} ║")

        print("╚" + "═" * 73 + "╝")
        
        # Saving history 
        weather_data = {
            "temperature" : temp,
            "humidity" : humidity,
            "wind_speed" : wind_speed,
            "aqi" : aqi,
            "condition" : condition
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
    while True:
        print("=======================Weather Dashboard======================")
        print("1. Check Weather.")
        print("2. See History")
        print("3. Exit")

        try:
            ch = int(input("Enter Choice: "))

        except ValueError:
            print("\nPlease enter a valid number!")
            continue
            

        history=load_history()

        '''if not history:
            print("\nNo previous search history found.\n")'''
            
        if (ch==1):
            if history:
                print(f"Last searched city : {history[-1]['city']}\n")
            else:
                print("\nNo previous search history found.\n")
            city = input("Enter city name: ")
            if not city.strip():
                print("\nCity name cannot be empty!")
                continue
            get_weather(city)
        elif (ch==2):
            show_history()
        elif (ch==3):
            print("\nThank you for using Weather Dashboard!")
            return
        else:
            print("Invalid Choice!")


if __name__=="__main__":
    main()
    