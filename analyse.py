import pandas as pd
from datetime import datetime

capteurs_df = pd.read_csv('mesures.csv',
                          parse_dates=["horodatage"],
                          dtype={"capteur": "string",
                                 "temperature": "float64",
                                 "humidite": "float64",
                                 "etat": "string"
                                 },
                          encoding="utf-8"
                          )

for id_capteur, groupe in capteurs_df.groupby("capteur"):
    print(f"\n--- {id_capteur} ---")
    print(f"le nombre de mesures : {groupe.shape[0]}")
    print(
        f"le nombre de mesures aberrantes : {groupe.loc[groupe['etat'].str.contains('aberrant')].shape[0]}")
    print(
        f"le nombre de mesures suspectes : {groupe.loc[groupe['etat'].str.contains('suspect')].shape[0]}")

print(f"\nla moyenne de toutes les températures pour chaque capteur : ")
print(capteurs_df.groupby("capteur")["temperature"].mean())

temperatues_valides = capteurs_df[capteurs_df["etat"] != "aberrant"]
print(f"\nla moyenne et l'écart-type de toutes les températures non aberrantes pour chaque capteur : \n")
print(temperatues_valides.groupby(["capteur"]).agg({
    "temperature": ["mean", "std"]
}))

print(f"\nles moments où un capteur est resté plus de 3 intervalles sans mesure : \n")
intervalle = int((input("saisie l'intervalle (int) : ")))

for id_capteur, groupe in capteurs_df.groupby("capteur"):
    groupe = groupe.sort_values("horodatage").copy()
    groupe["precedent"] = groupe["horodatage"].shift(1)
    groupe["ecart"] = (groupe["horodatage"] -
                       groupe["precedent"]).dt.total_seconds()
    trous = groupe[groupe["ecart"] > 3 * intervalle]

    for _, item in trous.iterrows():
        print(
            f"{id_capteur} : trou entre {item["precedent"]} et {item["horodatage"]} ({item["ecart"]} secondes)")
