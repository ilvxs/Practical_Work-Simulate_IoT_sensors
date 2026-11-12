import json
import random
import time
from datetime import datetime
import csv
from math import sin, pi

IDS_CAPTEURS = ["capteur-01", "capteur-02", "capteur-03"]
INTERVALLE = 1  # secondes entre deux mesures

debut = time.time()


def mesure(id_capteur, t):

    bruit = random.gauss(0, 0.5)

    temp = round(22 + 4 * sin(2 * pi * t / 120) + bruit, 2)

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

            secs = time.time() - debut

            for id_capteur in IDS_CAPTEURS:

                data = mesure(id_capteur, secs)

                print(json.dumps(data))
                writer.writerow(data)

            fichier.flush()

            time.sleep(INTERVALLE)
    except KeyboardInterrupt:
        print("Arret du capteur.")
