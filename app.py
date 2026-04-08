from flask import Flask,render_template,request
from weather import get_weather
from db_setup import init_db
import sqlite3

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/weather")
def weather():
    city = request.args.get("city").title()
    data=get_weather(city)
    if data is None:
        return "City not found", 404
    
    temp = data["current"]["temp"]
    condition = data["current"]["condition"]
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO searches (city, temp, condition)  
    VALUES (?,?,?)
    """, (city, temp, condition))

    conn.commit()
    conn.close()

    return render_template("weather.html", data=data)

@app.route("/history")
def history():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    cursor.execute("SELECT city, temp, condition FROM searches")
    data = cursor.fetchall()
    conn.close()
    return render_template("history.html", data=data)
if __name__ == "__main__":
    init_db()
    app.run(debug=True)