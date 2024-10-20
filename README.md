# Indian Cities Weather App

This Flask-based web application provides current weather information and historical temperature data for major Indian cities.

## Features

- Display current weather conditions for selected Indian cities
- Show hourly weather forecast
- Store and display historical temperature data
- Calculate average, maximum, and minimum temperatures for each city

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
   
   git clone https://github.com/Bhaskar9143/weatherforecast-main.git
   cd weatherforecast-main
   

2. Create a virtual environment (optional but recommended):
   
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   

3. Install the required packages:
   
   pip install -r requirements.txt
   

4. Set up your OpenWeatherMap API key:
   - Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/)
   - Get your API key from your account dashboard
   - Replace the API_KEY variable in weather.py with your actual API key

## Usage

1. Run the Flask application:
   
   python weather.py
   

2. Open a web browser and navigate to http://localhost:5000

3. Select a city from the dropdown menu to view its weather information

## Project Structure

- weather.py: Main Flask application file
- templates/index.html: HTML template for the web interface
- weather.db: SQLite database file for storing historical temperature data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

