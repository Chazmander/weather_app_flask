from flask import Flask, render_template, request
from weather import get_weather
from db_setup import init_db
import sqlite3

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/weather")
def weather():
    raw_city = request.args.get("city")
    city = (raw_city or "").strip()
    if not city:
        return render_template("home.html", error="Please enter a city"), 400
    
    city = city.title()

    data = get_weather(city)
    if "error" in data:
        return render_template("home.html", error=data["error"]), 404
    
    temp = data["current"]["temp"]
    condition = data["current"]["condition"]
    admin1 = data["admin1"]
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO searches (city, admin1, temp, condition)  
    VALUES (?,?,?,?)
    """, (city, admin1, temp, condition))

    conn.commit()
    conn.close()

    return render_template("weather.html", data=data)

@app.route("/history")
def history():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    cursor.execute("""SELECT city, admin1, temp, condition, datetime(created_at, 'localtime') FROM searches
                   ORDER BY id DESC
                   LIMIT 10
                    """)
    data = cursor.fetchall()
    conn.close()
    return render_template("history.html", data=data)
if __name__ == "__main__":
    init_db()
    app.run(debug=True)