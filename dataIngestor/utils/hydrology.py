import requests
import json
def estimate_hydro(elev, rain):
    river_discharge = rain * (1 + elev / 1000)
    water_level = rain / 8
    return {"river_discharge": river_discharge, "water_level": water_level}
