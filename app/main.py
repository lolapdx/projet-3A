import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from donnees import recuperer_donnees_json
from tableau import create_daily_paint
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/villes/{ville}")
def read_city(ville):
    print("Reading city", ville)
    return FileResponse("../static/ville.html")


@app.get("/info.html")
def read_info():
    return FileResponse("../static/info.html")


@app.get("/jour/{jour}")
def send_image(jour: str):
    print("Generating images for all cities")
    date = jour[:10].replace("-", "_")
    image_path_marseille = "../static/images/marseille/marseille_"+date+".png"
    image_path_paris = "../static/images/paris/paris_"+date+".png"
    image_path_lyon = "../static/images/lyon/lyon_"+date+".png"
    image_path_nantes = "../static/images/nantes/nantes_"+date+".png"
    image_path_lille = "../static/images/lille/lille_"+date+".png"
    if not os.path.exists(image_path_marseille):
        print("Generating image for Marseille")
        data_marseille = recuperer_donnees_json("marseille", jour)
        IMAGE_marseille = create_daily_paint(datajson=data_marseille)
        print("Image Marseille created")
        IMAGE_marseille.save(image_path_marseille)
        print("Image Marseille saved")
    if not os.path.exists(image_path_paris):
        print("Generating image for Paris")
        data_paris = recuperer_donnees_json("paris", jour)
        IMAGE_paris = create_daily_paint(datajson=data_paris)
        print("Image Paris created")
        IMAGE_paris.save(image_path_paris)
        print("Image Paris saved")
    if not os.path.exists(image_path_lyon):
        print("Generating image for Lyon")
        data_lyon = recuperer_donnees_json("lyon", jour)
        IMAGE_lyon = create_daily_paint(datajson=data_lyon)
        print("Image Lyon created")
        IMAGE_lyon.save(image_path_lyon)
        print("Image Lyon saved")
    if not os.path.exists(image_path_nantes):
        print("Generating image for Nantes")
        data_nantes = recuperer_donnees_json("nantes", jour)
        IMAGE_nantes = create_daily_paint(datajson=data_nantes)
        print("Image Nantes created")
        IMAGE_nantes.save(image_path_nantes)
        print("Image Nantes saved")
    if not os.path.exists(image_path_lille):
        print("Generating image for Lille")
        data_lille = recuperer_donnees_json("lille", jour)
        IMAGE_lille = create_daily_paint(datajson=data_lille)
        print("Image Lille created")
        IMAGE_lille.save(image_path_lille)
        print("Image Lille saved")

    # Retourne les chemins des fichiers images
    return JSONResponse({
        "marseille": image_path_marseille,
        "paris": image_path_paris,
        "lyon": image_path_lyon,
        "nantes": image_path_nantes,
        "lille": image_path_lille
    })



@app.get("/villes/{ville}/jour/{jour}")
def send_image(ville: str, jour: str):
    date = jour[:10].replace("-", "_")
    image_path = "../static/images/"+ville+"/"+ville+"_"+date+".png"
    print("image_path", image_path)
    if not os.path.exists(image_path):
        print("Generating image for city")
        data = recuperer_donnees_json(ville, jour)
        print("data loaded")
        IMAGE = create_daily_paint(datajson=data)
        print("Image created")
        IMAGE.save(image_path)
        print("Image saved")
    # Retourne le fichier image
    return FileResponse(image_path, media_type="image/png")

@app.get("/")
async def read_index():
    return FileResponse("../static/index.html")


@app.get("/{path:path}")
async def catch_all(path: str):
    return FileResponse("../static/index.html")