import streamlit as st
import requests
import plotly.graph_objects as go

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
        condition_icon = data['current']['condition']['icon']  # Icon URL

        return city_name, region, country, temperature, wind_speed, humidity, condition, condition_icon
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None, None, None, None, None, None, None, None

# Streamlit App UI
st.title("Weather Forecast App")

# Input field to enter city name
city = st.text_input("Enter a city name:")

if st.button("Get Weather Data"):
    if city:
        city_name, region, country, temperature, wind_speed, humidity, condition, condition_icon = get_weather(city)

        if city_name:
            # Display weather information with the icon
            st.subheader(f"Current Weather in {city_name}, {region}, {country}:")

            # Show weather icon (downloaded from the icon URL)
            icon_url = f"http:{condition_icon}"  
            st.image(icon_url, width=50, caption=condition)  

            st.write(f"Temperature: {temperature}°C")
            st.write(f"Wind Speed: {wind_speed} km/h")
            st.write(f"Humidity: {humidity}%")
            st.write(f"Condition: {condition}")

            # Create a Plotly bar chart to show the weather data
            weather_data = {
                'Temperature (°C)': temperature,
                'Wind Speed (km/h)': wind_speed,
                'Humidity (%)': humidity
            }

            # Create the Plotly bar chart with tooltips
            fig = go.Figure(data=[go.Bar(
                x=list(weather_data.keys()),  
                y=list(weather_data.values()),  
                hovertext=[f"{key}: {value}" for key, value in weather_data.items()],  # Tooltips
                hoverinfo='text',  
                marker=dict(color=['blue', 'green', 'orange'])  # Different colors for each bar
            )])

            # Add title and axis labels
            fig.update_layout(
                title=f"Weather Data for {city_name}",
                xaxis_title="Weather Parameter",
                yaxis_title="Value",
                template="plotly_dark"  # Optional: Choose a theme
            )

            # Display the plot
            st.plotly_chart(fig)
        else:
            st.error("Could not retrieve weather data. Please check the city name and try again.")
    else:
        st.error("Please enter a city name.")
