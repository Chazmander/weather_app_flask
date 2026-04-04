def get_weather(city):
    from datetime import datetime, date, timedelta
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
    
    #fetching today and tomorrows date
    today = date.today()
    tomorrow = today + timedelta(days=1)

    #send coords to api
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city_lat,
        "longitude": city_long,
        "temperature_unit": "fahrenheit",
        "hourly": "temperature_2m,weathercode",
        "start_date": today.isoformat(),
        "end_date" : tomorrow.isoformat()}

    weather_response = requests.get(weather_url, params=params)
    weather_data = weather_response.json()
    #pull data from json
    temps = weather_data["hourly"]["temperature_2m"]
    codes = weather_data["hourly"]["weathercode"]
    times = weather_data["hourly"]["time"]

    #finding current time in times[]
    now = datetime.now()
    start_index = 0
    for index in range(len(times)):
        time_dt = datetime.fromisoformat(times[index])
        if time_dt >= now:
            start_index = index
            break

    #weathercode table
    WEATHER_CODES = {
        0: "clear skies",
        1: "mostly clear skies",
        2: "partly cloudy skies",
        3: "overcast clouds",
        45: "fog",
        48: "fog",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        56: "light freezing drizzle",
        57: "dense freezing drizzle",
        61: "light rain",
        63: "moderate rain",
        65: "heavy rain",
        66: "light freezing rain",
        67: "heavy freezing rain",
        71: "light snow",
        73: "moderate snow",
        75: "heavy snow",
        77: "snow grains",
        80: "light rain showers",
        81: "moderate rain showers",
        82: "heavy rain showers",
        85: "light snow showers",
        86: "heavy snow showers",
        95: "thunderstorms",
        96: "thunderstorms and hail",
        99: "severe thunderstorms and hail"
    }
    weather_code = codes[start_index]
    condition = WEATHER_CODES[weather_code]
    temp = temps[start_index]

    #display to user
    current = {"temp":temp,
               "condition":condition}
    forecast = []
    hours_to_show = 5
    for hour in range(hours_to_show):
        i = start_index + hour
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