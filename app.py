from flask import Flask, render_template
import datetime
import requests

app = Flask(__name__)

# 🔹 Ustawienia API pogodowego
API_KEY = "1513648dee8b5b34ff07935309c7f01f"  # Pobierz z https://openweathermap.org/api
CITY = "Nowa Sól"

def get_weather():
    """Pobiera aktualną pogodę dla wybranego miasta."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pl"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Obsługa błędnych danych
        if "main" in data and "temp" in data["main"] and "weather" in data:
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"{temperature}°C, {description}"
        else:
            return "Nie udało się pobrać danych pogodowych"
    except requests.RequestException:
        return "Brak danych o pogodzie"

def get_namedays():
    """Pobiera imieniny na dzisiaj z API Abalin."""
    url = "https://api.genderapi.io/api/?name=Maciek"
    try:
        response = requests.get(url, timeout=5, verify=False)  # Wyłączamy SSL
        response.raise_for_status()
        data = response.json()

        # Obsługa błędnych danych
        if "data" in data and "namedays" in data["data"] and "pl" in data["data"]["namedays"]:
            return ", ".join(data["data"]["namedays"]["pl"])
        else:
            return "Brak danych o imieninach"
    except requests.RequestException:
        return "Brak danych o imieninach"

def get_holidays():
    """Pobiera święta nietypowe na dziś."""
    today = datetime.datetime.today().strftime("%m-%d")
    url = "https://imieniny.vercel.app/121224"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Obsługa błędnych danych
        if isinstance(data, list):  
            holidays_today = [holiday["name"] for holiday in data if "date" in holiday and holiday["date"] == today]
            return ", ".join(holidays_today) if holidays_today else "Brak ważnych świąt"
        else:
            return "Brak ważnych świąt"
    except requests.RequestException:
        return "Brak danych o świętach"

@app.route("/")
def home():
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    weather = get_weather()
    namedays = get_namedays()
    holidays = get_holidays()

    return render_template("index.html", date=today, temperature=weather, names=namedays, holidays=holidays)

if __name__ == "__main__":
    app.run(debug=True, port=5000)