import requests
import json
from requests.auth import HTTPBasicAuth
from typing import Optional
from geojson import Feature, FeatureCollection, Point
from datetime import datetime, date
# from parcometres import add_reglementations
#----------------------------------------------------------------------
#https://blog.bearer.sh/making-api-requests-with-python/
# import asyncio
# import aiohttp

# async def launch(url="http://localhost", bearer_token=None, body={}):
#     async with aiohttp.ClientSession() as session:
# 		if bearer_token is not None:
#             async with session.post(url, headers={'Authorization':'Bearer ' + bearer_token, 'Content-Type':'application/json'}, json=body) as resp:
#                 response = await resp.json() # [2]
#                 print(response)
#                 return response
#         #LOGIN
#         async with session.post(url, json=body) as resp:
#             response = await resp.json() # [2]
#             token = response["token"]
#             print(response)
#             return response, token
# asyncio.run(launch()) # [6]
#----------------------------------------------------------------------

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

PATH = "data/"

def convert_places(data, dateTime_reservation:Optional[datetime]=None,
                    price=None,
                    minStay=None):#TODO Parameters for polygon filter, price - pas forcement necessaire
    features = []
    # sNoPlace, nLongitude, nLatitude, nPositionCentreLongitude, nPositionCentreLatitude,
    # sStatut, sGenre, sType, sAutreTete, sNomRue, nSupVelo, sTypeExploitation, nTarifHoraire, sLocalisation, nTarifMax
    data = data["data"]    
    for place in data:
        longitude = place["NLONGITUDE"]
        latitude = place["NLATITUDE"]
        try:
            latitude, longitude = map(float, (latitude, longitude))
            features.append(
                Feature(
                    # geometry = p,
                    geometry = Point((longitude, latitude)),
                    properties = {
                        "sNoplace_sNoEmplacement": place["SNOPLACE"],
                        "nPositionCentreLongitude": place["NPOSITIONCENTRELONGITUDE"],
                        "nPositionCentreLatitude": place["NPOSITIONCENTRELATITUDE"],
                        "sStatut": place["SSTATUT"],
                        "sGenre": place["SGENRE"],
                        "sType": place["STYPE"],
                        "sAutreTete": place["SAUTRETETE"],
                        "sNomRue": place["SNOMRUE"],
                        "nSupVelo": place["NSUPVELO"],
                        "sTypeExploitation": place["STYPEEXPLOITATION"],
                        "nTarifHoraire": place["NTARIFHORAIRE"],
                        "sLocalisation": place["SLOCALISATION"],
                        "nTarifMax": place["NTARIFMAX"]
                    }
                )
        )
        except ValueError: #petit hack pour sauter la premiere ligne du fichier csv
            pass
    # for val in features:
    #     val[]
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
    Conversion des différentes donnees au format geojson
'''
def emplacement_reglementations_to_dic(data):
    # sNoEmplacement,sCodeAutocollant
    dic = {}
    l_tuple = []
    first_ligne = False
    for ligne in data:
        if first_ligne == False:
            first_ligne = True
            continue
        dic[ligne[0]] = {"sCodeAutocollant_Name":[]}
        l_tuple.append((ligne[0], ligne[1]) )
    for tp in l_tuple:
        dic[tp[0]]["sNoEmplacement"] = tp[0]
        dic[tp[0]]["sCodeAutocollant_Name"].append(tp[1])

    return dic

def reglementations_to_dic(data, dateTime_reservation:Optional[datetime]=None, minStay=None):#TODO minStay - pas forcement utile, l'interface le fait deja
    # Name,Type,DateDebut,DateFin,maxHeures
    dic = {}
    l_tuple = []
    first_ligne = False
    for ligne in data:
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

def reglementations_periods_to_dic(data):
    # sCode,noPeriode,sDescription
    dic = {}
    l_tuple = []
    first_ligne = False
    for ligne in data:
        if first_ligne == False:
            first_ligne = True
            continue
        dic[ligne[0]] = {"sub_prop":[]}
        l_tuple.append( (ligne[0], ligne[1], ligne[2]) )
    
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
    for ligne in data:
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


def run():
    uri_login = "http://52.235.16.115:8083/auth/signin"
    body_login = {}
    with open('credits.json') as f:
        body_login = json.load(f)
    r_uri_login = requests.post(uri_login, json=body_login)
    token = ""
    if r_uri_login.status_code == 200:
        token = r_uri_login.json()["token"]
    headers = {"Authorization": "Bearer "+token, 'Content-Type':'application/json'}

    # print(r_uri_login, type(r_uri_login))

    uri_select_data = "http://52.235.16.115:8083/dataAPI/selectData"

    # ITER stg_stationnement_mtl_emplacement_reglementation
    body_emp_regl = {
        "table": "stg_stationnement_mtl_emplacement_reglementation",
        "recordsPerPage":"5000",
        "currentPage":"1"
    }

    # FULL stg_stationnement_mtl_periode
    body_period = {
        "table": "stg_stationnement_mtl_periode",
        "recordsPerPage": "500",
        "currentPage": "1",
        "defaultReturnDateFormat":"HH:mm:ss"
    }

    # ITER stg_stationnement_mtl_place
    body_places = {
        "table": "stg_stationnement_mtl_place",
        "recordsPerPage": "1000",
        "currentPage": "1"
    }

    #FULL stg_stationnement_mtl_reglementation
    body_regl = {
        "table": "stg_stationnement_mtl_reglementation",
        "recordsPerPage": "500",
        "currentPage": "1"
    }

    #FULL stg_stationnement_mtl_reglementation_periode
    body_regl_period = {
        "table": "stg_stationnement_mtl_reglementation_periode",
        "recordsPerPage": "800",
        "currentPage": "1"
    }

    l_body = [body_emp_regl, body_period, body_places, body_regl, body_regl_period]
    body = l_body[2]

    r_uri_select_data = requests.get(uri_select_data, json=body_emp_regl, headers=headers)
    data_empl_reglementations = r_uri_select_data.json()

    r_uri_select_data = requests.get(uri_select_data, json=body_period, headers=headers) 
    data_periods = r_uri_select_data.json()
    
    r_uri_select_data = requests.get(uri_select_data, json=body_places, headers=headers) 
    data_places = r_uri_select_data.json()
    
    r_uri_select_data = requests.get(uri_select_data, json=body_regl, headers=headers) 
    data_reglementations = r_uri_select_data.json()
    
    r_uri_select_data = requests.get(uri_select_data, json=body_regl_period, headers=headers) 
    data_regl_periods = r_uri_select_data.json()
    
    print("\n Response: ", r_uri_select_data,
            "\n Type: ", type(r_uri_select_data),
            "\n Content: ", r_uri_select_data.json()
            )

    places_collection = convert_places(data=data_places)
    # r = ""
    # file_name = urls_name[0] + r +".geojson"
    # with open(PATH + file_name, "w") as f:
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
    # with open(PATH + file_name, "w") as f:
    #     f.write('%s' % places_collection_wr)



run()