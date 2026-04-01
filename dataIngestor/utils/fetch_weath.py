def fetch_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,precipitation,wind_speed_10m"
    )

    res = requests.get(url)
    data = res.json().get("current", {})

    return {
        "temperature": data.get("temperature_2m", 0),
        "rainfall": data.get("precipitation", 0),
        "wind": data.get("wind_speed_10m", 0),
    }
