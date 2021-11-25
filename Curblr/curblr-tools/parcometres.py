#%%
import wget
import requests
import csv
import json
import math
import os
from datetime import datetime, date
from typing import Optional
#from varname import name
from geojson import Feature, FeatureCollection, Point

'''
parcometres de la ville de Montreal
https://donnees.montreal.ca/agence-de-mobilite-durable/stationnements-municipaux-tarifes-sur-rue-et-hors-rue
'''

places_url  = "https://www.agencemobilitedurable.ca/images/data/Places.csv"
reglementations_url = "https://www.agencemobilitedurable.ca/images/data/Reglementations.csv"
emplacement_reglementations_url = "https://www.agencemobilitedurable.ca/images/data/EmplacementReglementation.csv"
reglementation_periode_url = "https://www.agencemobilitedurable.ca/images/data/ReglementationPeriode.csv"
periodes_url = "https://www.agencemobilitedurable.ca/images/data/Periodes.csv"
bornes_sur_rue = "https://www.agencemobilitedurable.ca/images/data/BornesSurRue.csv"
bornes_hors_rue = "https://www.agencemobilitedurable.ca/images/data/BornesHorsRue.csv"
date_exportation = "https://www.agencemobilitedurable.ca/images/data/DateExportation.csv"

urls = [
    places_url,
     reglementations_url,
      emplacement_reglementations_url,
       reglementation_periode_url,
        periodes_url,
         bornes_sur_rue,
          bornes_hors_rue,
           date_exportation
           ]

urls_name = [
    "places",
     "reglementatbions",
      "emplacement_reglementations",
       "reglementation_periode",
        "periodes",
         "bornes_sur_rue",
          "bornes_hors_rue",
           "date_exportation"
           ]

'''
    Téléchargment des différents fichiers de données
'''

#places
PATH = "data/"
try:
    os.mkdir(PATH)
except OSError:
    print ("Creation of the directory %s failed" % PATH)

def get_files():
    for i, url in enumerate(urls):
        r = requests.get(url, stream = True)
        file_name = urls_name[i] + ".csv"
        with open(PATH + file_name, "wb") as f:
            for chunk in r.iter_content(chunk_size = 1024):
                if chunk:
                    f.write(chunk)

