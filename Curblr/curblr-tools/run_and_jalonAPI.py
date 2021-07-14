import requests
import json
import os
import io
import base64

from requests.auth import HTTPBasicAuth
from typing import Optional
from datetime import datetime, date
from geojson import Feature, FeatureCollection, Point, Polygon
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
    l_out_file = []
    dic = {}
    for arrond in arrondissements:
        polygone = []

        # PLAZA
        if arrond == "plaza":
            file_to_open = DATA_PATH + "plaza-saint-hubert.geojson"#"plaza_rosemont.geojson"
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
                for i in (data["features"]):
                    if i["properties"]["NOM"] == arrond:
                        polygone = i["geometry"]["coordinates"][0]
                        break

        point_a_tester = []
        data = ""
        # file_to_open = "signalisation_stationnement.geojson"
        data = places_collection_wr
        '''
            m,n,p pour faciliter le debogage des filtres. Montre les points retenus et exclus.
        '''
        m=0
        n=0
        p =0
        filtered_features = []
        for feature in (data["features"]):
            m+=1
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
            outfile = "mtl-parco-" + "places-oasis-bellechasse-plaza".replace(" ","-").replace("+","-") + ".filtred.geojson"
        else:
            outfile = "mtl-parco-" + arrond.replace(" ","-").replace("+","-") + ".filtred.geojson"
        
        # with open(DATA_PATH + outfile, mode="w") as f:
        #     json.dump(data, f)
        # print("filtrage terminé")

        # l_out_file.append(outfile)
        dic[outfile] = data
    return dic #l_out_file

def convert_places(data, dateTime_reservation:Optional[datetime]=None,
                    price=None,
                    minStay=None):#TODO Parameters for polygon filter, price - pas forcement necessaire
    features = []
    # sNoPlace, nLongitude, nLatitude, nPositionCentreLongitude, nPositionCentreLatitude,
    # sStatut, sGenre, sType, sAutreTete, sNomRue, nSupVelo, sTypeExploitation, nTarifHoraire, sLocalisation, nTarifMax
    data = data["data"]
    for place in data:
        longitude = place[k_nlongitude]
        latitude = place[k_nlatitude]
        try:
            latitude, longitude = map(float, (latitude, longitude))
            features.append(
                Feature(
                    # geometry = p,
                    geometry = Point((longitude, latitude)),
                    properties = {
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
                        "nTarifMax": place[k_nTarifMax]
                    }
                )
        )
        except ValueError: #petit hack pour sauter la premiere ligne du fichier csv
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
                        minStay=None):#TODO Parameters for polygon filter and tarif(max)vation, price, minStay):
    
    for feature in collection["features"]:
        feature_properties = feature["properties"]
        sNoplace =  feature_properties["sNoplace_sNoEmplacement"]
        try:
            sNoplace_from_dic = data_geo_empl_reglementations[sNoplace]
        except Exception as e:
            print("add_reglementations, exception: ",e)
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
            except KeyError as e: #du au filtre selon le jour et le mois, certains autocollants disparaissent
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
        dic[ligne[k_sno_emplacement]] = {"sCodeAutocollant_Name":[]}
        l_tuple.append((ligne[k_sno_emplacement], ligne[k_scodeautocollant]) )
    for tp in l_tuple:
        dic[tp[0]]["sNoEmplacement"] = tp[0]
        dic[tp[0]]["sCodeAutocollant_Name"].append(tp[1])

    return dic

