from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "smart_agriculture_secret_key"

# OpenWeatherMap API Configuration
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
CITY = "Pune"


# -----------------------------
# Weather Function
# -----------------------------
def get_weather():
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={CITY}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=5)
        data = response.json()

        return {
            "temp": round(data["main"]["temp"]),
            "condition": data["weather"][0]["main"],
            "humidity": data["main"]["humidity"],
            "city": CITY
        }

    except Exception as e:
        print("Weather API Error:", e)

        return {
            "temp": 0,
            "condition": "Unavailable",
            "humidity": 0,
            "city": CITY
        }


# -----------------------------
# Smart Alert Function
# -----------------------------
def get_alert(temp, condition, language):

    condition = condition.lower()

    if language == "mr":

        if "rain" in condition:
            return "पाऊस येणार आहे - पाणी देऊ नका"

        elif temp > 35:
            return "खूप उष्णता आहे - पिकांना पाणी द्या"

        elif temp < 15:
            return "थंडी आहे - पिकांची काळजी घ्या"

        else:
            return "हवामान सामान्य आहे - नियमित देखभाल करा"

    else:

        if "rain" in condition:
            return "Rain expected - Avoid irrigation"

        elif temp > 35:
            return "High temperature - Water your crops"

        elif temp < 15:
            return "Low temperature - Protect your crops"

        else:
            return "Weather is normal - Continue regular farming"


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -----------------------------
# Login Page
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        language = request.form.get("language", "en")

        # Simple session login
        if username == "admin" and password == "admin123":

            session["user"] = username
            session["language"] = language

            return redirect(url_for("dashboard"))

        else:
            error = "Invalid Username or Password"

    return render_template("login.html", error=error)


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    weather = get_weather()

    language = session.get("language", "en")

    alert = get_alert(
        weather["temp"],
        weather["condition"],
        language
    )

    # Dummy weekly temperature data
    graph_data = [28, 30, 31, 33, 35, 32, 29]

    return render_template(
        "dashboard.html",
        weather=weather,
        alert=alert,
        graph_data=graph_data,
        language=language,
        username=session["user"]
    )


# -----------------------------
# Change Language
# -----------------------------
@app.route("/change-language/<lang>")
def change_language(lang):

    if lang in ["en", "mr"]:
        session["language"] = lang

    return redirect(url_for("dashboard"))


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
