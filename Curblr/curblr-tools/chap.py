'''
import os
l = [
    "vdq-panneauxstationnement-filtred-cap-rouge.geojson",
"vdq-panneauxstationnement-filtred-chutes-montmorency.geojson",
"vdq-panneauxstationnement-filtred-cité-universitaire.geojson",
"vdq-panneauxstationnement-filtred-des-châtels.geojson",
"vdq-panneauxstationnement-filtred-duberger—les-saules.geojson",
"vdq-panneauxstationnement-filtred-jésuites.geojson",
"vdq-panneauxstationnement-filtred-lac-saint-charles.geojson",
"vdq-panneauxstationnement-filtred-l'aéroport.geojson",
"vdq-panneauxstationnement-filtred-lairet.geojson",
"vdq-panneauxstationnement-filtred-maizerets.geojson",
"vdq-panneauxstationnement-filtred-montcalm.geojson",
"vdq-panneauxstationnement-filtred-neufchatel-est—lebourgneuf.geojson",
"vdq-panneauxstationnement-filtred-notre-dame-des-laurentides.geojson",
"vdq-panneauxstationnement-filtred-plateau.geojson",
"vdq-panneauxstationnement-filtred-pointe-de-sainte-foy.geojson",
"vdq-panneauxstationnement-filtred-quartier-4-2.geojson",
"vdq-panneauxstationnement-filtred-quartier-4-3.geojson",
"vdq-panneauxstationnement-filtred-quartier-4-5.geojson",
"vdq-panneauxstationnement-filtred-quartier-4-6.geojson",
"vdq-panneauxstationnement-filtred-quartier-5-1.geojson",
"vdq-panneauxstationnement-filtred-quartier-5-2.geojson",
"vdq-panneauxstationnement-filtred-quartier-5-4.geojson",
"vdq-panneauxstationnement-filtred-saint-jean-baptiste.geojson",
"vdq-panneauxstationnement-filtred-saint-louis.geojson",
"vdq-panneauxstationnement-filtred-saint-roch.geojson",
"vdq-panneauxstationnement-filtred-saint-sacrement.geojson",
"vdq-panneauxstationnement-filtredSaint-Sauveur.geojson",
"vdq-panneauxstationnement-filtred-saint-sauveur.geojson",
"vdq-panneauxstationnement-filtred-sillery.geojson",
"vdq-panneauxstationnement-filtred-val-bélair.geojson",
"vdq-panneauxstationnement-filtred-vanier.geojson",
"vdq-panneauxstationnement-filtred-vieux-limoilou.geojson",
"vdq-panneauxstationnement-filtred-vieux-moulin.geojson",
"vdq-panneauxstationnement-filtred-vieux-québec—cap-blanc—colline-parlementaire.geojson"
]
quartiers = [
    # "Saint-Jean-Baptiste",
    # "Cap-Rouge",
    # "Cité-Universitaire",
    # "Vieux-Québec—Cap-Blanc—Colline parlementaire",
    # "Des Châtels",
    # "Duberger—Les Saules",
    # "L'Aéroport",

    # "Saint-Sauveur",

    # "Lac-Saint-Charles",
    # "Lairet",
    # "Vieux-Limoilou",
    # "Loretteville",
    # "Maizerets",
    # "Montcalm",
    # "Neufchatel Est—Lebourgneuf",
    # "Notre-Dame-des-Laurentides",
    # "Plateau",
    # "Saint-Louis",
    # "Pointe-de-Sainte-Foy",
    # "Quartier 4-2",
    # "Quartier 4-3",
    # "Jésuites",
    # "Quartier 4-5",
    # "Quartier 4-6",
    # "Quartier 5-1",
    # "Quartier 5-2",
    # "Chutes-Montmorency",
    # "Quartier 5-4",
    # "Saint-Émile",//bug
    "Saint-Sacrement",
    "Saint-Roch",
    
    "Sillery",
    "Val-Bélair",
    "Vanier",
    "Vieux-Moulin"
    ]
l = [
"vdq-panneauxstationnement-filtred-chutes-montmorency.curblr.json",
"vdq-panneauxstationnement-filtred-des-châtels.curblr.json",
"vdq-panneauxstationnement-filtred-duberger—les-saules.curblr.json",
"vdq-panneauxstationnement-filtred-jésuites.curblr.json",
"vdq-panneauxstationnement-filtred-lac-saint-charles.curblr.json",
"vdq-panneauxstationnement-filtred-maizerets.curblr.json",
"vdq-panneauxstationnement-filtred-montcalm.curblr.json",
"vdq-panneauxstationnement-filtred-neufchatel-est—lebourgneuf.curblr.json",
"vdq-panneauxstationnement-filtred-notre-dame-des-laurentides.curblr.json",
"vdq-panneauxstationnement-filtred-plateau.curblr.json",
"vdq-panneauxstationnement-filtred-pointe-de-sainte-foy.curblr.json",
"vdq-panneauxstationnement-filtred-quartier-4-2.curblr.json",
"vdq-panneauxstationnement-filtred-quartier-4-3.curblr.json",
"vdq-panneauxstationnement-filtred-quartier-4-6.curblr.json",
"vdq-panneauxstationnement-filtred-quartier-5-1.curblr.json",
"vdq-panneauxstationnement-filtred-quartier-5-2.curblr.json",
"vdq-panneauxstationnement-filtred-saint-louis.curblr.json",
"vdq-panneauxstationnement-filtred-saint-roch.curblr.json",
"vdq-panneauxstationnement-filtred-saint-sacrement.curblr.json",
"vdq-panneauxstationnement-filtredSaint-Sauveur.curblr.json",
"vdq-panneauxstationnement-filtred-saint-sauveur.curblr.json",
"vdq-panneauxstationnement-filtred-val-bélair.curblr.json",
"vdq-panneauxstationnement-filtred-vanier.curblr.json",
"vdq-panneauxstationnement-filtred-vieux-moulin.curblr.json",
"vdq-panneauxstationnement-filtred-vieux-québec—cap-blanc—colline-parlementaire.curblr.json"
]    
for quartier in l:
    print('{ path: "'+ quartier +'", label: "' +'qc - ' + quartier[len("vdq-panneauxstationnement-filtred-"):-12] +'"},')
os.system("mv data/vdq* ../../CurbLr/conversion-mt-qc-et-map/curblr-dataqc-convert/data/")
arrondissements = [
    "plaza",
    "Outremont",#0
    "LaSalle",
    "Mont-Royal", #absent dans curbconvert
    "Ville-Marie",
    "Le Plateau-Mont-Royal", #4 #Plateau-Mont-Royal
    "Hampstead", #absent dans curbconvert
    "Le Sud-Ouest", #"Sud-Ouest"
    "Rivière-des-Prairies-Pointe-aux-Trembles", #"Rivière-des-Prairies - Pointe-aux-Trembles"
    "Lachine", #8
    "Dorval", #absent
    "Montréal-Nord", 
    "L'Île-Bizard-Sainte-Geneviève", #un script pour extraire tous les noms arrond? #"L'Île-Bizard - Sainte-Geneviève"
    "Kirkland", #12 #Absent
    "Dollard-des-Ormeaux",
    "Senneville",
    "Ahuntsic-Cartierville",
    "Côte-Saint-Luc", #16
    "Saint-Léonard",
    "Montréal-Ouest",
    "Pointe-Claire",
    "L'Île-Dorval", #20
    "Mercier-Hochelaga-Maisonneuve",
    "Côte-des-Neiges-Notre-Dame-de-Grâce",
    "Rosemont-La Petite-Patrie",
    "Saint-Laurent", #24
    "Beaconsfield",
    "Villeray-Saint-Michel-Parc-Extension",
    "Westmount",
    "Montréal-Est", #28
    "Anjou",
    "Pierrefonds-Roxboro",
    "Sainte-Anne-de-Bellevue",
    "Verdun", #32
    "Baie-d'Urfé"
]
for arrondissement in arrondissements:
    print('{ label: "'+ arrondissement +'", value: "' + arrondissement +'"},')
'''

import requests
import json

#en deploimement
# uri = "https://alivisiond4.herokuapp.com"
#en local
# uri = "http://127.0.0.1:8081/items"

# payload = {
# #   "true_date": "2021-04-18T09:31:44.601Z",
# #   "true_date_dayow": "2021-04-18",
#   "true_date_dayom": "yoi",
#   "true_date_month": "may",
# #   "true_date_time": "09:31:44",
#   "arrond_quartier": "Rosemont",
#   "price": 3,
#   "maxStay": 32
# }
# payload = dict(true_date_dayom="yoi",
#   true_date_month= "may")
# r = requests.post(uri, data=payload)
# print(r.status_code, r.text)

import requests
import json

uri = "https://drive.google.com/uc?export=download&id=13L3dqI_DJvPL_O4PcrARZr6GsFZrS9ev"
response = json.loads(requests.get(uri).text)
print(response)