import json
import random
import time
from datetime import datetime
import csv

IDS_CAPTEURS = ["capteur-01", "capteur-02", "capteur-03"]
INTERVALLE = 1  # secondes entre deux mesures


def mesure(id_capteur):

    x = random.random()

    if x < 0.05:
        temp = round(random.choice([95.0, -40.0]), 2)
    else:
        temp = round(random.gauss(24, 1.5), 2)

    return {
        "capteur": id_capteur,
        "temperature": temp,
        "humidite": round(random.gauss(55, 5), 2),
        "horodatage": datetime.now().isoformat(timespec="seconds"),
    }


with open("mesures.csv", "w", encoding="utf-8", newline="") as fichier:

    writer = csv.DictWriter(fichier, fieldnames=[
                            "horodatage", "capteur", "temperature", "humidite"])
    writer.writeheader()

    try:
        while True:
            for id_capteur in IDS_CAPTEURS:

                data = mesure(id_capteur)
                print(json.dumps(data))
                writer.writerow(data)

            time.sleep(INTERVALLE)
    except KeyboardInterrupt:
        print("Arret du capteur.")
