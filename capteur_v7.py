import json
import random
import time
from datetime import datetime
import csv
from math import sin, pi
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--nb", type=int, default=3)
parser.add_argument("--intervalle", type=float, default=2)
parser.add_argument("--anomalies", type=float, default=0.05)
parser.add_argument("--tours", type=int, default=0)

args = parser.parse_args()

IDS_CAPTEURS = ["capteur-%02d" % i for i in range(1, args.nb + 1)]

debut = time.time()


def mesure(id_capteur, t, prob_anomalie):

    x = random.random()

    if x < prob_anomalie:
        temp = random.choice([95.0, -40.0])
    else:
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

    tour = 0

    try:
        while args.tours == 0 or tour < args.tours:

            secs = time.time() - debut

            for id_capteur in IDS_CAPTEURS:

                data = mesure(id_capteur, secs, args.anomalies)

                print(json.dumps(data))
                writer.writerow(data)

            fichier.flush()

            tour += 1

            if args.tours == 0 or tour < args.tours:
                time.sleep(args.intervalle)

    except KeyboardInterrupt:
        print("Arret du capteur.")
