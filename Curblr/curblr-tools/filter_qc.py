import json
import os
import requests
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

quartiers = [
    "Saint-Jean-Baptiste",
    "Cap-Rouge",
    "Cité-Universitaire",
    "Vieux-Québec—Cap-Blanc—Colline parlementaire",
    "Des Châtels",
    "Duberger—Les Saules",
    "L'Aéroport",

    "Saint-Sauveur",

    "Lac-Saint-Charles",
    "Lairet",
    "Vieux-Limoilou",
    "Loretteville",
    "Maizerets",
    "Montcalm",
    "Neufchatel Est—Lebourgneuf",
    "Notre-Dame-des-Laurentides",
    "Plateau",
    "Saint-Louis",
    "Pointe-de-Sainte-Foy",
    "Quartier 4-2",
    "Quartier 4-3",
    "Jésuites",
    "Quartier 4-5",
    "Quartier 4-6",
    "Quartier 5-1",
    "Quartier 5-2",
    "Chutes-Montmorency",
    "Quartier 5-4",
    "Saint-Émile", #//bug
    "Saint-Sacrement",
    "Saint-Roch",
    
    "Sillery",
    "Val-Bélair",
    "Vanier",
    "Vieux-Moulin"
    ]
urls = [
    "https://www.donneesquebec.ca/recherche/fr/dataset/9c11aab8-419c-4a7e-8bdc-95b5395a9f32/resource/27480cd1-ab19-47fe-a93b-9d526a0eb1e3/download/vdq-panneauxstationnement.geojson"
]
def get_files():
    for i, url in enumerate(urls):
        r = requests.get(url, stream = True)
        # file_name = PATH + urls_name[i] + ".csv"
        file_name = "data/vdq-panneauxstationnement.geojson"
        with open(file_name, "wb") as f:
            for chunk in r.iter_content(chunk_size = 1024):
                if chunk:
                    f.write(chunk)
def filter_qc(quartiers = ["Saint-Sauveur"]):
    for quartier_quebec in quartiers:
        polygone = []

        with open("data/vdq-quartier.geojson.json") as f:
            data = json.load(f)
            for i in (data["features"]):
                # print(i["properties"]["NOM"])
                if i["properties"]["NOM"] == quartier_quebec:
                    polygone = i["geometry"]["coordinates"]
                    break
        point_a_tester = []
        data = ""
        m=0
        with open("data/vdq-panneauxstationnement.geojson") as f:
            data = json.load(f)
            n=0
            l = []
            for i in (data["features"]):
                m+=1
                point_a_tester = i["geometry"]["coordinates"]
                point_format_turfpy = Feature(geometry=Point(point_a_tester))
                polygone_format_turfpy = Polygon(polygone)
                # print(point_format_turfpy)
                try:    
                    if(boolean_point_in_polygon(point_format_turfpy, polygone_format_turfpy)) == True:
                        l.append(i)
                    else:
                        n +=1
                except Exception as e:
                    print(e)
                    pass
            data["features"] = l
        # print(l)
        # print(n,m)

        outfile = "data/vdq-panneauxstationnement-filtred-" + quartier_quebec + ".geojson"
        outfile = outfile.strip().lower().replace(" ","-")
        with open(outfile, mode="w") as f:
            json.dump(data, f)
        print("filtrage termine pour", quartier_quebec)
get_files()
print("fin du téléchargement, début du filtrage")
filter_qc(quartiers=quartiers)
os.system("mv data/vdq-panneauxstationnement-filtred* ../conversion-datas/curblr-dataqc-convert/data/")

