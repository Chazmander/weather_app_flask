def get_weather(city):
    from datetime import datetime
    import requests

    #convert city to coords with api
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name" : city, "count" : 1}
    geo_response = requests.get(geo_url, params=params)
    geo_data = geo_response.json()
    if "results" not in geo_data or len(geo_data["results"]) == 0:
        return None
    city_lat = geo_data["results"][0]["latitude"]
    city_long = geo_data["results"][0]["longitude"]
    admin1 = geo_data["results"][0]["admin1"]
    
    #send coords to api
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city_lat,
        "longitude": city_long,
        "temperature_unit": "fahrenheit",
        "hourly" : "temperature_2m,weathercode",
        "forecast_hours": 6,
        "timezone": "auto"}

    weather_response = requests.get(weather_url, params=params)
    weather_data = weather_response.json()
    #pull data from json
    temps = weather_data["hourly"]["temperature_2m"]
    codes = weather_data["hourly"]["weathercode"]
    times = weather_data["hourly"]["time"]

    #weathercode table
    WEATHER_CODES = {
        0: "Clear Skies",
        1: "Mostly Clear Skies",
        2: "Partly Cloudy Skies",
        3: "Overcast Clouds",
        45: "Fog",
        48: "Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        56: "Light Freezing Drizzle",
        57: "Dense Freezing Drizzle",
        61: "Light Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Light Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Light Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Light Rain Showers",
        81: "Moderate Rain Showers",
        82: "Heavy Rain Showers",
        85: "Light Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorms",
        96: "Thunderstorms and Hail",
        99: "Severe Thunderstorms and Hail"
    }
    weather_code = codes[0]
    condition = WEATHER_CODES[weather_code]
    temp = temps[0]

    #display to user
    current = {"temp":temp,
               "condition":condition}
    forecast = []
    hours_to_show = 5
    for hour in range(hours_to_show):
        i =  hour + 1
        time_str = times[i]
        temp = temps[i]
        code = codes[i]
        condition = WEATHER_CODES[code]
        time_dt = datetime.fromisoformat(time_str)
        pretty_time = time_dt.strftime("%I %p").lstrip("0")
        forecast.append({"time":pretty_time,
                         "temp":temp,
                         "condition":condition})
    return{"city":city,
           "admin1":admin1,
           "current":current,
           "forecast":forecast}