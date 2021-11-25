import json 
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

arrondissements = [
"Outremont",
"LaSalle",
"Mont-Royal",
"Ville-Marie",
"Le Plateau-Mont-Royal",
"Hampstead",
"Le Sud-Ouest",
"Rivière-des-Prairies-Pointe-aux-Trembles",
"Lachine",
"Dorval",
"Montréal-Nord",
"L'Île-Bizard-Sainte-Geneviève",
"Kirkland",
"Dollard-des-Ormeaux",
"Senneville",
"Ahuntsic-Cartierville",
"Côte-Saint-Luc",
"Saint-Léonard",
"Montréal-Ouest",
"Pointe-Claire",
"L'Île-Dorval",
"Mercier-Hochelaga-Maisonneuve",
"Côte-des-Neiges-Notre-Dame-de-Grâce",
"Rosemont-La Petite-Patrie",
"Saint-Laurent",
"Beaconsfield",
"Villeray-Saint-Michel-Parc-Extension",
"Westmount",
"Montréal-Est",
"Anjou",
"Pierrefonds-Roxboro",
"Sainte-Anne-de-Bellevue",
"Verdun",
"Baie-d'Urfé"
]

'''
plaza -- in:  694 , out:  17632 , total:  18326
filtrage terminé
Outremont -- in:  615 , out:  17711 , total:  18326
filtrage terminé
LaSalle -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Mont-Royal -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Ville-Marie -- in:  7372 , out:  10954 , total:  18326
filtrage terminé
Le Plateau-Mont-Royal -- in:  3803 , out:  14523 , total:  18326
filtrage terminé
Hampstead -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Le Sud-Ouest -- in:  658 , out:  17668 , total:  18326
filtrage terminé
Rivière-des-Prairies-Pointe-aux-Trembles -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Lachine -- in:  218 , out:  18108 , total:  18326
filtrage terminé
Dorval -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Montréal-Nord -- in:  0 , out:  18326 , total:  18326
filtrage terminé
L'Île-Bizard-Sainte-Geneviève -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Kirkland -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Dollard-des-Ormeaux -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Senneville -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Ahuntsic-Cartierville -- in:  338 , out:  17988 , total:  18326
filtrage terminé
Côte-Saint-Luc -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Saint-Léonard -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Montréal-Ouest -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Pointe-Claire -- in:  0 , out:  18326 , total:  18326
filtrage terminé
L'Île-Dorval -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Mercier-Hochelaga-Maisonneuve -- in:  517 , out:  17809 , total:  18326
filtrage terminé
Côte-des-Neiges-Notre-Dame-de-Grâce -- in:  1435 , out:  16891 , total:  18326
filtrage terminé
Rosemont-La Petite-Patrie -- in:  1508 , out:  16818 , total:  18326
filtrage terminé
Saint-Laurent -- in:  191 , out:  18135 , total:  18326
filtrage terminé
Beaconsfield -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Villeray-Saint-Michel-Parc-Extension -- in:  788 , out:  17538 , total:  18326
filtrage terminé
Westmount -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Montréal-Est -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Anjou -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Pierrefonds-Roxboro -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Sainte-Anne-de-Bellevue -- in:  0 , out:  18326 , total:  18326
filtrage terminé
Verdun -- in:  883 , out:  17443 , total:  18326
filtrage terminé
Baie-d'Urfé -- in:  0 , out:  18326 , total:  18326
filtrage terminé
'''

'''
    Pour filtrer tous les arrondissements en même temps
'''

DATA_PATH = "data/"

def filter_mtl(arronds=["Rosemont-La Petite-Patrie"], specific_arrond=""):
    l_out_file = []
    for i in arronds:
        arrondissement_montreal = i
        polygone = []

        # PLAZA
        if arrondissement_montreal == "plaza":
            file_to_open = DATA_PATH + "plaza-saint-hubert.geojson"
            with open(file_to_open) as f:
                data = json.load(f)
                polygone = data["features"][0]["geometry"]["coordinates"]
                        
                # for i in (data["features"]):
                #     if i["properties"]["Name"] == "Oasis bellechasse+ plaza":
                #         polygone = i["geometry"]["coordinates"]
                #         break
        else:
            file_to_open = DATA_PATH + "quartiers_arrodissement_villemarie.geojson" if specific_arrond == "Ville-Marie" else DATA_PATH + "limadmin.geojson.json"
            with open(file_to_open) as f:
                data = json.load(f)
                for i in (data["features"]):
                    if i["properties"]["NOM"] == arrondissement_montreal:
                        polygone = i["geometry"]["coordinates"][0] if specific_arrond != "Ville-Marie" else i["geometry"]["coordinates"]
                        break

        point_a_tester = []
        data = ""
        m=0
        # file_to_open = "signalisation_stationnement.geojson"
        file_to_open = DATA_PATH + "places_with_reglementations.geojson"
        with open(file_to_open) as f:
            data = json.load(f)
            n=0
            p =0
            l = []
            for i in (data["features"]):
                m+=1
                point_a_tester = i["geometry"]["coordinates"]
                # print(i["properties"]["nPositionCentreLongitude"])
                # print(point_a_tester)
                point_format_turfpy = Feature(geometry=Point(point_a_tester))
                polygone_format_turfpy = Polygon(polygone)
                if(boolean_point_in_polygon(point_format_turfpy, polygone_format_turfpy)) == True:
                    l.append(i)
                    p += 1
                else:
                    n += 1
            data["features"] = l
        print(arrondissement_montreal, "-- in: ", p, ", out: ", n, ", total: ", m)
        if arrondissement_montreal == "plaza":
            outfile = "mtl-parco-" + "places-oasis-bellechasse-plaza".replace(" ","-").replace("+","-") + ".filtred.geojson"
        else:
            outfile = "mtl-parco-" + arrondissement_montreal.replace(" ","-").replace("+","-") + ".filtred.geojson"
        
        with open(DATA_PATH + outfile, mode="w") as f:
            json.dump(data, f)
        print("filtrage terminé")

        l_out_file.append(outfile)
            
    return l_out_file
    