import streamlit as st
import os
import requests
from requests_oauthlib import OAuth2Session
import plotly.graph_objects as go

# 🔐 Load API credentials securely
GITHUB_CLIENT_ID = "Ov23li5GnjAPjFmi5yCr"
GITHUB_CLIENT_SECRET = "9d7b3892b0780a28f779a4a1c9a42e102f4f5587"
WEATHER_API_KEY = "dab8caad667c4374898121150251102"
REDIRECT_URI = "http://localhost:8501"

# GitHub OAuth Endpoints
AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"

# Function to get GitHub login URL
def get_github_login_url():
    github = OAuth2Session(GITHUB_CLIENT_ID)
    auth_url, state = github.authorization_url(AUTHORIZATION_URL)
    st.session_state["oauth_state"] = state  # Save state for security check
    return auth_url

# Function to get access token from GitHub
def get_github_token(code):
    github = OAuth2Session(GITHUB_CLIENT_ID, state=st.session_state.get("oauth_state"))
    token = github.fetch_token(TOKEN_URL, client_secret=GITHUB_CLIENT_SECRET, code=code)
    return token

# Function to get GitHub user details
def get_github_user(token):
    headers = {"Authorization": f"token {token['access_token']}"}
    response = requests.get(USER_API_URL, headers=headers)
    return response.json()

# Function to fetch weather data
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "wind_speed": data["current"]["wind_kph"],
            "humidity": data["current"]["humidity"],
            "condition": data["current"]["condition"]["text"],
            "icon": f"http:{data['current']['condition']['icon']}"
        }
    else:
        st.error(f"Error fetching weather data: {response.status_code}")
        return None

# 🌟 Streamlit App UI
st.title("🌤 Weather Forecast App with GitHub OAuth")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 1️⃣ GitHub Authentication
if not st.session_state["authenticated"]:
    login_url = get_github_login_url()
    st.markdown(f"[🔑 Login with GitHub]({login_url})")

    query_params = st.query_params  # Streamlit's correct method
    code = query_params.get("code")

    if code:
        token = get_github_token(code[0])
        user_info = get_github_user(token)

        if user_info:
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_info["login"]
            st.success(f"✅ Logged in as {user_info['login']}!")
            st.rerun()

else:
    st.sidebar.write(f"👤 Logged in as: **{st.session_state['user']}**")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state.pop("user", None)
        st.rerun()

    # 2️⃣ Weather Forecast UI
    city = st.text_input("Enter a city name:")
    if st.button("Get Weather Data"):
        if city:
            weather = get_weather(city)
            if weather:
                st.subheader(f"🌎 {weather['city']}, {weather['region']}, {weather['country']}")

                # Show Weather Icon & Condition
                st.image(weather["icon"], width=50)
                st.write(f"📌 **Condition**: {weather['condition']}")
                st.write(f"🌡 **Temperature**: {weather['temperature']}°C")
                st.write(f"💨 **Wind Speed**: {weather['wind_speed']} km/h")
                st.write(f"💧 **Humidity**: {weather['humidity']}%")

                # Plot Weather Data
                fig = go.Figure(data=[go.Bar(
                    x=["Temperature (°C)", "Wind Speed (km/h)", "Humidity (%)"],
                    y=[weather["temperature"], weather["wind_speed"], weather["humidity"]],
                    hoverinfo='text',
                    marker=dict(color=['blue', 'green', 'orange'])
                )])

                fig.update_layout(
                    title=f"📊 Weather Data for {weather['city']}",
                    xaxis_title="Weather Parameters",
                    yaxis_title="Values",
                    template="plotly_dark"
                )
                st.plotly_chart(fig)
            else:
                st.error("⚠ Could not fetch weather data. Please check the city name.")
        else:
            st.error("⚠ Please enter a city name.")
