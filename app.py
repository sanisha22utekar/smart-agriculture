from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "smart_agriculture_secret"

# OpenWeatherMap API Key
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

CITY = "Pune"


def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        temp = data["main"]["temp"]
        condition = data["weather"][0]["main"]

        return {
            "temp": temp,
            "condition": condition
        }

    except:
        return {
            "temp": 0,
            "condition": "Unavailable"
        }


def get_alert(temp, language):
    if language == "mr":

        if temp > 35:
            return "खूप उष्णता आहे - पिकांना पाणी द्या"

        elif temp < 15:
            return "थंडी आहे - पिकांची काळजी घ्या"

        else:
            return "पाऊस येणार आहे - पाणी देऊ नका"

    else:

        if temp > 35:
            return "High temperature - Water your crops"

        elif temp < 15:
            return "Low temperature - Protect your crops"

        else:
            return "Rain expected - Avoid irrigation"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["user"] = username

            language = request.form.get("language", "en")
            session["language"] = language

            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    weather = get_weather()

    language = session.get("language", "en")

    alert = get_alert(weather["temp"], language)

    graph_data = [28, 30, 29, 32, 34, 31, 27]

    return render_template(
        "dashboard.html",
        weather=weather,
        alert=alert,
        graph_data=graph_data,
        language=language
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
