import requests
import json
import os
import io
import base64

from requests.auth import HTTPBasicAuth
from typing import Optional
from datetime import datetime, date
from geojson import Feature, FeatureCollection, Point, Polygon, geometry
from turfpy.measurement import boolean_point_in_polygon
from pydrive_logic import *

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

arrondissements = [
    "plaza",
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
    liste de clés pour faciliter le refactoring en cas de changement dans l'API
    exemple: dans l'ancienne API, toutes les clés étaient en majuscule
'''

DATA_PATH = "data/"
k_geometry = "geometry".lower()
k_coordinates = "coordinates".lower()
k_nlongitude = "NLONGITUDE".lower()
k_nlatitude = "NLATITUDE".lower()
k_sno_emplacement = "SNO_EMPLACEMENT".lower()
k_scodeautocollant = "SCODE_AUTOCOLLANT".lower()
k_maxheures = "MAXHEURES".lower()
k_datedebut = "DATEDEBUT".lower()
k_datefin = "DATEFIN".lower()
k_sNoplace_sNoEmplacement = "SNOPLACE".lower()
k_nPositionCentreLongitude = "NPOSITIONCENTRELONGITUDE".lower()
k_nPositionCentreLatitude = "NPOSITIONCENTRELATITUDE".lower()
k_sStatut = "SSTATUT".lower()
k_sGenre = "SGENRE".lower()
k_sType = "STYPE".lower()
k_sAutreTete = "SAUTRETETE".lower()
k_sNomRue = "SNOMRUE".lower()
k_nSupVelo = "NSUPVELO".lower()
k_sTypeExploitation = "STYPEEXPLOITATION".lower()
k_nTarifHoraire = "NTARIFHORAIRE".lower()
k_sLocalisation = "SLOCALISATION".lower()
k_nTarifMax = "NTARIFMAX".lower()
k_name = "NAME".lower()
k_type = "TYPE".lower()
k_scode = "SCODE".lower()
k_noperiode = "NOPERIODE".lower()
k_sdescription = "SDESCRIPTION".lower()
k_nid = "NID".lower()
k_dtheuredebut = "DTHEUREDEBUT".lower()
k_dtheurefin = "DTHEUREFIN".lower()
k_blun = "BLUN".lower()
k_bmar = "BMAR".lower()
k_bmer = "BMER".lower()
k_bjeu = "BJEU".lower()
k_bven = "BVEN".lower()
k_bsam = "BSAM".lower()
k_bdim = "BDIM".lower()


def filter_mtl(places_collection_wr, arrondissements=["plaza"]):
    # l_out_file = []
    dic = {}
    for arrond in arrondissements:
        polygone = []

        # PLAZA
        if arrond == "plaza":
            file_to_open = DATA_PATH + "plaza-saint-hubert.geojson"  # "plaza_rosemont.geojson"
            with open(file_to_open) as f:
                data = json.load(f)
                polygone = data["features"][0]["geometry"]["coordinates"]
                # for i in (data["features"]):
                # if i["properties"]["Name"] == "Oasis bellechasse+ plaza":
                # polygone = i["geometry"]["coordinates"]
                # break
        else:
            file_to_open = DATA_PATH + "limadmin.geojson.json"
            with open(file_to_open) as f:
                data = json.load(f)
                for feature in (data["features"]):
                    if feature["properties"]["NOM"] == arrond:
                        polygone = feature["geometry"]["coordinates"][0]
                        break
        point_a_tester = []
        data = ""
        # file_to_open = "signalisation_stationnement.geojson"
        data = {}
        data["type"] = places_collection_wr["type"]
        '''
            m,n,p pour faciliter le debogage des filtres. Montre les points retenus et exclus.
        '''
        m = 0
        n = 0
        p = 0
        filtered_features = []
        for feature in (places_collection_wr["features"]):
            m += 1
            point_a_tester = feature[k_geometry][k_coordinates]
            point_format_turfpy = Feature(geometry=Point(point_a_tester))
            polygone_format_turfpy = Polygon(polygone)
            if(boolean_point_in_polygon(point_format_turfpy, polygone_format_turfpy)) == True:
                filtered_features.append(feature)
                p += 1
            else:
                n += 1

        data["features"] = filtered_features
        print(arrond, " <-> in:", p, ", out:", n, ", total:", m)

        if arrond == "plaza":
            outfile = "mtl-parco-" + \
                "places-oasis-bellechasse-plaza".replace(
                    " ", "-").replace("+", "-") + ".filtred.geojson"
        else:
            outfile = "mtl-parco-" + \
                arrond.replace(" ", "-").replace("+", "-") + ".filtred.geojson"

        # with open(DATA_PATH + outfile, mode="w") as f:
        #     json.dump(data, f)
        # print("filtrage terminé")

        # l_out_file.append(outfile)
        dic[outfile] = data
    return dic  # l_out_file


def convert_places(data, dateTime_reservation: Optional[datetime] = None,
                   price=None,
                   minStay=None):  # TODO Parameters for polygon filter, price - pas forcement necessaire
    features = []
    # sNoPlace, nLongitude, nLatitude, nPositionCentreLongitude, nPositionCentreLatitude,
    # sStatut, sGenre, sType, sAutreTete, sNomRue, nSupVelo, sTypeExploitation, nTarifHoraire, sLocalisation, nTarifMax
    data = data["data"]
    for place in data:
        longitude = place[k_nlongitude]
        latitude = place[k_nlatitude]
        try:
            latitude, longitude = map(float, (latitude, longitude))
            geom = Point((longitude, latitude))
            features.append(
                Feature(
                    # geometry = p,
                    geometry=geom,
                    properties={
                        "sNoplace_sNoEmplacement": place[k_sNoplace_sNoEmplacement],
                        "nPositionCentreLongitude": place[k_nPositionCentreLongitude],
                        "nPositionCentreLatitude": place[k_nPositionCentreLatitude],
                        "sStatut": place[k_sStatut],
                        "sGenre": place[k_sGenre],
                        "sType": place[k_sType],
                        "sAutreTete": place[k_sAutreTete],
                        "sNomRue": place[k_sNomRue],
                        "nSupVelo": place[k_nSupVelo],
                        "sTypeExploitation": place[k_sTypeExploitation],
                        "nTarifHoraire": place[k_nTarifHoraire],
                        "sLocalisation": place[k_sLocalisation],
                        "nTarifMax": place[k_nTarifMax],
                        "original_geometry": geom
                    }
                )
            )
        except ValueError:  # petit hack pour sauter la premiere ligne du fichier csv
            pass
    collection = FeatureCollection(features)
    return collection


def add_reglementations(data_geo_empl_reglementations,
                        data_geo_reglementations,
                        data_geo_regl_periods,
                        data_geo_periods,
                        collection,
                        dateTime_reservation=None,
                        price=None,
                        minStay=None):  # TODO Parameters for polygon filter and tarif(max)vation, price, minStay):

    for feature in collection["features"]:
        feature_properties = feature["properties"]
        sNoplace = feature_properties["sNoplace_sNoEmplacement"]
        try:
            sNoplace_from_dic = data_geo_empl_reglementations[sNoplace]
        except Exception as e:
            print("add_reglementations, exception: ", e)
            continue
        sCodeAutocollant_from_dic = data_geo_empl_reglementations[sNoplace]["sCodeAutocollant_Name"]
        feature_properties["sCodeAutocollant_Name"] = {}
        feature_properties["liste_sCodeAutocollant_Name"] = sCodeAutocollant_from_dic

        for i in sCodeAutocollant_from_dic:
            try:
                feature_properties["sCodeAutocollant_Name"][i] = data_geo_reglementations[i]
                feature_properties["sCodeAutocollant_Name"][i]["sub_prob"] = data_geo_regl_periods[i]["sub_prop"]
                for j in feature_properties["sCodeAutocollant_Name"][i]["sub_prob"]:
                    nId = j["noPeriode"]
                    j["periodes"] = data_geo_periods[nId]
            except KeyError as e:  # du au filtre selon le jour et le mois, certains autocollants disparaissent
                # print(e)
                pass
    return collection


'''
    Conversion des différentes donnees au format geojson
'''


def emplacement_reglementations_to_dic(data):
    # sNoEmplacement,sCodeAutocollant
    dic = {}
    l_tuple = []
    first_ligne = False
    data = data["data"]
    for ligne in data:
        if first_ligne == False:
            first_ligne = True
            continue
        dic[ligne[k_sno_emplacement]] = {"sCodeAutocollant_Name": []}
        l_tuple.append((ligne[k_sno_emplacement], ligne[k_scodeautocollant]))
    for tp in l_tuple:
        dic[tp[0]]["sNoEmplacement"] = tp[0]
        dic[tp[0]]["sCodeAutocollant_Name"].append(tp[1])

    return dic


# TODO minStay - pas forcement utile, l'interface le fait deja
def reglementations_to_dic(data, dateTime_reservation: Optional[datetime] = None, minStay=None):
    # Name,Type,DateDebut,DateFin,maxHeures
    dic = {}
    l_tuple = []
    first_ligne = False
    data = data["data"]
    for ligne in data:

        maxHeures = ligne[k_maxheures]
        if dateTime_reservation is not None:
            if first_ligne == False:
                first_ligne = True
                continue
            # TODO dateTime and minStay
            day_begin = int(ligne[k_datedebut][:2])
            month_begin = int(ligne[k_datedebut][2:])

            date_begin = date(dateTime_reservation.year,
                              month_begin, day_begin)
            day_end = int(ligne[k_datefin][:2])
            month_end = int(ligne[k_datefin][2:])
            date_end = date(dateTime_reservation.year, month_end, day_end)
            day_reservation = dateTime_reservation.day
            month_reservation = dateTime_reservation.month
            weekday_reservation = dateTime_reservation.weekday()

            dateTime_reservation = date(
                dateTime_reservation.year, dateTime_reservation.month, dateTime_reservation.day)
            print("FILTERING",
                  day_begin,
                  month_begin,
                  day_end,
                  month_end,
                  maxHeures,
                  day_reservation,
                  month_reservation,
                  weekday_reservation)
            if (dateTime_reservation <= date_end and dateTime_reservation >= date_begin):  # todoMaxHeures
                dic[ligne[k_name]] = {
                    "Name": ligne[k_name],
                    "Type": ligne[k_type],
                    "DateDebut": ligne[k_datedebut],
                    "DateFin": ligne[k_datefin],
                    "maxHeures": maxHeures
                }
        else:
            dic[ligne[k_name]] = {
                "Name": ligne[k_name],
                "Type": ligne[k_type],
                "DateDebut": ligne[k_datedebut],
                "DateFin": ligne[k_datefin],
                "maxHeures": maxHeures
            }

    return dic


def reglementations_periods_to_dic(data):
    # sCode,noPeriode,sDescription
    dic = {}
    l_tuple = []
    first_ligne = False
    data = data["data"]
    for ligne in data:
        if first_ligne == False:
            first_ligne = True
            continue

        dic[ligne[k_scode]] = {"sub_prop": []}
        l_tuple.append((ligne[k_scode], ligne[k_noperiode],
                       ligne[k_sdescription].encode('utf-8').decode()))

    L = {}  # debug
    n = 0  # debug
    for tp in l_tuple:
        l = []
        dic[tp[0]]["sCode"] = tp[0]
        dic[tp[0]]["sub_prop"].append(
            {"noPeriode": tp[1], "sDescription": tp[2]})

        L[str(n)] = tp[2].encode('utf-8').decode()  # debug
        n += 1  # debug
    with open("debugHeures.json", "w", encoding="utf-8") as f:  # debug
        L = {"desc": "ensemble de descriptions pour regex", "val": L}  # debug
        # print(L)
        json.dump(L, f)  # debug
    return dic  # debug


def periods_to_dic(data, dateTime_reservation: Optional[datetime] = None):
    # nID,dtHeureDebut,dtHeureFin,bLun,bMar,bMer,bJeu,bVen,bSam,bDim
    dic = {}
    l_tuple = []
    first_ligne = False
    if dateTime_reservation is not None:
        # TODO weekday - pas forcement utile, l'interface le fait deja
        weekday = dateTime_reservation.weekday()
        # print("weekday", weekday)
    data = data["data"]
    for ligne in data:
        if first_ligne == False:
            first_ligne = True
            continue

        dic[ligne[k_nid]] = {
            "nID": ligne[k_nid],
            "dtHeureDebut": ligne[k_dtheuredebut],
            "dtHeureFin": ligne[k_dtheurefin],
            "bLun": ligne[k_blun],
            "bMar": ligne[k_bmar],
            "bMer": ligne[k_bmer],
            "bJeu": ligne[k_bjeu],
            "bVen": ligne[k_bven],
            "bSam": ligne[k_bsam],
            "bDim": ligne[k_bdim]
        }
    return dic


def to_segment(data):
    # print(data)
    fleche_map = {
        "left": {
            'double': 2,  # no arrow -> middle
            'left': 3,    # left arrow -> end
            'right': 1
        },               # right arrow -> start
        "right": {
            'double': 2,  # no arrow -> middle
            'left': 1,    # left arrow -> start
            'right': 3    # right arrow -> end
        }
    }
    data_tw = data
    for feature in data_tw['features']:
        feature['geometry'] = feature['properties']['pp_original_geometry']
        try:
            feature['properties']["point_sequence"] = fleche_map[feature['properties']
                                                                 ["sideOfStreet"]][feature["properties"]["pp_fleche_pan"]]
        except:  # pas de fleche pan dans les data; ignorer
            pass

    return data_tw


def turn_regl_to_regu(current_file):
    with open(current_file, "r") as f:
        data = json.load(f)
        geojson = {}
        geojson['manifest'] = {
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

            # debug
            # noplace = feature['properties']['pp_snoplace_snoemplacement']
            # if noplace == "PN578":
            #     with open("debug"+noplace+".json", "w") as f:
            #         json.dump(feature, f)
            #     exit()

            try:
                regulations = []
                n = 0
                feature_properties = feature["properties"]
                for autocollant in feature_properties["pp_liste_scodeautocollant_name"]:
                    current_autocollant = feature_properties["pp_scodeautocollant_name"][autocollant]
                    regulation = {}
                    maxStay = current_autocollant["maxHeures"]*60
                    regulation["rule"] = {  # https://github.com/curblr/curblr-spec/blob/master/Rule.md
                                            "activity": "parking",  # parking, no parking, standing, no standing, loading, no loading
                                            "priority": "paid parking",
                                            "maxStay": maxStay,
                                            # "reason": "construction",
                                            # "noReturn": 240,
                                            "payment": True
                    }
                    regulation["userClasses"] = [  # https://github.com/curblr/curblr-spec/blob/master/UserClasses.md
                        {
                            # "classes": ["permit"],
                            # "subclasses": ["zone 5"]
                        }
                    ]
                    regulation["timeSpans"] = []

                    dateDebut = current_autocollant["DateDebut"][2:] + \
                        "-" + current_autocollant["DateDebut"][:2],
                    datefin = current_autocollant["DateFin"][2:] + \
                        "-" + current_autocollant["DateFin"][:2]
                    for sub_prob in current_autocollant["sub_prob"]:
                        days = []
                        periodes = sub_prob["periodes"]
                        if periodes["bLun"] == "1":
                            days.append("mo")
                        if periodes["bMar"] == "1":
                            days.append("tu")
                        if periodes["bMer"] == "1":
                            days.append("we")
                        if periodes["bJeu"] == "1":
                            days.append("th")
                        if periodes["bVen"] == "1":
                            days.append("fr")
                        if periodes["bSam"] == "1":
                            days.append("sa")
                        if periodes["bDim"] == "1":
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
                                    # couper les secondes
                                    "from": periodes["dtHeureDebut"][:5],
                                    "to": periodes["dtHeureFin"][:5]
                                    # "from": "07:00",
                                    # "to": "19:00"
                                }
                            ],
                            # "designated
                            "effectiveDates": [
                                {
                                    "from": dateDebut,
                                    "to":  datefin
                                }
                                # {"from": "12-01", "to": "12-31"},
                                # {"from": "01-01", "to": "03-31"}
                            ],
                        }
                        # a = feature_properties["pp_snoplace_snoemplacement"]
                        # if a == "RB133":#TODO: DEBUG PARCO
                        # print(p, " ", a," - " ,n, " ", autocollant,  ": ", timeSpan)
                        regulation["timeSpans"].append(timeSpan)
                        regulation["payment"] = {  # https://github.com/curblr/curblr-spec/blob/master/Payment.md
                            "rates": [
                                {
                                    "fees": [
                                        # 0.5
                                        float(
                                            feature_properties["pp_ntarifhoraire"])/100
                                    ],
                                    # "durations": durations
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
                    # voir types de reglementations page 4
                    # https://www.agencemobilitedurable.ca/images/DescriptionDonneesOuvertes.pdf
                    if current_autocollant["Type"] == "I":
                        '''
                            "ARRET INT. 16 h - 18 h 30 LUN À VEN" 
                        '''
                        regulation["rule"] = {  # https://github.com/curblr/curblr-spec/blob/master/Rule.md
                                                "activity": "no parking",  # parking, no parking, standing, no standing, loading, no loading
                                                "priority": "paid parking",
                                                "maxStay": maxStay,
                                                # "reason": "street cleaning",
                                                # "noReturn": 240,
                                                "payment": True
                        }
                        regulation["userClasses"] = [  # https://github.com/curblr/curblr-spec/blob/master/UserClasses.md
                            {
                                # "classes": ["permit"],
                                # "subclasses": ["zone 5"]
                            }
                        ]
                    if current_autocollant["Type"] == "R":
                        '''
                            R - Remorquage
                        '''
                        regulation["rule"] = { 
                                                "activity": "no parking",  # parking, no parking, standing, no standing, loading, no loading
                                                "priority": "paid parking",
                                                "maxStay": maxStay,
                                                # "noReturn": 240,
                                                "payment": True
                        }
                    if current_autocollant["Type"] == "E":
                        '''
                        E - Entretien
                        '''
                        regulation["rule"] = { 
                                                "activity": "no parking",  # parking, no parking, standing, no standing, loading, no loading
                                                "priority": "paid parking",
                                                "maxStay": maxStay,
                                                "reason": "street cleaning", #to verify
                                                # "noReturn": 240,
                                                "payment": True
                        }
                    if current_autocollant["Type"] == "A":
                        '''
                        Autre, Interdiction autre : balai mécanique 
                        ex: STAT. INT. 14 h 30 - 15 h 30 MER 01 avril au 01 déc
                        '''
                        regulation["rule"] = { 
                                                "activity": "no parking",  # parking, no parking, standing, no standing, loading, no loading
                                                "priority": "paid parking",
                                                "maxStay": maxStay,
                                                "reason": "other", #to verify
                                                # "noReturn": 240,
                                                "payment": True
                        }
                    if current_autocollant["Type"] == "P":
                        '''
                        MAX 3 h18 h - 21 h LUN A VEN
                        '''
                        pass
                    if current_autocollant["Type"] == "Q":
                        '''
                        MAX 3 h 9h - 18 h SAM et 13 h - 18 h DIM
                        '''
                        pass
                    if current_autocollant["Type"] == "V":
                        '''
                        9 h - 21 h AVEC MAX JOUR P$ 6 HEURES
                        '''
                        pass
                    if current_autocollant["Type"] == "M":
                        '''
                            Tarif max Journalier
                            ex: LUN À VEN 9 h - 18 h (9 $ MAX)
                        '''
                        pass
                    if current_autocollant["Type"] == "F":
                        '''
                        F - Utilisation - Tarification et durée fixe
                        '''
                        pass
                    if current_autocollant["Type"] == "U":
                        '''
                        U - Utilisation
                        '''
                        pass
                    if current_autocollant["Type"] == "H":
                        '''
                            Réservé aux personnes handicapées
                            ex: \\P  Réservé aux handicapés"
                        '''
                        regulation["userClasses"].append(# https://github.com/curblr/curblr-spec/blob/master/UserClasses.md
                            {
                                "classes": ["handicap"]
                            }
                        )
                    # break#
                geojson['features'].append(
                    {
                        "type": feature["type"],
                        "properties": {
                            "location": {
                                "shstRefId": feature_properties["referenceId"],
                                "sideOfStreet": feature_properties["sideOfStreet"],
                                # Math.round
                                "shstLocationStart": round(feature_properties["section"][0]),
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
                # print("turn_regl_to_regu, KeyError: ", e)
                # print("Pas de match pour,", current_file,
                #       ". Fichier buffered probablement vide ou clé inexistante")
                pass
            except TypeError as e:
                # print("turn_regl_to_regu, Il n'y aura pas de match pour", current_file,
                #       "car la propriété 'geometry' du fichier manque probablement")
                # print("Type error", e)
                pass

    # outfile = current_file.replace(".buffered.geojson", ".curblr.json")
    outfile = current_file.replace(".matched.geojson", ".curblr.json")

    # outfile = "laLégende
    # outfile = "last_converted_all.curblr.json"

    with open(outfile, mode="w") as f:
        # print(2,outfile)
        json.dump(geojson, f)
        # print(3,outfile)
    return outfile, geojson


def run(arronds=[arrondissements[0]], dateTime_reservation: Optional[datetime] = None, price=None, minStay=None):
    # uri_login = "http://52.235.16.115:8083/auth/signin" #old API
    uri_login = "https://jalonmtl.services/api/v1/auth/signin"
    body_login = {}
    with open('credits.json') as f:
        body_login = json.load(f)
    r_uri_login = requests.post(uri_login, json=body_login)
    token = ""
    if r_uri_login.status_code == 200:
        token = r_uri_login.json()["token"]
    headers = {"Authorization": "Bearer "+token,
               'Content-Type': 'application/json'}

    # print(r_uri_login, type(r_uri_login))

    # uri_select_data = "http://52.235.16.115:8083/dataAPI/selectData" #old API
    uri_select_data = "https://jalonmtl.services/api/v1/public/data"

    # ITER stg_stationnement_mtl_emplacement_reglementation
    body_emp_regl = {
        "table": "stg_stationnement_mtl_emplacement_reglementation",
        "recordsPerPage": "100000",
        "currentPage": "1"
    }

    # FULL stg_stationnement_mtl_periode
    body_period = {
        "table": "stg_stationnement_mtl_periode",
        "recordsPerPage": "100000",
        "currentPage": "1",
        "defaultReturnDateFormat": "HH:mm:ss"
    }

    # ITER stg_stationnement_mtl_place
    body_places = {
        "table": "stg_stationnement_mtl_place",
        "recordsPerPage": "100000",
        "currentPage": "1"
    }

    # FULL stg_stationnement_mtl_reglementation
    body_regl = {
        "table": "stg_stationnement_mtl_reglementation",
        "recordsPerPage": "100000",
        "currentPage": "1"
    }

    # FULL stg_stationnement_mtl_reglementation_periode
    body_regl_period = {
        "table": "stg_stationnement_mtl_reglementation_periode",
        "recordsPerPage": "100000",
        "currentPage": "1"
    }

    r_uri_select_data = requests.post(
        uri_select_data, json=body_emp_regl, headers=headers)
    data_empl_reglementations = r_uri_select_data.json()
    # print(data_empl_reglementations)

    r_uri_select_data = requests.post(
        uri_select_data, json=body_period, headers=headers)
    data_periods = r_uri_select_data.json()

    r_uri_select_data = requests.post(
        uri_select_data, json=body_places, headers=headers)
    data_places = r_uri_select_data.json()
    # print(data_places)

    r_uri_select_data = requests.post(
        uri_select_data, json=body_regl, headers=headers)
    data_reglementations = r_uri_select_data.json()

    r_uri_select_data = requests.post(
        uri_select_data, json=body_regl_period, headers=headers)
    data_regl_periods = r_uri_select_data.json()

    # print("\n Response: ", r_uri_select_data,
    #         "\n Type: ", type(r_uri_select_data),
    #         "\n Content: ", r_uri_select_data.json()
    #         )

    places_collection = convert_places(data=data_places)
    # r = ""
    # file_name = urls_name[0] + r +".geojson"
    # with open(DATA_PATH + file_name, "w") as f:
    #     f.write('%s' % places_collection)

    '''
        Ajout des réglementations
    '''
    dateTime_reservation = None
    price = None
    minStay = None
    data_geo_empl_reglementations = emplacement_reglementations_to_dic(
        data_empl_reglementations)
    # TODO minStay - pas forcement utile, l'interface le fait deja
    data_geo_reglementations = reglementations_to_dic(
        data_reglementations, dateTime_reservation, minStay)
    data_geo_regl_periods = reglementations_periods_to_dic(data_regl_periods)
    # TODO weekday - pas forcement utile, l'interface le fait deja
    data_geo_periods = periods_to_dic(data_periods, dateTime_reservation)

    places_collection_wr = add_reglementations(data_geo_empl_reglementations,
                                               data_geo_reglementations,
                                               data_geo_regl_periods,
                                               data_geo_periods,
                                               places_collection,
                                               dateTime_reservation,
                                               price,
                                               minStay)
    # r = "_with_reglementations"
    # file_name = urls_name[0] + r +".geojson"
    # with open(DATA_PATH + file_name, "w") as f:
    #     f.write('%s' % places_collection_wr)

    # stream = os.popen(f'{python_exe} {main_file} -i="{src}" -it=1 -o="{dest}" twin -d=0 -pd=1')
    # stream.read()
    data_filtred = filter_mtl(places_collection_wr, arronds)

    '''
        Match des data avec SharedStreets
    '''

    for outfile, data_i in data_filtred.items():
        # -----------------------------------
        # UploadMapFile(data_i)
        # f = "https://drive.google.com/uc?export=download&id=13L3dqI_DJvPL_O4PcrARZr6GsFZrS9ev"
        # Cloud Vs File

        current_file = "current_data.geojson"
        json_l = DATA_PATH + current_file
        with open(json_l, "w") as f:
            json.dump(data_i, f)
        # -----------------------------------
        # f = io.BytesIO(json.dumps(data_i).encode('utf-8'))
        # econdage VS formatage
        # json_t = "debug.json" #open
        # json_l = json.dumps(json_t) #data_i:principal, json_t:test
        # json_l = json_l.replace('\"', '\\"')
        # json_l = "'" + json_l + "'"
        # -----------------------------------

        print("\nDébut premier match")
        c = f"shst match {json_l} \
                --search-radius=15 \
                    --offset-line=10 \
                        --snap-side-of-street \
                                --buffer-points"
        os.system(c)
        print("Fin premier match")

        with open(json_l.replace(".geojson", ".buffered.geojson"), "r") as fr, \
                open(json_l.replace(".geojson", "-segment.geojson"), "w") as fw:

            data_tr = json.load(fr)
            data_tw = to_segment(data_tr)
            json.dump(data_tw, fw)

        json_l = json_l.replace(".geojson", "-segment.geojson")
        c = f"shst match {json_l}  \
            --join-points \
                --join-points-match-fields=pp_snomrue \
                    --search-radius=15 \
                        --snap-intersections \
                            --snap-intersections-radius=10 \
                                --trim-intersections-radius=5 \
                                        --buffer-merge-group-fields=pp_snomrue \
                                            --buffer-points"

        # print(c)
        # with open("command.txt", "w") as f:
        #     f.write(c)
        os.system(c)

    '''
        Transformation des data en regulations
    '''

    geojson = {}
    try:
        current_file_buffered = DATA_PATH + \
            current_file.replace("geojson", "buffered.geojson")

        _, geojson = turn_regl_to_regu(current_file_buffered)
    except FileNotFoundError as e:
        print("Pas de match pour,", json_l, ". Fichier buffered manquant")

    os.system("rm data/mtl-*")
    with open("../../../curb-map/src/assets/data/last_converted.curblr.json", "w") as f:
        json.dump(geojson, f)
    return geojson
    '''
        TODO: ameliorations:
                - un seul fichier - class
                - creer un dictionnaire des conversions par arrondissements, et eventuellement enregistrer dans une bd

        TODO: lier a sharedstreets node env
        TODO: deploy
        TODO: gerer les autres cas de regulations I, R, E etc.
    '''


if __name__ == "__main__":
    # os.system("nvm use 12.18.0")
    geojson = run(arronds=arrondissements[:2])
