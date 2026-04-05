from flask import Flask,render_template,request
from weather import get_weather

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
    return render_template("weather.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)