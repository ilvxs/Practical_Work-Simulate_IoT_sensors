import json
import random
import time
from datetime import datetime
import csv
from math import sin, pi
import argparse
from collections import deque


parser = argparse.ArgumentParser()

# nbr de capteurs a simuler (3 par défaut)
parser.add_argument("--nb", type=int, default=3)
# intervalle en secondes entre deux tours de simulation (2 sec par défaut)
parser.add_argument("--intervalle", type=float, default=2)
# probabilité de générer une anomalie (5 % par défaut)
parser.add_argument("--anomalies", type=float, default=0.05)
# nbr de tours a effectuer (0 -> infinie)
parser.add_argument("--tours", type=int, default=0)

args = parser.parse_args()

IDS_CAPTEURS = ["capteur-%02d" % i for i in range(1, args.nb + 1)]

# chaque deque contient les 5 dernieres valeurs collectées par le meme capteur
fenetres = {id_capteur: deque(maxlen=5) for id_capteur in IDS_CAPTEURS}

debut = time.time()

ETATS = ["aberrant", "suspect", "ok"]

panne_restante = {id_capteur: 0 for id_capteur in IDS_CAPTEURS}


def mesure(id_capteur, t, prob_anomalie):

    x = random.random()

    bruit = random.gauss(0, 0.5)
    temp_normale = round(22 + 4 * sin(2 * pi * t / 120) + bruit, 2)

    if x < prob_anomalie:
        temp = round(random.choice([95.0, -40.0, temp_normale + 10]), 2)
    else:
        temp = temp_normale

    return {
        "capteur": id_capteur,
        "temperature": temp,
        "humidite": round(random.gauss(55, 5), 2),
        "horodatage": datetime.now().isoformat(timespec="seconds"),
    }


def verifier_mesures(data, id_capteur):

    temp = data["temperature"]
    # 'fen' est une réference vers le deque stocké dans 'fenetres'
    fen = fenetres[id_capteur]

    if (temp < -10 or temp > 60):
        data["etat"] = ETATS[0]

    else:
        if len(fen) == 5:
            moyenne = sum(fen) / len(fen)

            if abs(temp - moyenne) > 5:
                data["etat"] = ETATS[1]
            else:
                data["etat"] = ETATS[2]

        else:
            # si on n'a pas encore 5 mesures on ne peut pas effectuer la comparaison
            data["etat"] = ETATS[2]

        fen.append(temp)


with open("mesures.csv", "w", encoding="utf-8", newline="") as fichier:

    writer = csv.DictWriter(fichier, fieldnames=[
                            "horodatage", "capteur", "temperature", "humidite", "etat"])
    writer.writeheader()

    tour = 0

    try:
        while args.tours == 0 or tour < args.tours:

            secs = time.time() - debut

            for id_capteur in IDS_CAPTEURS:

                # verifier si le capteur est deja muet
                if panne_restante[id_capteur] != 0:
                    panne_restante[id_capteur] -= 1
                    continue
                else:
                    x = random.random()

                    if x < 0.02:  # 2% de chances que le capteur tombe en panne
                        panne_restante[id_capteur] = 4
                    else:
                        data = mesure(id_capteur, secs, args.anomalies)
                        # détection des mesures suspectes
                        verifier_mesures(data, id_capteur)

                        print(json.dumps(data))
                        writer.writerow(data)

            fichier.flush()

            tour += 1

            if args.tours == 0 or tour < args.tours:
                time.sleep(args.intervalle)

    except KeyboardInterrupt:
        print("Arret du capteur.")
