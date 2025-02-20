import streamlit as st
import requests
import plotly.graph_objects as go

# Function to validate login
def login():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if username == "admin" and password == "password123":  # Replace with a secure authentication method
            st.session_state["authenticated"] = True
            st.sidebar.success("Login successful!")
            st.rerun()

        else:
            st.sidebar.error("Invalid username or password")

# Function to get weather data from WeatherAPI
def get_weather(city):
    api_key = "dab8caad667c4374898121150251102"  # Replace with your API key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city_name = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        temperature = data['current']['temp_c']
        wind_speed = data['current']['wind_kph']
        humidity = data['current']['humidity']
        condition = data['current']['condition']['text']
        condition_icon = data['current']['condition']['icon']

        return city_name, region, country, temperature, wind_speed, humidity, condition, condition_icon
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None, None, None, None, None, None, None, None

# Authentication Check
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    # Streamlit App UI (Only visible after login)
    st.title("🌤 Weather Forecast App")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

    city = st.text_input("Enter a city name:")

    if st.button("Get Weather Data"):
        if city:
            city_name, region, country, temperature, wind_speed, humidity, condition, condition_icon = get_weather(city)

            if city_name:
                st.subheader(f"Current Weather in {city_name}, {region}, {country}:")

                icon_url = f"http:{condition_icon}"  
                st.image(icon_url, width=50, caption=condition)  

                st.write(f"🌡 Temperature: {temperature}°C")
                st.write(f"💨 Wind Speed: {wind_speed} km/h")
                st.write(f"💧 Humidity: {humidity}%")
                st.write(f"📌 Condition: {condition}")

                # Create a Plotly bar chart for weather data
                weather_data = {
                    'Temperature (°C)': temperature,
                    'Wind Speed (km/h)': wind_speed,
                    'Humidity (%)': humidity
                }

                fig = go.Figure(data=[go.Bar(
                    x=list(weather_data.keys()),  
                    y=list(weather_data.values()),  
                    hovertext=[f"{key}: {value}" for key, value in weather_data.items()],  
                    hoverinfo='text',  
                    marker=dict(color=['blue', 'green', 'orange'])  
                )])

                fig.update_layout(
                    title=f"Weather Data for {city_name}",
                    xaxis_title="Weather Parameter",
                    yaxis_title="Value",
                    template="plotly_dark"  
                )

                st.plotly_chart(fig)
            else:
                st.error("Could not retrieve weather data. Please check the city name and try again.")
        else:
            st.error("Please enter a city name.")
