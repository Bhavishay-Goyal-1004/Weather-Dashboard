# Weather + Air Quality CLI Dashboard

Week 02 Project — FORGETRACK 2026 Tech Track

A Python command-line application that fetches real-time weather and air quality data using the OpenWeatherMap API.

---

# Features

* Fetch current weather data for any city
* Display:

  * Temperature
  * Feels Like Temperature
  * Humidity
  * Wind Speed
  * Weather Condition
* Fetch Air Quality Index (AQI)
* Display AQI advisory messages
* Store last 5 searched cities in a JSON file
* View search history using `history` command
* Robust error handling for:

  * Invalid city names
  * Network issues
  * Missing API data
  * API failures

---

# Project Structure

weather-dashboard/

├── main.py

├── history.json

├── .env

├── .env.example

├── .gitignore

├── requirements.txt

└── README.md

---

# Installation

## Clone the Repository

```bash
git clone <your_repository_link>
```

## Open Project Folder

```bash
cd weather-dashboard
```

## Install Required Libraries

```bash
pip install -r requirements.txt
```

---

# API Setup

1. Create a free account on OpenWeatherMap
2. Generate your API key
3. Create a `.env` file in the project folder
4. Add your API key like this:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

---

# Running the Program

Run the following command:

```bash
python main.py
```

---

# Example Usage

## Weather Search

```bash
Enter city name (or type 'history'): Pune
```

## Example Output

```bash
╔══════════════════════════════════════════════════════════════════════════════╗
║                              WEATHER DASHBOARD                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ City                 : Pune                                                  ║
║ Temperature          : 35.78°C                                               ║
║ Feels Like           : 36.32°C                                               ║
║ Humidity             : 32%                                                   ║
║ Wind Speed           : 7.39 m/s                                              ║
║ Condition            : scattered clouds                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ AQI                  : 1                                                     ║
║ AQI Status           : Good                                                  ║
║ Advisory             : Air quality is satisfactory.                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# Search History

Type:

```bash
history
```

to view previously searched cities.

---

# Error Handling

This project handles:

* Invalid city names
* Internet connection failures
* API request timeouts
* Missing JSON fields
* Unexpected errors

without crashing the program.

---

# Learning Outcomes

This project helped practice:

* REST APIs
* JSON parsing
* Python dictionaries and lists
* File handling
* Exception handling
* Environment variables
* Working with real-world API data

---

# API Used

OpenWeatherMap API:
https://openweathermap.org/api

---

# Submission Requirements Covered

* Weather Data
* AQI Data
* Search History
* Error Handling
* `.env` Security
* `.env.example`
* GitHub Repository
* README Documentation

---

# Author

Bhavishay Goyal

