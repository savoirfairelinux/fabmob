'''
    Utilisation d'expressions régulieres pour extraire les periodes dans les descriptions des régulations
'''

jours = [
    "LUN", "MAR", "MER", "JEU", "VEN", "SAM", "DIM"
]

marqueurs = [
    "MAX",
    "ET",
    "À",
    "-",
    "ARRET INT.",
    "STAT. INT.",
    "EXCEPTÉ LIVR.",
    "EXCEPTÉ LIVRAISON",
    "STAT. INT. EXCEPTÉ LIVR.",
    "\P  EXCEPTÉ LIVRAISON",
    "P 15 min.  Débarcadère",
    "STAT. INT. EXCEPTÉ DÉB."
]

print("STAT. INT. EXCEPT\u00c9 D\u00c9B.".encode("utf-8").decode())