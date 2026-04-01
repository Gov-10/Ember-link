def compute_signals(weather, sat):
    rainfall = weather["rainfall"] + sat["satellite_rainfall"]
    return {
        "combined_rainfall": rainfall,
        "extreme_rain_alert": rainfall > 25,
        "flood_risk": rainfall > 40,
    }
