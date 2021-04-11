#!/usr/bin/env
# HexMap, 2020
# Written by Kyle Fitzsimmons
from datetime import datetime
import json
import os
from django.conf import settings

def convert():
    # DATA_DIR = "/home/eanoh/Téléchargements/files"
    # DATA_DIR = "/home/eanoh/Cozy Drive/herdr_raw"
    DATA_DIR = settings.MEDIA_ROOT
    # DATA_DIR = './data'
    points_feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }

    polylines_feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }
    date_idx = 0
    last_date = None
    polyline = None
    for fn in sorted(os.listdir(DATA_DIR)):
        fp = os.path.join(DATA_DIR, fn)


        if not fn.endswith('GEOLOCATION.json'):
            continue

        with open(fp, 'r') as json_f:
            data = json.load(json_f)

            # generate polyline data by each day
            epoch = float(data['timestampEpoch']) / 1000
            dt = datetime.fromtimestamp(epoch)
            if not last_date or last_date != dt.date():
                # if polyline:
                #     try:
                #         polyline['properties']['endTimestamp'] = data['timestamp']
                #         polyline_feature_collection.append(polyline)
                #     except Exception as e:
                #         print("ERREUR ---------------->", e)#, "-->", polyline)
                #         pass
                polyline = {
                    'type' : 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': []
                    },
                    'properties': {
                        'date': dt.date().isoformat(),
                        'startTimestamp': data['timestamp'],
                        'endTimestamp': None,
                    }
                }
                last_date = dt.date()


            polyline['geometry']['coordinates'].append([data['longitude'], data['latitude']])

            # generate a point data for each file
            point = {
                'geometry': {
                    'type' : 'Feature',
                    'type': 'Point',
                    'coordinates': [data['longitude'], data['latitude']]
                },
                'properties': {
                    'timestamp': data['timestamp'],
                    'timestampEpoch': data['timestampEpoch'],
                    'altitude': data['altitude'],
                    'accuracyHorizontalMeters': data['accuracyHorizontalMeters'],
                    'accuracyVerticalMeters': data['accuracyVerticalMeters']
                }
            }
            points_feature_collection['features'].append(point)

    polylines_feature_collection['features'].append(polyline)


    # write output files
    with open(settings.MEDIA_ROOT+'/points.geojson', 'w') as geojson_points_f:
        json.dump(points_feature_collection, geojson_points_f)


    with open(settings.MEDIA_ROOT+'/polylines.geojson', 'w') as geojson_polylines_f:
        json.dump(polylines_feature_collection, geojson_polylines_f)


def convert_form_list(list_files):
    # DATA_DIR = settings.MEDIA_ROOT
    
    points_feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }

    polylines_feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }

    date_idx = 0
    last_date = None
    polyline = None
    # for fn in sorted(list_files):
    for fn in list_files:
            #     print(file_i.read())
        # fp = os.path.join(DATA_DIR, fn)

        if not fn.name.endswith('GEOLOCATION.json'):
            continue

        # with open(fp, 'r') as json_f:
        json_fff = fn.read() 
        # print("COUCOU", type(json_fff), json_fff)
        json_ff = json_fff.decode("utf-8")
        # print("COUCOU2", type(json_ff), json_ff)
        json_f = json.dumps(json_ff)
        # print("COUCOU3", type(json_f), json_f)

        data = json.loads(json_fff)

        # print("COUCOU4", type(data))
        # generate polyline data by each day
        epoch = float(data['timestampEpoch']) / 1000
        dt = datetime.fromtimestamp(epoch)
        if not last_date or last_date != dt.date():
            # if polyline:
            #     try:
            #         polyline['properties']['endTimestamp'] = data['timestamp']
            #         polyline_feature_collection.append(polyline)
            #     except Exception as e:
            #         print("ERREUR ---------------->", e)#, "-->", polyline)
            #         pass
            polyline = {
                'type' : 'Feature',
                'geometry': {
                    
                    'type': 'LineString',
                    'coordinates': []
                },
                'properties': {
                    'date': dt.date().isoformat(),
                    'startTimestamp': data['timestamp'],
                    'endTimestamp': None,
                }
            }
            last_date = dt.date()

        polyline['geometry']['coordinates'].append([data['longitude'], data['latitude']])

        # generate a point data for each file
        point = {
            'type' : 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [data['longitude'], data['latitude']]
            },
            'properties': {
                'timestamp': data['timestamp'],
                'timestampEpoch': data['timestampEpoch'],
                'altitude': data['altitude'],
                'accuracyHorizontalMeters': data['accuracyHorizontalMeters'],
                'accuracyVertic alMeters': data['accuracyVerticalMeters']
            }
        }
        points_feature_collection['features'].append(point)

    polylines_feature_collection['features'].append(polyline)

    # write output files
    # with open(settings.MEDIA_ROOT+'/points.geojson', 'w') as geojson_points_f:
    #     json.dump(points_feature_collection, geojson_points_f)


    # with open(settings.MEDIA_ROOT+'/polylines.geojson', 'w') as geojson_polylines_f:
    #     json.dump(polylines_feature_collection, geojson_polylines_f)
    # print(points_feature_collection,polylines_feature_collection)
    return points_feature_collection, polylines_feature_collection
