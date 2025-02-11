import streamlit as st
import requests

# Function to get weather data from WeatherAPI
def get_weather(city):
    api_key = "dab8caad667c4374898121150251102"  # Replace with your API key from WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response

        # Extract current weather data
        city_name = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        temperature = data['current']['temp_c']
        wind_speed = data['current']['wind_kph']
        humidity = data['current']['humidity']
        condition = data['current']['condition']['text']

        return city_name, region, country, temperature, wind_speed, humidity, condition
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None, None, None, None, None, None, None

# Streamlit App UI
st.title("Weather Forecast App")

# Input field to enter city name
city = st.text_input("Enter a city name:")

if st.button("Get Weather Data"):
    if city:
        city_name, region, country, temperature, wind_speed, humidity, condition = get_weather(city)

        if city_name:
            st.subheader(f"Current Weather in {city_name}, {region}, {country}:")
            st.write(f"Temperature: {temperature}°C")
            st.write(f"Wind Speed: {wind_speed} km/h")
            st.write(f"Humidity: {humidity}%")
            st.write(f"Condition: {condition}")
        else:
            st.error("Could not retrieve weather data. Please check the city name and try again.")
    else:
        st.error("Please enter a city name.")
