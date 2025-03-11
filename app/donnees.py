import time
import datetime as dt
import requests
import csv
import io


### Variables globales


BASE_URL_METEO_FRANCE = "https://public-api.meteofrance.fr/public/DPClim/v1/"
API_KEY_METEO_FRANCE = open('./api-key.txt', 'r').read()


# période souhaitée (journée précédente)     /!\A CHANGER
date_fin = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) # aujourd'hui à minuit
date_debut = date_fin - dt.timedelta(days=1) # hier à minuit
date_fin_str = date_fin.strftime("%Y-%m-%dT%H:%M:%SZ") # format --> chaîne de caractères
date_debut_str = date_debut.strftime("%Y-%m-%dT%H:%M:%SZ") # format --> chaîne de caractères


def recuperer_code_station(ville) :
    ville_lower_case = ville.lower()
    if(ville_lower_case == "marseille") :
        return "13054001" #Marignane
    elif(ville_lower_case == "lyon") :
        return "69299001" #Lyon St Exupery
    elif(ville_lower_case == "paris") :
        return "95527001" #Roissy
    elif(ville_lower_case == "nantes") :
        return "44020001" #Nantes Bouguenais
    elif(ville_lower_case == "lille") :
        return "59343001" #Lille Lesquin


def recuperer_code_commande(code_station, date_debut_str, date_fin_str):
    # '''Récupérer id-cmde -- date et d'heure en ISO 8601  (exemple : 2025-01-28T14:30:45Z)'''
    try :
        url = f"{BASE_URL_METEO_FRANCE}commande-station/horaire?apikey={API_KEY_METEO_FRANCE}&id-station={code_station}&date-deb-periode={date_debut_str}&date-fin-periode={date_fin_str}"
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP (ex. 404, 500)
        data = response.json()
        try:
            code_commande = int(data['elaboreProduitAvecDemandeResponse']['return'])
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError("La réponse API ne contient pas la clé attendue 'elaboreProduitAvecDemandeResponse/return'") from e
        return code_commande
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur lors de la requête API : {e}") from e


def recuperer_data_json_from_id_cmde(id_cmde):
    '''Récupérer les données associées à un id-cmde'''
    time.sleep(0.1)
    try :
        url = f"{BASE_URL_METEO_FRANCE}commande/fichier?apikey={API_KEY_METEO_FRANCE}&id-cmde={id_cmde}"
        data=[]
        response = requests.get(url)
        texte= response.text
        texte_modifie = texte.replace(",", ".")
        csv_donnes = csv.reader(io.StringIO(texte_modifie))
        for row in csv_donnes :
            # Séparer la chaîne par les points-virgules
            elements = row[0].split(";")
            data.append(elements)
        temperature = []
        precipitation = []
        vent_vitesse = []
        vent_direction = []
        nuage = []
        for i in range(24) :
            temperature.append(float(data[1 + i][10]) if data[1 + i][10] else 0)
            precipitation.append(float(data[1 + i][2]) if data[1 + i][2] else 0)
            vent_vitesse.append(float(data[1 + i][48]) if data[1 + i][48] else 0)
            vent_direction.append(float(data[1 + i][50]) if data[1 + i][50] else 0)
            nuage.append(float(data[1 + i][120]) if data[1 + i][120] else 4)
        donnees_json = {
            "temperature": temperature,
            "precipitation": precipitation,
            "vent_vitesse": vent_vitesse,
            "vent_direction": vent_direction,
            "nuage": nuage
        }
        return donnees_json
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur lors de la requête API : {e}") from e
   
def recuperer_donnees_json(ville, jour):
    code_station = recuperer_code_station(ville)
    print("code station récupéré")
    # ATTENTION AU JOUR !
    # test --> il faudra prendre le jour d'après et pas la veille (exemple quand je demande le 31/12 ca demande les données entre le 30 et le 31 mais c'est pas ce qu'on veut)
    date_jour = dt.datetime.strptime(jour, "%Y-%m-%dT%H:%M:%SZ")
    date_lendemain = date_jour + dt.timedelta(days=1)
    date_jour_str = date_jour.strftime("%Y-%m-%dT%H:%M:%SZ")
    date_lendemain_str = date_lendemain.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(date_lendemain_str)
    print(date_jour_str)
    id_cmde = recuperer_code_commande(code_station, date_jour_str, date_lendemain_str)
    print(id_cmde)
    time.sleep(0.1) #a voir pour éviter d'avoir un time sleep ici
    data_json = recuperer_data_json_from_id_cmde(id_cmde)
    print(data_json)
    return data_json


# data = recuperer_donnees_json("marseille", "jour_pas_important")
# print(data)