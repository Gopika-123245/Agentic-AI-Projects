import streamlit as st
import requests
from groq import Groq

st.set_page_config("Weather Agent", "🌤️")

API_KEY = "6ddaff0742138244f147d53635c48da7"

# 🔑 Groq API Key (set in environment for safety)
# export GROQ_API_KEY="your_key"
client = Groq(api_key="")  # <-- replace here or use env


def weather(city):
    r = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": API_KEY, "units": "metric"}
    ).json()

    if r.get("cod") != 200:
        return None

    return {
        "temp": r["main"]["temp"],
        "hum": r["main"]["humidity"],
        "cond": r["weather"][0]["description"]
    }


def rating(t, c):
    c = c.lower()
    return "⛈️ Bad" if "rain" in c else "🔥 Hot" if t > 35 else "❄️ Cold" if t < 10 else "🌤️ Perfect" if 20 <= t <= 30 else "🌥️ Ok"


def ai(city, d):
    prompt = f"""City:{city}
Temp:{d['temp']}°C
Humidity:{d['hum']}%
Condition:{d['cond']}

Give:
- Insight
- Outfit
- Activity (short)"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content


# ---------- UI ----------
st.title("🌍 Weather Agent (Groq Powered)")

city = st.text_input("Enter city")

if st.button("Check Weather") and city:
    data = weather(city)

    if not data:
        st.error("City not found")
    else:
        st.subheader(f"📍 {city.title()}")

        c1, c2, c3 = st.columns(3)
        c1.metric("🌡️ Temp", f"{data['temp']}°C")
        c2.metric("💧 Humidity", f"{data['hum']}%")
        c3.metric("☁️ Condition", data["cond"].title())

        st.success("Weather: " + rating(data["temp"], data["cond"]))

        with st.expander("🧠 AI Weather Agent"):
            st.write(ai(city, data))
