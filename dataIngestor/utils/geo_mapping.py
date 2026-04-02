def get_geo_features(region_name):
    mapping = {
        "dehradun": ("Forest", "Loam"),
        "rishikesh": ("Forest", "Sandy"),
        "haridwar": ("Agricultural", "Clay"),
        "rudraprayag": ("Forest", "Loam"),
        "chamoli": ("Forest", "Silt"),
        "devprayag": ("Forest", "Loam"),
    }

    land, soil = mapping.get(region_name, ("Forest", "Loam"))

    return {
        "land_cover": land,
        "soil_type": soil
    }
