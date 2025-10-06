from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

API_KEY = os.environ.get('WEATHER_API_KEY', '07c76e93fa3f49e08c0111233252308')
BASE_URL = 'https://api.weatherapi.com/v1/current.json'


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'GET':
        return redirect(url_for('home'))

    city = (request.form.get('city') or '').strip()
    if not city:
        flash('Please enter a city name to search weather.', 'warning')
        return redirect(url_for('home'))

    params = {
        'key': API_KEY,
        'q': city,
        'aqi': 'no',
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get('current', {})
        location = data.get('location', {})

        result = {
            'city': f"{location.get('name', '')}, {location.get('region', '')}, {location.get('country', '')}",
            'localtime': location.get('localtime', ''),
            'temp_c': current.get('temp_c'),
            'temp_f': current.get('temp_f'),
            'condition_text': (current.get('condition') or {}).get('text'),
            'icon': (current.get('condition') or {}).get('icon'),
            'wind_kph': current.get('wind_kph'),
            'humidity': current.get('humidity'),
            'feelslike_c': current.get('feelslike_c'),
            'feelslike_f': current.get('feelslike_f'),
            'cloud': current.get('cloud'),
            'uv': current.get('uv'),
            'is_day': current.get('is_day'),
        }

        return render_template('weather.html', result=result)

    except requests.exceptions.HTTPError as http_err:
        try:
            err = response.json()
            msg = (err.get('error') or {}).get('message') or 'Unable to fetch weather.'
        except Exception:
            msg = f'HTTP error: {http_err}'
        flash(msg, 'danger')
        return redirect(url_for('home'))
    except requests.exceptions.RequestException:
        flash('Network error. Please check your connection and try again.', 'danger')
        return redirect(url_for('home'))
    except Exception:
        flash('Unexpected error occurred. Please try again later.', 'danger')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


