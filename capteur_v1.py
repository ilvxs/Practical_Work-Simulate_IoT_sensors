import json
import random
import time
from datetime import datetime

ID_CAPTEUR = "salle-B"
INTERVALLE = 1  # secondes entre deux mesures


def mesure():
    return {
        "capteur": ID_CAPTEUR,
        "temperature": round(random.gauss(24, 1.5), 2),
        "humidite": round(random.gauss(55, 5), 2),
        "horodatage": datetime.now().isoformat(timespec="seconds"),
    }


try:
    while True:
        print(json.dumps(mesure()))
        time.sleep(INTERVALLE)
except KeyboardInterrupt:
    print("Arret du capteur.")