'''
    Conversion des différents fichiers .csv au format geojson
'''
def emplacement_reglementations_to_dic(url_name):
    # file_name = PATH + urls_name[2] + ".csv"
    file_name = url_name + ".csv"
    dic = {}
    with open(PATH + file_name, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # sNoEmplacement,sCodeAutocollant
        l_tuple = []
        first_ligne = False
        for ligne in reader:
            if first_ligne == False:
                first_ligne = True
                continue
            dic[ligne[0]] = {"sCodeAutocollant_Name":[]}
            l_tuple.append((ligne[0], ligne[1]) )
        for tp in l_tuple:
            dic[tp[0]]["sNoEmplacement"] = tp[0]
            dic[tp[0]]["sCodeAutocollant_Name"].append(tp[1])
    return dic

def reglementations_to_dic(url_name, dateTime_reservation:Optional[datetime]=None, minStay=None):#TODO minStay - pas forcement utile, l'interface le fait deja
    # file_name = PATH + urls_name[1] + ".csv"
    file_name = url_name + ".csv"
    dic = {}
    with open(PATH + file_name, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Name,Type,DateDebut,DateFin,maxHeures
        l_tuple = []
        first_ligne = False
        for ligne in reader:
            maxHeures = ligne[4]
            if dateTime_reservation is not None:
                if first_ligne == False:
                    first_ligne = True
                    continue
                #TODO dateTime and minStay
                day_begin = int(ligne[2][:2])
                month_begin = int(ligne[2][2:])

                date_begin = date(dateTime_reservation.year, month_begin, day_begin)
                day_end = int(ligne[3][:2])
                month_end = int(ligne[3][2:])
                date_end = date(dateTime_reservation.year, month_end, day_end)
                day_reservation = dateTime_reservation.day
                month_reservation = dateTime_reservation.month
                weekday_reservation = dateTime_reservation.weekday()

                dateTime_reservation = date(dateTime_reservation.year, dateTime_reservation.month, dateTime_reservation.day)
                print("FILTERING",
                day_begin,
                month_begin,
                day_end,
                    month_end,
                    maxHeures,
                    day_reservation,
                    month_reservation,
                        weekday_reservation)
                if (dateTime_reservation<=date_end and dateTime_reservation>=date_begin):#todoMaxHeures
                    dic[ligne[0]] = {"Name":ligne[0], "Type":ligne[1], "DateDebut":ligne[2], "DateFin":ligne[3], "maxHeures": maxHeures}
            else:
                dic[ligne[0]] = {"Name":ligne[0], "Type":ligne[1], "DateDebut":ligne[2], "DateFin":ligne[3], "maxHeures": maxHeures}

    return dic

def reglementations_periode_to_dic(url_name):
    # file_name = PATH + urls_name[3] + ".csv"
    file_name = url_name + ".csv"
    dic = {}
    with open(PATH + file_name, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # sCode,noPeriode,sDescription
        l_tuple = []
        first_ligne = False
        for ligne in reader:
            if first_ligne == False:
                first_ligne = True
                continue
            dic[ligne[0]] = {"sub_prop":[]}
            l_tuple.append( (ligne[0], ligne[1], ligne[2]) )
        for tp in l_tuple:
            dic[tp[0]]["sCode"] = tp[0]
            dic[tp[0]]["sub_prop"].append({"noPeriode": tp[1], "sDescription":tp[2]})
    return dic

def periodes_to_dic(url_name, dateTime_reservation:Optional[datetime]=None):
    # file_name = PATH + urls_name[4] + ".csv"
    file_name = url_name + ".csv"
    dic = {}
    with open(PATH + file_name, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # nID,dtHeureDebut,dtHeureFin,bLun,bMar,bMer,bJeu,bVen,bSam,bDim

        l_tuple = []
        first_ligne = False
        if dateTime_reservation is not None:
            weekday = dateTime_reservation.weekday() #TODO weekday - pas forcement utile, l'interface le fait deja
            # print("weekday", weekday)
        for ligne in reader:
            if first_ligne == False:
                first_ligne = True
                continue
            dic[ligne[0]] = {
                "nID":ligne[0],
                 "dtHeureDebut":ligne[1],
                  "dtHeureFin":ligne[2],
                   "bLun":ligne[3],
                    "bMar":ligne[4],
                    "bMer":ligne[5],
                    "bJeu":ligne[6],
                    "bVen":ligne[7],
                    "bSam":ligne[8],
                    "bDim":ligne[9]
                    }
    return dic


'''
    conversion de places.csv en geojson + ajout des réglementations(association de tous les autres fichiers)
    
    https://www.agencemobilitedurable.ca/fr/informations/donnees-ouvertes/description-des-donnees-disponibles.html

'''
def convert_places(dateTime_reservation:Optional[datetime]=None, price=None, minStay=None):#TODO Parameters for polygon filter, price - pas forcement necessaire
    features = []
    file_name = urls_name[0] + ".csv"
    with open(PATH + file_name, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # sNoPlace, nLongitude, nLatitude, nPositionCentreLongitude, nPositionCentreLatitude,
        # sStatut, sGenre, sType, sAutreTete, sNomRue, nSupVelo, sTypeExploitation, nTarifHoraire, sLocalisation, nTarifMax
        for colonnes in reader:
            latitude = colonnes[2]
            longitude = colonnes[1]
            try:
                # print(latitude, longitude)
                latitude, longitude = map(float, (latitude, longitude))
                # print(latitude, longitude)
                # p = {"coordinates": [float(longitude), float(latitude)], "type": "Point"}
                # print(p)
                features.append(
                    Feature(
                        # geometry = p,
                        geometry = Point((longitude, latitude)),
                        properties = {
                            "sNoplace_sNoEmplacement": colonnes[0],
                            "nPositionCentreLongitude": colonnes[3],
                            "nPositionCentreLatitude": colonnes[4],
                            "sStatut": colonnes[5],
                            "sGenre": colonnes[6],
                            "sType": colonnes[7],
                            "sAutreTete": colonnes[8],
                            "sNomRue": colonnes[9],
                            "nSupVelo": colonnes[10],
                            "sTypeExploitation": colonnes[11],
                            "nTarifHoraire": colonnes[12],
                            "sLocalisation": colonnes[13],
                            "nTarifMax": colonnes[14] #TODO price
                        }
                    )
            )
            except ValueError: #petit hack pour sauter la premiere ligne du fichier csv
                pass
        # for val in features:
        #     val[]
    collection = FeatureCollection(features)
    r = ""

    '''
        Ajout des réglementations
    '''

    collection = add_reglementations(collection, dateTime_reservation, price, minStay)
    r = "_with_reglementations"
    file_name = urls_name[0] + r +".geojson"
    with open(PATH + file_name, "w") as f:
        f.write('%s' % collection)

def convert_bornes_sur_rue():
    features = []
    file_name = urls_name[5] + ".csv"
    with open(PATH + file_name, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # nNoBorne,sStatut,sNomRue,sZoneGroupeCode,nLongitude,nLatitude,sTypeExploitation
        
        for colonnes in reader:
            latitude = colonnes[5]
            longitude = colonnes[4]
            try:
                latitude, longitude = map(float, (latitude, longitude))
                features.append(
                    Feature(
                        geometry = Point((longitude, latitude)),
                        properties = {
                            "nNoBorne": colonnes[0],
                            "sStatut":colonnes[1],
                            "sNomRue":colonnes[2],
                            "sZoneGroupeCode":colonnes[3],
                            "sTypeExploitation":colonnes[6]
                        }
                    )
            )
            except ValueError: 
                pass
    collection = FeatureCollection(features)
    file_name = urls_name[5] + ".geojson"
    with open(PATH + file_name, "w") as f:
        f.write('%s' % collection)

def convert_bornes_hors_rue():
    features = []
    file_name = urls_name[6] + ".csv"
    with open(PATH + file_name, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # nNoBorne,sTerrain,sNomRuePrincipale,sStatut,nLongitude,nLatitude,Lun,Mar,Mer,Jeu,Ven,Sam,Dim,dtHeureDebutAP,dtHeureFinAP,nTarifHoraire,nMax
        for colonnes in reader:
            latitude = colonnes[5]
            longitude = colonnes[4]
            try:
                latitude, longitude = map(float, (latitude, longitude))
                features.append(
                    Feature(
                        geometry = Point((longitude, latitude)),
                        properties = {
                            "nNoBorne": colonnes[0],
                            "sTerrain": colonnes[1],
                            "sNomRuePrincipale": colonnes[2],
                            "sStatut": colonnes[3],
                            "Lun": colonnes[6],
                            "Mar": colonnes[7],
                            "Mer": colonnes[8],
                            "Jeu": colonnes[9],
                            "Ven": colonnes[10],
                            "Sam": colonnes[11],
                            "Dim": colonnes[12],
                            "dtHeureDebutAP":colonnes[13],
                            "dtHeureFinAP":colonnes[14],
                            "nTarifHoraire":colonnes[15],
                            "nMax":colonnes[16]
                        }
                    )
                )
            except ValueError:
                pass
    collection = FeatureCollection(features)
    file_name = urls_name[6] + ".geojson"
    with open(PATH + file_name, "w") as f:
        f.write('%s' % collection)

def add_reglementations(collection, dateTime_reservation=None, price=None, minStay=None):#TODO Parameters for polygon filter and tarif(max)vation, price, minStay):
    a = emplacement_reglementations_to_dic(urls_name[2]) 
    b = reglementations_to_dic(urls_name[1], dateTime_reservation, minStay)#TODO minStay - pas forcement utile, l'interface le fait deja
    c = reglementations_periode_to_dic(urls_name[3])
    d = periodes_to_dic(urls_name[4], dateTime_reservation)#TODO weekday - pas forcement utile, l'interface le fait deja
    
    for feature in collection["features"]:
        feature_properties = feature["properties"]
        sNoplace =  feature_properties["sNoplace_sNoEmplacement"]
        # print(sNoplace)
        sNoplace_from_dic = a[sNoplace]
        sCodeAutocollant_from_dic = a[sNoplace]["sCodeAutocollant_Name"]
        # print(sCodeAutocollant_from_dic)
        feature_properties["sCodeAutocollant_Name"] = {}
        feature_properties["liste_sCodeAutocollant_Name"] = sCodeAutocollant_from_dic
        for i in sCodeAutocollant_from_dic:
            # feature_properties["liste_sCodeAutocollant_Name"].append(i)
            try:
                feature_properties["sCodeAutocollant_Name"][i] = b[i]
                # print(feature_properties["sCodeAutocollant_Name"][i])
                feature_properties["sCodeAutocollant_Name"][i]["sub_prob"] = c[i]["sub_prop"]
                for j in feature_properties["sCodeAutocollant_Name"][i]["sub_prob"]:
                    nId = j["noPeriode"]
                    j["periodes"] = d[nId]
            except KeyError as e: #du au filtre selon le jour et le mois, certains autocollants disparaissent
                # print(e)
                pass
    return collection


'''
    Fonction principale dans la conversion en Curblr, ajout des regulations.
    Beaucoup de code commenté sont en fait les clés-valeurs facultatives. Je les ai laissés pour faciliter la tâche de conversion.
'''

def turn_regl_to_regu(buffered_file):
    with open(PATH + buffered_file) as f:
        data = json.load(f)
        geojson = {}
        geojson['manifest']= {
        "priorityHierarchy": [
                "no standing",
                "no parking",
                "passenger loading",
                "loading",
                "transit",
                "free parking",
                "paid parking", 
                "restricted"
        ],
        "curblrVersion": "1.1.0",
        }
        geojson['type'] = 'FeatureCollection'
        geojson['features'] = []
        
        p = 0
        for feature in data['features']:
            try:
                # print(feature)
                regulations = []
                n = 0
                feature_properties = feature["properties"]
                for autocollant in feature_properties["pp_liste_scodeautocollant_name"]: 
                    durations = [int(value["maxHeures"])*60 for value in feature_properties["pp_scodeautocollant_name"].values()]
                    sub_prob = feature_properties["pp_scodeautocollant_name"][autocollant]
                    regulation = {}    
                    regulation["rule"] = { #https://github.com/curblr/curblr-spec/blob/master/Rule.md
                                            "activity": "parking", #parking, no parking, standing, no standing, loading, no loading
                                            "priority": "paid parking",
                                            "maxStay": max(durations),
                                            # "reason": "construction",
                                            # "noReturn": 240,
                                            "payment": True #
                                        }
                    regulation["userClasses"] = [#https://github.com/curblr/curblr-spec/blob/master/UserClasses.md
                                        {
                                            # "classes": ["permit"],
                                            # "subclasses": ["zone 5"]
                                        }
                                    ]
                    regulation["timeSpans"] = []
                    
                    # print(feature_properties["pp_scodeautocollant_name"][autocollant]["sub_prob"])
                    for sub_prob in feature_properties["pp_scodeautocollant_name"][autocollant]["sub_prob"]:
                        days = []
                        
                        if sub_prob["periodes"]["bLun"] == "1":
                            days.append("mo")
                        if sub_prob["periodes"]["bMar"] == "1":
                            days.append("tu")
                        if sub_prob["periodes"]["bMer"] == "1":
                            days.append("we")
                        if sub_prob["periodes"]["bJeu"] == "1":
                            days.append("th")
                        if sub_prob["periodes"]["bVen"] == "1":
                            days.append("fr")
                        if sub_prob["periodes"]["bSam"] == "1":
                            days.append("sa")
                        if sub_prob["periodes"]["bDim"] == "1":
                            days.append("su")
                        timeSpan = {
                            "daysOfWeek": {
                                "days": days 
                                # [
                                #     "mo","tu", "we","th","fr","sa"
                                    
                                # ],
                                # "occurrencesInMonth": ["2nd", "4th"]
                            },
                            "timesOfDay": [
                                {
                                    "from": sub_prob["periodes"]["dtHeureDebut"][:5],#couper les secondes
                                    "to": sub_prob["periodes"]["dtHeureFin"][:5]
                                    # "from": "07:00",
                                    # "to": "19:00"
                                }
                            ],
                            # "designated 
                            "effectiveDates": [
                                {
                                    "from": feature_properties["pp_scodeautocollant_name"][autocollant]["DateDebut"][2:]+"-"+ feature_properties["pp_scodeautocollant_name"][autocollant]["DateDebut"][:2],
                                    "to":  feature_properties["pp_scodeautocollant_name"][autocollant]["DateFin"][2:]+"-"+ feature_properties["pp_scodeautocollant_name"][autocollant]["DateFin"][:2]
                                }
                                # {"from": "12-01", "to": "12-31"},
                                # {"from": "01-01", "to": "03-31"}
                            ],
                        }
                        a = feature_properties["pp_snoplace_snoemplacement"]
                        # if a == "RB133":#TODO: DEBUG PARCO
                            # print(p, " ", a," - " ,n, " ", autocollant,  ": ", timeSpan) 
                        regulation["timeSpans"].append(timeSpan)
                        regulation["payment"] = {#https://github.com/curblr/curblr-spec/blob/master/Payment.md
                                        "rates": [
                                            {
                                                "fees": [
                                                    # 0.5
                                                    float(feature_properties["pp_ntarifhoraire"])/100
                                                ],
                                                "durations": durations
                                                # [
                                                #     # 15
                                                #     float()
                                                # ]
                                            }
                                        ],
                                        "methods": [
                                            "pay_station",
                                            # "digital"
                                        ],
                                        "forms": [
                                            "Visa",
                                            "Mastercard",
                                            # "American Express",
                                            # "Smart Card",
                                            # "coins",
                                            # "Parking Kitty"
                                        ],
                                        # "phone": "+15032785410",
                                        # "operator": "PBOT",
                                        # "deviceIds": [
                                        #     "zone 1002"
                                        # ]
                                    }
                    regulations.append(regulation)
                    n += 1
                    # break#
                geojson['features'].append(
                    {
                        "type": feature["type"],
                        "properties": {
                            "location":{
                                "shstRefId": feature_properties["referenceId"],
                                "sideOfStreet": feature_properties["sideOfStreet"],
                                "shstLocationStart": round(feature_properties["section"][0]), #Math.round
                                "shstLocationEnd": round(feature_properties["section"][1]),
                                # "referenceLength": feature_properties["referenceLength"],
                                "assetType": feature_properties["pp_stypeexploitation"], 
                                # "baysAngle": "parallel",
                                # "objectId": "94022",
                                # "derivedFrom": ["sign_820", "sign_028", "sign-940"],
                                # "assetType": "sign",
                                "streetName": feature_properties["pp_snomrue"],
                                # "status": "proposed"
                            },
                            "regulations": regulations
                        },
                        "geometry": feature["geometry"],
                        # "images": [
                        #     "https://fordspacesdev.blob.core.windows.net/images/DA877882-E220-4A8B-A7C1-69D446C43CD8"
                        #     ]

                    }
                )
                p += 1
            except KeyError as e:
                pass
                # print(e)
                # print("Pas de match pour,", buffered_file, ". Fichier buffered probablement vide ou clé inexistante")
            except TypeError as e: 
                print("Il n'y aura pas de match pour", buffered_file, "car la propriété 'geometry' du fichier manque probablement")
                print("Type error", e)
                
    outfile = buffered_file.replace(".buffered.geojson", ".curblr.json")
    # outfile = "last_converted.curblr.json"
    # outfile = "last_converted_all.curblr.json"
    
    with open(PATH + outfile, mode="w") as f:
        # print(2,outfile)
        json.dump(geojson, f)
        # print(3,outfile)
    return outfile, geojson
# %%

'''
    [
        {
            "rule": { #https://github.com/curblr/curblr-spec/blob/master/Rule.md
                "activity": "parking",
                "priorityCategory": "5",
                # "maxStay": 30,
                # "reason": "construction",
                # "noReturn": 240,
                "payment": True #
            },
            "userClasses": [#https://github.com/curblr/curblr-spec/blob/master/UserClasses.md
                {
                    # "classes": ["permit"],
                    # "subclasses": ["zone 5"]
                },
            ],
            "timeSpans": [#https://github.com/curblr/curblr-spec/blob/master/TimeSpans.md
                {
                    "daysOfWeek": {
                        "days": [
                            "mo","tu", "we","th","fr","sa"
                        ],
                        "occurrencesInMonth": ["2nd", "4th"]
                    },
                    "timesOfDay": [
                        {
                            "from": "07:00",
                            "to": "19:00"
                        }
                    ],
                    "designatedPeriods": [
                        {
                            "name": "holidays",
                            "apply": "except during"
                        }
                    ],
                    "effectiveDates": [
                        {"from": "12-01", "to": "12-31"},
                        {"from": "01-01", "to": "03-31"}
                    ],
                }
            ],
            "payment": {#https://github.com/curblr/curblr-spec/blob/master/Payment.md
                "rates": [
                    {
                        "fees": [
                            # 0.5

                        ],
                        "durations": [
                            15
                        ]
                    }
                ],
                "methods": [
                    "pay_station",
                    "digital"
                ],
                "forms": [
                    "Visa",
                    "Mastercard",
                    "American Express",
                    "Smart Card",
                    "coins",
                    "Parking Kitty"
                ],
                "phone": "+15032785410",
                "operator": "PBOT",
                "deviceIds": [
                    "zone 1002"
                ]
            }
        }
    ]
'''
# %%
