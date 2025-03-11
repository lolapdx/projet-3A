from datetime import datetime
from PIL import Image, ImageDraw
import numpy as np
import random


random.seed(1)


# Définir les couleurs
HEX_COLORS = [
    "#001f3f", "#003f7f", "#005fbf", "#007fff", "#3399ff",
    "#66b2ff", "#99ccff", "#cce6ff", "#e6f0ff", "#f0e6ff",
    "#e6ccff", "#d9b3ff", "#cc99ff", "#bf80ff", "#b266ff",
    "#a64dff", "#9933ff", "#8c1aff", "#7f00ff", "#6600cc"
]


# Convertir les couleurs hexadécimales en RGB
RGB_COLORS = [(int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)) for hex_color in HEX_COLORS]


def adjust_image_brightness(image, luminosity_factor):
    """Ajuster la luminosité d'une image."""
    image_np = np.array(image).astype(np.float32)
    image_np *= luminosity_factor
    image_np = np.clip(image_np, 0, 255).astype(np.uint8)
    return Image.fromarray(image_np)


def apply_wind(image, amplitude: int, direction: str):
    """Appliquer une distorsion de vent à une image."""
    image_np = np.array(image)
    rows, cols, channels = image_np.shape
    distorted_image = np.zeros_like(image_np)


    for y in range(rows):
        for x in range(cols):
            displacement_x = int(amplitude * np.sin(np.pi * y / rows))
            displacement_y = int(amplitude * np.sin(np.pi * x / cols))
            new_x, new_y = x, y


            # Appliquer la distorsion en fonction de la direction du vent
            if direction == "right":
                new_x = x + displacement_x
            elif direction == "left":
                new_x = x - displacement_x
            elif direction == "down":
                new_y = y + displacement_y
            elif direction == "up":
                new_y = y - displacement_y
            elif direction == "northeast":
                new_x = x + displacement_x
                new_y = y - displacement_y
            elif direction == "northwest":
                new_x = x - displacement_x
                new_y = y - displacement_y
            elif direction == "southeast":
                new_x = x + displacement_x
                new_y = y + displacement_y
            elif direction == "southwest":
                new_x = x - displacement_x
                new_y = y + displacement_y


            # S'assurer que les nouvelles coordonnées sont dans les limites de l'image
            new_x = max(0, min(cols - 1, new_x))
            new_y = max(0, min(rows - 1, new_y))
            distorted_image[y, x] = image_np[new_y, new_x]


    return distorted_image


def generate_square(temperature, cloud_cover):
    """Générer une image carrée basée sur la température et la couverture nuageuse."""
    image = Image.new("RGB", (4, 4), "white")
    pixels = image.load()
    index = int((temperature + 10) // 3)


    for x in range(4):
        for y in range(4):
            pixels[x, y] = random.choice(RGB_COLORS[index:index + 3])


    return adjust_image_brightness(image, cloud_cover)


def adapt_cloud_cover(cloud_cover):
    """Adapter les valeurs de couverture nuageuse."""
    return [((9 - octas + 1) * 3 + 80) / 100 for octas in cloud_cover]




def adapt_wind_direction(wind_directions):
    """Convertir la direction du vent en radians en une direction sous forme de chaîne."""
    avg_direction = sum(wind_directions) / len(wind_directions)
    if avg_direction < 22.5:
        return "northeast"
    elif avg_direction < 67.5:
        return "right"
    elif avg_direction < 112.5:
        return "southeast"
    elif avg_direction < 157.5:
        return "down"
    elif avg_direction < 202.5:
        return "southwest"
    elif avg_direction < 247.5:
        return "left"
    elif avg_direction < 292.5:
        return "northwest"
    else:
        return "up"


def add_rain_effect(image, width, height, rain_intensity):
    """Ajouter un effet de pluie à une image."""
    draw = ImageDraw.Draw(image)
    max_drops = int((width * height) * rain_intensity / 1000)


    for _ in range(max_drops):
        drop_x = random.randint(0, width - 1)
        drop_y_start = random.randint(0, height - 1)
        drop_y_end = drop_y_start + random.randint(0, 3)
        draw.line([drop_x, drop_y_start, drop_x, drop_y_end], fill=(255, 255, 255), width=3)


    return image


def average_wind_speed(wind_speeds):
    """Calculer la vitesse moyenne du vent."""
    return sum(wind_speeds) / len(wind_speeds)


def average_rain_intensity(rain_intensities):
    """Calculer l'intensité moyenne de la pluie."""
    return sum(rain_intensities) / len(rain_intensities)


def generate_image_grid(datajson):
    """Générer une image plus grande composée de petits carrés représentant différentes heures de la journée."""
    temperatures = datajson["temperature"]
    cloud_covers = adapt_cloud_cover(datajson["nuage"])
    rain_intensity = average_rain_intensity(datajson["precipitation"])
    wind_amplitude = average_wind_speed(datajson["vent_vitesse"]) * 50/3
    wind_direction = adapt_wind_direction(datajson["vent_direction"])


    total_width = 4 * 6
    total_height = 4 * 4
    new_image = Image.new("RGB", (total_width, total_height))


    for hour in range(24):
        square_image = generate_square(temperatures[hour], cloud_covers[hour])
        quotient = hour // 4
        remainder = hour % 4
        new_image.paste(square_image, (quotient * 4, remainder * 4))


    # Agrandir l'image pour une meilleure visualisation
    enlarged_image = new_image.resize((new_image.size[0] * 50, new_image.size[1] * 50), resample=Image.NEAREST)
    final_image = Image.fromarray(apply_wind(enlarged_image, wind_amplitude, wind_direction))
    final_image = add_rain_effect(final_image, total_width * 50, total_height * 50, rain_intensity)


    return final_image


def create_daily_paint(datajson):
    """Créer l'image de visualisation météorologique pour les données fournies."""
    final_image = generate_image_grid(datajson)
    return final_image




### TESTS
def test():
    datajson_test = {
        "temperature": [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
        "precipitation": 0.5,  # Rain intensity (0 to 1)
        "vent_vitesse": 5,  # Wind speed
        "vent_direction": [45, 90, 135, 180, 225, 270, 315, 360, 45, 90, 135, 180, 225, 270, 315, 360, 45, 90, 135, 180, 225, 270, 315, 360],  # Wind directions in degrees
        "nuage": [2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1]  # Cloud cover (0 to 8)
    }


    datajson_test_high_wind = {
        "temperature": [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
        "precipitation": 0.5,  # Rain intensity (0 to 1)
        "vent_vitesse": 45,  # Higher wind speed
        "vent_direction": [0, 45, 90, 135, 180, 225, 270, 315, 0, 45, 90, 135, 180, 225, 270, 315, 0, 45, 90, 135, 180, 225, 270, 315],  # Wind directions in degrees
        "nuage": [2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1]  # Cloud cover (0 to 8)
    }


    # Test the function
    final_image = create_daily_paint(datajson_test_high_wind)
    # Save the image to a file
    image_path = "daily_weather_chart_high_wind.png"
    final_image.save(image_path)
    return