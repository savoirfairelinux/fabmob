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


#FIND VERSION
# import os

# versions = [
#         # "10.1.0",
#         # "10.2.0",
#         # "10.2.1",
#         # "10.3.0",
#         # "10.4.0",
#         # "10.4.1",
#         # "10.5.0",
#         # "10.6.0",
#         # "10.7.0",
#         # "10.8.0",
#         # "10.9.0",
#         # "10.10.0",
#         # "10.11.0",
#         # "10.12.0",
#         # "10.13.0",
#         # "10.14.0",
#         # "10.14.1",
#         # "10.14.2",
#         # "10.15.0",
#         # "10.15.1",
#         # "10.15.2",
#         # "10.15.3",
#         # "10.16.0",
#         # "10.16.1",
#         # "10.16.2",
#         # "10.16.3",
#         # "10.17.0",
#         # "10.18.0",
#         # "10.18.1",
#         # "10.19.0",
#         # "10.20.0",
#         # "10.20.1",
#         # "10.21.0",
#         # "10.22.0",
#         # "10.22.1",
#         # "10.23.0",
#         # "10.23.1",
#         # "10.23.2",
#         # "10.23.3",
#         # "10.24.0",
#         # "10.24.1",
#       #  # "11.0.0",
#         # "11.1.0",
#         # "11.2.0",
#         # "11.3.0",
#         # "11.4.0",
#         # "11.5.0",
#         # "11.6.0",
#         # "11.7.0",
#         # "11.8.0",
#       #  # "11.9.0",
#         # "11.10.0",
#         # "11.10.1",
#         # "11.11.0",
#         # "11.12.0",
#         # "11.13.0",
#         # "11.14.0",
#         # "11.15.0",
#         # "12.0.0",
#         # "12.1.0",
#         # "12.2.0",
#         # "12.3.0",
#         # "12.3.1",
#         # "12.4.0",
#         # "12.5.0",
#         # "12.6.0",
#         # "12.7.0",
#         # "12.8.0",
#         # "12.8.1",
#         # "12.9.0",
#         # "12.9.1",
#         # "12.10.0",
#         # "12.11.0",
#         # "12.11.1",
#         # "12.12.0",
#         # "12.13.0",
#         # "12.13.1",
#         # "12.14.0",
#         # "12.14.1",
#         # "12.15.0",
#         # "12.16.0",
#         # "12.16.1",
#         # "12.16.2",
#         # "12.16.3",
#         # "12.17.0",
#         # "12.18.0",
#         # "12.18.1",
#         # "12.18.2",
#         # "12.18.3",
#         # "12.18.4",
#         # "12.19.0",
#         # "12.19.1",
#         # "12.20.0",
#         # "12.20.1",
#         # "12.20.2",
#         # "12.21.0",
#         # "12.22.0",
#         # "12.22.1",
#         # "13.0.0",
#         # "13.0.1",
#         # "13.1.0",
#         # "13.2.0",
#         # "13.3.0",
#         # "13.4.0",
#         # "13.5.0",
#         # "13.6.0",
#         # "13.7.0",
#         # "13.8.0",
#         # "13.9.0",
#         # "13.10.0",
#         # "13.10.1",
#         # "13.11.0",
#         # "13.12.0",
#         # "13.13.0",
#         # "13.14.0",
#         "14.0.0",
#         "14.1.0",
#         "14.2.0",
#         "14.3.0",
#         "14.4.0",
#         "14.5.0",
#         "14.6.0",
#         "14.7.0",
#         "14.8.0",
#         "14.9.0",
#         "14.10.0",
#         "14.10.1",
#         "14.11.0",
#         "14.12.0",
#         "14.13.0",
#         "14.13.1",
#         "14.14.0",
#         "14.15.0",
#         "14.15.1",
#         "14.15.2",
#         "14.15.3",
#         "14.15.4",
#         "14.15.5",
#         "14.16.0",
#         "14.16.1",
#         "14.17.0",
#         "14.17.1",
#         # "15.0.0",
#         # "15.0.1",
#         # "15.1.0",
#         # "15.2.0",
#         # "15.2.1",
#         # "15.3.0",
#         # "15.4.0",
#         # "15.5.0",
#         # "15.5.1",
#         # "15.6.0",
#         # "15.7.0",
#         # "15.8.0",
#         # "15.9.0",
#         # "15.10.0",
#         # "15.11.0",
#         # "15.12.0",
#         # "15.13.0",
#         # "15.14.0",
#         # "16.0.0",
#         # "16.1.0",
#         # "16.2.0",
#         # "16.3.0"
# ]
# def run():
#         for version in versions:
#                 c1 = f"nodeenv --node={version} env -p"
#                 c2 = "shst match data/current_data.geojson" 
#                 os.system(c1)
#                 os.system(c2)

# if __name__ == "__main__":
#         run()


#INPOLYGONE
# def inPolygon(polygon, point):
#     counter = 0
#     x_inters = 0
#     p1 = [0,0]
#     p2 = [0,0]
#     p1 = polygon[0]
#     N = len(polygon)

#     for i in range(1, N):
#         p2 = polygon[i % N]
#         if point[1] > min(p1[1], p2[1]):
            
#             if point[1] <= max(p1[1], p2[1]):
                
#                 if point[0] <= max(p1[0], p2[0]):
                    
#                     if p1[1] != p2.y:
#                         x_inters = (point[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
#                         if (p1[0] == p2[0] or point[0] <= x_inters):
#                             counter += 1
#         p1 = p2

#     if (counter % 2 == 0):
#         return "outside"
#     else:
#         return "inside"

# print(inPolygon(polygon=polygone, point=[46.804405748929035, -71.25646591858953]))

import requests
import json

uri = "https://drive.google.com/uc?export=download&id=13L3dqI_DJvPL_O4PcrARZr6GsFZrS9ev"
response = json.loads(requests.get(uri).text)
print(response)