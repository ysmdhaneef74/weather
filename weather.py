from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database (or replace with your preferred database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Replace with your actual API key
API_KEY = 'your_api_key'  # Make sure to replace this with your actual API key

# List of Indian cities with their coordinates
cities = {
    'Delhi': (28.6139, 77.2090),
    'Mumbai': (19.0760, 72.8777),
    'Bengaluru': (12.9716, 77.5946),
    'Chennai': (13.0827, 80.2707),
    'Kolkata': (22.5726, 88.3639),
    'Hyderabad': (17.3850, 78.4867),
}

# Create a WeatherData model to store temperature information
class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)  # Store temperature in Celsius
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<WeatherData {self.city} - {self.temperature}°C at {self.recorded_at}>'

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    if request.method == 'POST':
        selected_city = request.form.get('city')
        if selected_city:
            lat, lon = cities[selected_city]
            url = f"http://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temp_celsius = data['current']['temp'] - 273.15  # Convert from Kelvin to Celsius

                # Save the current temperature in the database
                new_entry = WeatherData(city=selected_city, temperature=temp_celsius)
                db.session.add(new_entry)
                db.session.commit()

                # Retrieve historical temperature data from the database for this city
                city_temperatures = WeatherData.query.filter_by(city=selected_city).all()

                # Calculate the average, max, and min temperatures
                temperatures = [entry.temperature for entry in city_temperatures]
                avg_temp = round(sum(temperatures) / len(temperatures), 2) if temperatures else None
                max_temp = max(temperatures) if temperatures else None
                min_temp = min(temperatures) if temperatures else None

                weather_data[selected_city] = {
                    'current': data['current'],
                    'hourly': data['hourly'],
                    'avg_temp': avg_temp,
                    'max_temp': max_temp,
                    'min_temp': min_temp
                }
            else:
                weather_data[selected_city] = {'error': 'Failed to fetch weather data.'}

    return render_template('index.html', weather_data=weather_data, cities=cities)

if __name__ == '__main__':
    app.run(debug=True)
