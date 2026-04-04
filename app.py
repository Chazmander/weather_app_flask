from flask import Flask,jsonify
from weather import get_weather

app = Flask(__name__)
@app.route("/")
def home():
    return "Home Page"

@app.route("/weather/<city>")
def weather(city):
    data=get_weather(city)
    if data is None:
        return "City not found"
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)