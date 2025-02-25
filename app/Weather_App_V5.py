import streamlit as st
import requests
import json
import urllib.parse
import os
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

# 🔐 Secure API Keys
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI")

SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]

SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 🚀 Get Google Login URL
def get_google_login_url():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    auth_url, state = flow.authorization_url(prompt="consent")
    st.session_state["oauth_state"] = state
    return auth_url

# 🎫 Fetch Google OAuth Token
def get_google_token(auth_code):
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uris": [REDIRECT_URI],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=SCOPES,
            state=st.session_state.get("oauth_state"),
        )
        flow.redirect_uri = REDIRECT_URI
        flow.fetch_token(code=auth_code)
        return flow.credentials
    except Exception as e:
        st.error(f"⚠ Authentication failed: {e}")
        return None

# 📩 Get Google User Data
def get_google_user(token):
    try:
        headers = {"Authorization": f"Bearer {token.token}"}
        response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
        return response.json()
    except Exception as e:
        st.error(f"⚠ Failed to fetch user info: {e}")
        return None

# 🌦 Fetch Weather Data
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
        st.error(f"⚠ Error fetching weather data: {response.status_code}")
        return None

# 🌟 Streamlit UI
st.title("🌤 Weather Forecast App with Google OAuth")

# 🔑 Authentication
if not st.session_state["authenticated"]:
    login_url = get_google_login_url()
    st.markdown(f"[🔑 Login with Google]({login_url})")

    # ✅ Correctly Parse Query Parameters
    query_params = st.experimental_get_query_params()
    auth_code = query_params.get("code")

    if auth_code:
        token = get_google_token(auth_code[0])
        if token:
            user_info = get_google_user(token)
            if user_info:
                st.session_state["authenticated"] = True
                st.session_state["user"] = user_info["name"]
                st.success(f"✅ Logged in as {user_info['name']}!")
                st.rerun()
        else:
            st.error("⚠ Google Authentication failed. Try again.")

else:
    st.sidebar.write(f"👤 Logged in as: **{st.session_state['user']}**")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # 🌍 Weather Forecast
    city = st.text_input("Enter a city name:")
    if st.button("Get Weather Data"):
        if city:
            weather = get_weather(city)
            if weather:
                st.subheader(f"🌎 {weather['city']}, {weather['region']}, {weather['country']}")
                st.image(weather["icon"], width=50)
                st.write(f"📌 **Condition**: {weather['condition']}")
                st.write(f"🌡 **Temperature**: {weather['temperature']}°C")
                st.write(f"💨 **Wind Speed**: {weather['wind_speed']} km/h")
                st.write(f"💧 **Humidity**: {weather['humidity']}%")

                # 📊 Plot Weather Data
                fig = go.Figure(data=[go.Bar(
                    x=["Temperature (°C)", "Wind Speed (km/h)", "Humidity (%)"],
                    y=[weather["temperature"], weather["wind_speed"], weather["humidity"]],
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
