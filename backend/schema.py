"""Canonical input schema for the Covertype notebook's 54 predictors."""

NUMERIC_FEATURES = [
    {"name": "Elevation", "label": "Elevation", "unit": "m", "min": 1859, "max": 3858, "step": 1},
    {"name": "Aspect", "label": "Aspect", "unit": "degrees", "min": 0, "max": 360, "step": 1},
    {"name": "Slope", "label": "Slope", "unit": "degrees", "min": 0, "max": 66, "step": 1},
    {"name": "Horizontal_Distance_To_Hydrology", "label": "Horizontal distance to water", "unit": "m", "min": 0, "max": 1397, "step": 1},
    {"name": "Vertical_Distance_To_Hydrology", "label": "Vertical distance to water", "unit": "m", "min": -173, "max": 601, "step": 1},
    {"name": "Horizontal_Distance_To_Roadways", "label": "Distance to roadways", "unit": "m", "min": 0, "max": 7117, "step": 1},
    {"name": "Hillshade_9am", "label": "Hillshade · 9 am", "unit": "index", "min": 0, "max": 255, "step": 1},
    {"name": "Hillshade_Noon", "label": "Hillshade · noon", "unit": "index", "min": 0, "max": 255, "step": 1},
    {"name": "Hillshade_3pm", "label": "Hillshade · 3 pm", "unit": "index", "min": 0, "max": 255, "step": 1},
    {"name": "Horizontal_Distance_To_Fire_Points", "label": "Distance to fire points", "unit": "m", "min": 0, "max": 7173, "step": 1},
]

WILDERNESS_FEATURES = [f"Wilderness_Area_{index}" for index in range(1, 5)]
SOIL_FEATURES = [f"Soil_Type_{index}" for index in range(1, 41)]
FEATURES = [item["name"] for item in NUMERIC_FEATURES] + WILDERNESS_FEATURES + SOIL_FEATURES

COVER_TYPES = {
    1: "Spruce / fir",
    2: "Lodgepole pine",
    3: "Ponderosa pine",
    4: "Cottonwood / willow",
    5: "Aspen",
    6: "Douglas-fir",
    7: "Krummholz",
}

SAMPLE_INPUT = {
    "Elevation": 2596,
    "Aspect": 51,
    "Slope": 3,
    "Horizontal_Distance_To_Hydrology": 258,
    "Vertical_Distance_To_Hydrology": 0,
    "Horizontal_Distance_To_Roadways": 510,
    "Hillshade_9am": 221,
    "Hillshade_Noon": 232,
    "Hillshade_3pm": 148,
    "Horizontal_Distance_To_Fire_Points": 6279,
    **{f"Wilderness_Area_{index}": int(index == 1) for index in range(1, 5)},
    **{f"Soil_Type_{index}": int(index == 29) for index in range(1, 41)},
}