def reglementations_to_dic(data, dateTime_reservation:Optional[datetime]=None, minStay=None):#TODO minStay - pas forcement utile, l'interface le fait deja
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
            #TODO dateTime and minStay
            day_begin = int(ligne[k_datedebut][:2])
            month_begin = int(ligne[k_datedebut][2:])

            date_begin = date(dateTime_reservation.year, month_begin, day_begin)
            day_end = int(ligne[k_datefin][:2])
            month_end = int(ligne[k_datefin][2:])
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
                dic[ligne[k_name]] = {
                    "Name":ligne[k_name],
                     "Type":ligne[k_type],
                      "DateDebut":ligne[k_datedebut],
                       "DateFin":ligne[k_datefin],
                        "maxHeures": maxHeures
                        }
        else:
            dic[ligne[k_name]] = {
                "Name":ligne[k_name],
                 "Type":ligne[k_type],
                  "DateDebut":ligne[k_datedebut],
                   "DateFin":ligne[k_datefin],
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

        dic[ligne[k_scode]] = {"sub_prop":[]}
        l_tuple.append( (ligne[k_scode], ligne[k_noperiode], ligne[k_sdescription]) )
    
    for tp in l_tuple:
        dic[tp[0]]["sCode"] = tp[0]
        dic[tp[0]]["sub_prop"].append({"noPeriode": tp[1], "sDescription":tp[2]})
    
    return dic

def periods_to_dic(data, dateTime_reservation:Optional[datetime]=None):
    # nID,dtHeureDebut,dtHeureFin,bLun,bMar,bMer,bJeu,bVen,bSam,bDim
    dic = {}
    l_tuple = []
    first_ligne = False
    if dateTime_reservation is not None:
        weekday = dateTime_reservation.weekday() #TODO weekday - pas forcement utile, l'interface le fait deja
        # print("weekday", weekday)
    data = data["data"]  
    for ligne in data:
        if first_ligne == False:
            first_ligne = True
            continue

        dic[ligne[k_nid]] = {
            "nID":ligne[k_nid],
                "dtHeureDebut":ligne[k_dtheuredebut],
                "dtHeureFin":ligne[k_dtheurefin],
                "bLun":ligne[k_blun],
                "bMar":ligne[k_bmar],
                "bMer":ligne[k_bmer],
                "bJeu":ligne[k_bjeu],
                "bVen":ligne[k_bven],
                "bSam":ligne[k_bsam],
                "bDim":ligne[k_bdim]
                }
    return dic

def requests_iter(url):
    data = {}
    return data

def turn_regl_to_regu(buffered_file):
    with open(buffered_file, "r") as f:
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
                regulations = []
                n = 0
                feature_properties = feature["properties"]
                # print(feature_properties.keys())
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
                print("turn_regl_to_regu, KeyError: ", e)
                print("Pas de match pour,", buffered_file, ". Fichier buffered probablement vide ou clé inexistante")
            except TypeError as e: 
                print("turn_regl_to_regu, Il n'y aura pas de match pour", buffered_file, "car la propriété 'geometry' du fichier manque probablement")
                print("Type error", e)
                
    outfile = buffered_file.replace(".buffered.geojson", ".curblr.json")
    # outfile = "last_converted.curblr.json"
    # outfile = "last_converted_all.curblr.json"
    
    with open(outfile, mode="w") as f:
        # print(2,outfile)
        json.dump(geojson, f)
        # print(3,outfile)
    return outfile, geojson

def run(arronds=[arrondissements[0]], dateTime_reservation:Optional[datetime]=None, price=None, minStay=None):
    # uri_login = "http://52.235.16.115:8083/auth/signin" #old API
    uri_login = "https://jalonmtl.services/api/v1/auth/signin"
    body_login = {}
    with open('credits.json') as f:
        body_login = json.load(f)
    r_uri_login = requests.post(uri_login, json=body_login)
    token = ""
    if r_uri_login.status_code == 200:
        token = r_uri_login.json()["token"]
    headers = {"Authorization": "Bearer "+token, 'Content-Type':'application/json'}

    # print(r_uri_login, type(r_uri_login))

    # uri_select_data = "http://52.235.16.115:8083/dataAPI/selectData" #old API
    uri_select_data = "https://jalonmtl.services/api/v1/public/data"

    # ITER stg_stationnement_mtl_emplacement_reglementation
    body_emp_regl = {
        "table": "stg_stationnement_mtl_emplacement_reglementation",
        "recordsPerPage":"100000",
        "currentPage":"1"
    }

    # FULL stg_stationnement_mtl_periode
    body_period = {
        "table": "stg_stationnement_mtl_periode",
        "recordsPerPage": "100000",
        "currentPage": "1",
        "defaultReturnDateFormat":"HH:mm:ss"
    }

    # ITER stg_stationnement_mtl_place
    body_places = {
        "table": "stg_stationnement_mtl_place",
        "recordsPerPage": "100000",
        "currentPage": "1"
    }

    #FULL stg_stationnement_mtl_reglementation
    body_regl = {
        "table": "stg_stationnement_mtl_reglementation",
        "recordsPerPage": "100000",
        "currentPage": "1"
    }

    #FULL stg_stationnement_mtl_reglementation_periode
    body_regl_period = {
        "table": "stg_stationnement_mtl_reglementation_periode",
        "recordsPerPage": "100000",
        "currentPage": "1"
    }

    r_uri_select_data = requests.post(uri_select_data, json=body_emp_regl, headers=headers)
    data_empl_reglementations = r_uri_select_data.json()
    # print(data_empl_reglementations)

    r_uri_select_data = requests.post(uri_select_data, json=body_period, headers=headers) 
    data_periods = r_uri_select_data.json()
    
    r_uri_select_data = requests.post(uri_select_data, json=body_places, headers=headers) 
    data_places = r_uri_select_data.json()
    # print(data_places)

    r_uri_select_data = requests.post(uri_select_data, json=body_regl, headers=headers) 
    data_reglementations = r_uri_select_data.json()
    
    r_uri_select_data = requests.post(uri_select_data, json=body_regl_period, headers=headers) 
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
    dateTime_reservation=None
    price=None
    minStay=None
    data_geo_empl_reglementations = emplacement_reglementations_to_dic(data_empl_reglementations) 
    data_geo_reglementations = reglementations_to_dic(data_reglementations, dateTime_reservation, minStay)#TODO minStay - pas forcement utile, l'interface le fait deja
    data_geo_regl_periods = reglementations_periods_to_dic(data_regl_periods)
    data_geo_periods = periods_to_dic(data_periods, dateTime_reservation)#TODO weekday - pas forcement utile, l'interface le fait deja
    
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
        #-----------------------------------
        # UploadMapFile(data_i)
        # f = "https://drive.google.com/uc?export=download&id=13L3dqI_DJvPL_O4PcrARZr6GsFZrS9ev"
        ##Cloud Vs File

        current_file = "current_data.geojson"
        json_l = DATA_PATH + current_file
        with open(json_l, "w") as f:
            json.dump(data_i, f)    
        #-----------------------------------
        #exemple
        json_t = {
            "features": [
                {
                "geometry": {
                    "coordinates": [
                    -73.607113,
                    45.537208
                    ],
                    "type": "Point"
                },
                "properties": {
                    "liste_sCodeAutocollant_Name": [
                    "CH-AA",
                    "MX-02",
                    "MX-12",
                    "ZX-30"
                    ],
                    "nPositionCentreLatitude": "45.537168362723925000",
                    "nPositionCentreLongitude": "-73.607097772974456000",
                    "nSupVelo": "0",
                    "nTarifHoraire": "150",
                    "nTarifMax": "",
                    "sAutreTete": "RA577",
                    "sCodeAutocollant_Name": {
                    "CH-AA": {
                        "DateDebut": "0101",
                        "DateFin": "3112",
                        "Name": "CH-AA",
                        "Type": "U",
                        "maxHeures": "2",
                        "sub_prob": [
                        {
                            "noPeriode": "28",
                            "periodes": {
                            "bDim": "0",
                            "bJeu": "0",
                            "bLun": "0",
                            "bMar": "0",
                            "bMer": "0",
                            "bSam": "1",
                            "bVen": "0",
                            "dtHeureDebut": "09:00:00",
                            "dtHeureFin": "18:00:00",
                            "nID": "28"
                            },
                            "sDescription": "LUN À VEN 9 h - 21 h SAM 9 h - 18 h DIM 13 h - 18 h"
                        },
                        {
                            "noPeriode": "108",
                            "periodes": {
                            "bDim": "0",
                            "bJeu": "1",
                            "bLun": "1",
                            "bMar": "1",
                            "bMer": "1",
                            "bSam": "0",
                            "bVen": "1",
                            "dtHeureDebut": "09:00:00",
                            "dtHeureFin": "21:00:00",
                            "nID": "108"
                            },
                            "sDescription": "LUN À VEN 9 h - 21 h SAM 9 h - 18 h DIM 13 h - 18 h"
                        },
                        {
                            "noPeriode": "125",
                            "periodes": {
                            "bDim": "1",
                            "bJeu": "0",
                            "bLun": "0",
                            "bMar": "0",
                            "bMer": "0",
                            "bSam": "0",
                            "bVen": "0",
                            "dtHeureDebut": "13:00:00",
                            "dtHeureFin": "18:00:00",
                            "nID": "125"
                            },
                            "sDescription": "LUN À VEN 9 h - 21 h SAM 9 h - 18 h DIM 13 h - 18 h"
                        }
                        ]
                    },
                    "MX-02": {
                        "DateDebut": "0101",
                        "DateFin": "3112",
                        "Name": "MX-02",
                        "Type": "Q",
                        "maxHeures": "3",
                        "sub_prob": [
                        {
                            "noPeriode": "28",
                            "periodes": {
                            "bDim": "0",
                            "bJeu": "0",
                            "bLun": "0",
                            "bMar": "0",
                            "bMer": "0",
                            "bSam": "1",
                            "bVen": "0",
                            "dtHeureDebut": "09:00:00",
                            "dtHeureFin": "18:00:00",
                            "nID": "28"
                            },
                            "sDescription": "MAX 3 h 9h - 18 h SAM et 13 h - 18 h DIM"
                        },
                        {
                            "noPeriode": "125",
                            "periodes": {
                            "bDim": "1",
                            "bJeu": "0",
                            "bLun": "0",
                            "bMar": "0",
                            "bMer": "0",
                            "bSam": "0",
                            "bVen": "0",
                            "dtHeureDebut": "13:00:00",
                            "dtHeureFin": "18:00:00",
                            "nID": "125"
                            },
                            "sDescription": "MAX 3 h 9h - 18 h SAM et 13 h - 18 h DIM"
                        }
                        ]
                    },
                    "MX-12": {
                        "DateDebut": "0101",
                        "DateFin": "3112",
                        "Name": "MX-12",
                        "Type": "Q",
                        "maxHeures": "3",
                        "sub_prob": [
                        {
                            "noPeriode": "108",
                            "periodes": {
                            "bDim": "0",
                            "bJeu": "1",
                            "bLun": "1",
                            "bMar": "1",
                            "bMer": "1",
                            "bSam": "0",
                            "bVen": "1",
                            "dtHeureDebut": "09:00:00",
                            "dtHeureFin": "21:00:00",
                            "nID": "108"
                            },
                            "sDescription": "MAX 3 h 9 h - 21 h LUN à VEN"
                        }
                        ]
                    },
                    "ZX-30": {
                        "DateDebut": "0104",
                        "DateFin": "0112",
                        "Name": "ZX-30",
                        "Type": "A",
                        "maxHeures": "0",
                        "sub_prob": [
                        {
                            "noPeriode": "1406",
                            "periodes": {
                            "bDim": "0",
                            "bJeu": "0",
                            "bLun": "0",
                            "bMar": "0",
                            "bMer": "1",
                            "bSam": "0",
                            "bVen": "0",
                            "dtHeureDebut": "14:30:00",
                            "dtHeureFin": "15:30:00",
                            "nID": "1406"
                            },
                            "sDescription": "STAT. INT. 14 h 30 - 15 h 30 MER 01 avril au 01 déc"
                        }
                        ]
                    }
                    },
                    "sGenre": "NORMAL",
                    "sLocalisation": "S",
                    "sNomRue": "Saint-Zotique",
                    "sNoplace_sNoEmplacement": "RA576",
                    "sStatut": "1",
                    "sType": "Double",
                    "sTypeExploitation": "Régulier Payez-Partez"
                },
                "type": "Feature"
                }
            ]
            }
        #-----------------------------------
        # f = io.BytesIO(json.dumps(data_i).encode('utf-8'))  
        ##econdage VS formatage
        # json_l = json.dumps(json_t) #data_i:principal, json_t:test
        # json_l = json_l.replace('\"', '\\"')
        # json_l = "'" + json_l + "'"
        #-----------------------------------
        # c = f"shst match {f_subset}  \
        #         --search-radius=15 \
        #             --offset-line=10 \
        #                 --snap-side-of-street \
        #                         --buffer-points"

        c = f"shst match {json_l}  \
            --join-points \
                --join-points-match-fields=PANNEAU_ID_RPA,CODE_RPA \
                    --search-radius=15 \
                        --snap-intersections \
                            --snap-intersections-radius=10 \
                                --trim-intersections-radius=5 \
                                        --buffer-merge-group-fields=POTEAU_ID_POT,PANNEAU_ID_PAN \
                                            --buffer-points \
                                                --direction-field=direction \
                                                    --two-way-value=two \
                                                        --one-way-against-direction-value=against \
                                                            --one-way-with-direction-value=one"
        # print(c)
        # with open("command.txt", "w") as f:
        #     f.write(c)
        os.system(c)
    
    '''
        Transformation des data en regulations
    ''' 
    
    geojson = {}
    try:
        current_file_buffered = DATA_PATH + current_file.replace("geojson", "buffered.geojson")
        _, geojson = turn_regl_to_regu(current_file_buffered)
    except FileNotFoundError as e:
        print("Pas de match pour,", json_l, ". Fichier buffered manquant")

    os.system("rm data/mtl-*")
    return geojson
    '''
        TODO: ameliorations:
                - un seul fichier - class
                - creer un dictionnaire des conversions par arrondissements, et eventuellement enregistrer dans une bd

        TODO: lier a sharedstreets node env
        TODO: deploy
    '''

if __name__ == "__main__":
    # os.system("nvm use 12.18.0")
    geojson = run()