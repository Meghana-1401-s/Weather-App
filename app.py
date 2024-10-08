from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your actual OpenWeatherMap API key
API_KEY = 'Your_API_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    air_quality_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        
        # URL to fetch weather data (temperature, humidity, pressure)
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        weather_response = requests.get(weather_url)
        
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            # Extract latitude and longitude for Air Quality Index request
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            
            # URL to fetch air quality index
            air_quality_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
            air_quality_response = requests.get(air_quality_url)
            
            if air_quality_response.status_code == 200:
                air_quality_data = air_quality_response.json()
                # Extract AQI from the response
                air_quality_index = air_quality_data['list'][0]['main']['aqi']
                weather_data['main']['air_quality_index'] = air_quality_index
            else:
                weather_data['main']['air_quality_index'] = "Not available"
        else:
            weather_data = {"error": "City not found."}
    
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
