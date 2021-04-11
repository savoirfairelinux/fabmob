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
Outremont -- in:  628 , out:  18115 , total:  18743
LaSalle -- in:  0 , out:  18743 , total:  18743
Mont-Royal -- in:  0 , out:  18743 , total:  18743
Ville-Marie -- in:  7728 , out:  11015 , total:  18743
Le Plateau-Mont-Royal -- in:  3801 , out:  14942 , total:  18743
Hampstead -- in:  0 , out:  18743 , total:  18743
Le Sud-Ouest -- in:  698 , out:  18045 , total:  18743
Rivière-des-Prairies-Pointe-aux-Trembles -- in:  0 , out:  18743 , total:  18743
Lachine -- in:  220 , out:  18523 , total:  18743
Dorval -- in:  0 , out:  18743 , total:  18743
Montréal-Nord -- in:  0 , out:  18743 , total:  18743
L'Île-Bizard-Sainte-Geneviève -- in:  0 , out:  18743 , total:  18743
Kirkland -- in:  0 , out:  18743 , total:  18743
Dollard-des-Ormeaux -- in:  0 , out:  18743 , total:  18743
Senneville -- in:  0 , out:  18743 , total:  18743
Ahuntsic-Cartierville -- in:  338 , out:  18405 , total:  18743
Côte-Saint-Luc -- in:  0 , out:  18743 , total:  18743
Saint-Léonard -- in:  0 , out:  18743 , total:  18743
Montréal-Ouest -- in:  0 , out:  18743 , total:  18743
Pointe-Claire -- in:  0 , out:  18743 , total:  18743
L'Île-Dorval -- in:  0 , out:  18743 , total:  18743
Mercier-Hochelaga-Maisonneuve -- in:  518 , out:  18225 , total:  18743
Côte-des-Neiges-Notre-Dame-de-Grâce -- in:  1435 , out:  17308 , total:  18743
Rosemont-La Petite-Patrie -- in:  1512 , out:  17231 , total:  18743
Saint-Laurent -- in:  191 , out:  18552 , total:  18743
Beaconsfield -- in:  0 , out:  18743 , total:  18743
Villeray-Saint-Michel-Parc-Extension -- in:  790 , out:  17953 , total:  18743
Westmount -- in:  0 , out:  18743 , total:  18743
Montréal-Est -- in:  0 , out:  18743 , total:  18743
Anjou -- in:  0 , out:  18743 , total:  18743
Pierrefonds-Roxboro -- in:  0 , out:  18743 , total:  18743
Sainte-Anne-de-Bellevue -- in:  0 , out:  18743 , total:  18743
Verdun -- in:  884 , out:  17859 , total:  18743
Baie-d'Urfé -- in:  0 , out:  18743 , total:  18743
filtrage terminé
'''

'''
    Pour filtrer tous les arrondissements en même temps
'''

PATH = "data/"

def filter_mtl(arronds=["Rosemont-La Petite-Patrie"]):
    l_out_file = []
    for i in arronds:
        # if arrond == "all":
        #     arrondissement_montreal = i
        # else:
        #     arrondissement_montreal = "Rosemont-La Petite-Patrie"
        arrondissement_montreal = i
        polygone = []

        
        # PLAZA
        if arrondissement_montreal == "plaza":
            file_to_open = PATH + "plaza_rosemont.geojson"
            with open(file_to_open) as f:
                data = json.load(f)
                for i in (data["features"]):
                    if i["properties"]["Name"] == "Oasis bellechasse+ plaza":
                        polygone = i["geometry"]["coordinates"]
                        break
        else:
            file_to_open = PATH + "limadmin.geojson.json"
            with open(file_to_open) as f:
                data = json.load(f)
                for i in (data["features"]):
                    if i["properties"]["NOM"] == arrondissement_montreal:
                        polygone = i["geometry"]["coordinates"][0]
                        break

        point_a_tester = []
        data = ""
        m=0
        # file_to_open = "signalisation_stationnement.geojson"
        file_to_open = PATH + "places_with_reglementations.geojson"
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
        # print(polygone)
        # print(l)
        print(arrondissement_montreal, "-- in: ", p, ", out: ", n, ", total: ", m)
        if arrondissement_montreal == "plaza":
            outfile = "mtl-parco-" + "places-oasis-bellechasse-plaza".replace(" ","-").replace("+","-") + ".filtred.geojson"
        else:
            outfile = "mtl-parco-" + arrondissement_montreal.replace(" ","-").replace("+","-") + ".filtred.geojson"
        
        with open(PATH + outfile, mode="w") as f:
            json.dump(data, f)
        print("filtrage terminé")

        l_out_file.append(outfile)
        
        # if arrond != "all"
        #     break          
    return l_out_file
    