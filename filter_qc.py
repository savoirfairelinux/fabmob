import json 
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

quartiers = ["Saint-Jean-Baptiste",
"Cap-Rouge",
"Cité-Universitaire",
"Vieux-Québec—Cap-Blanc—Colline parlementaire",
"Des Châtels",
"Duberger—Les Saules",
"L'Aéroport",
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
"Saint-Émile",
"Saint-Sacrement",
"Saint-Roch",
"Saint-Sauveur",
"Sillery",
"Val-Bélair",
"Vanier",
"Vieux-Moulin"]

quartier_quebec = "Saint-Sauveur"
polygone = []

with open("vdq-quartier.geojson.json") as f:
    data = json.load(f)
    for i in (data["features"]):
        # print(i["properties"]["NOM"])
        if i["properties"]["NOM"] == quartier_quebec:
            polygone = i["geometry"]["coordinates"]
            break
point_a_tester = []
data = ""
m=0
with open("vdq-panneauxstationnement.geojson") as f:
    data = json.load(f)
    n=0
    l = []
    for i in (data["features"]):
        m+=1
        point_a_tester = i["geometry"]["coordinates"]
        point_format_turfpy = Feature(geometry=Point(point_a_tester))
        polygone_format_turfpy = Polygon(polygone)
        if(boolean_point_in_polygon(point_format_turfpy, polygone_format_turfpy)) == True:
            l.append(i)
        else:
            n +=1
    data["features"] = l
# print(l)
# print(n,m)

outfile = "vdq-panneauxstationnement-filtred"+quartier_quebec+".geojson"
with open(outfile, mode="w") as f:
    json.dump(data, f)
print("filtrage termine")