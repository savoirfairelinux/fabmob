import os
import json 

arronds = [
    # "LaSalle",
    # "Ville-Marie",
    "Côte-des-Neiges - Notre-Dame-de-Grâce",#null
    # # "None",
    # "Montréal-Nord",
    "Saint-Léonard",#null
    # "Verdun",
    "L'Île-Bizard - Sainte-Geneviève",#####present mais
    "Sud-Ouest",##null
    # "Villeray - Saint-Michel - Parc-Extension",
    # "Anjou",
    # "Lachine",
    # "Plateau-Mont-Royal",
    # "Rivière-des-Prairies - Pointe-aux-Trembles",
    # "Rosemont - La Petite-Patrie",
    # "Mercier - Hochelaga-Maisonneuve",
    # "Pierrefonds - Roxboro",
    "Outremont",###lourd bug
    # "Ahuntsic - Cartierville",
    # "Saint-Laurent"
    ]
arronds = [
    "LaSalle",
    "Ville-Marie",
    "Côte-des-Neiges - Notre-Dame-de-Grâce",#null
    # "None",
    "Montréal-Nord",
    "Saint-Léonard",#null
    "Verdun",
    "L'Île-Bizard - Sainte-Geneviève",#####present mais
    "Sud-Ouest",##null
    "Villeray - Saint-Michel - Parc-Extension",
    "Anjou",
    "Lachine",
    "Plateau-Mont-Royal",
    "Rivière-des-Prairies - Pointe-aux-Trembles",
    "Rosemont - La Petite-Patrie",
    "Mercier - Hochelaga-Maisonneuve",
    "Pierrefonds - Roxboro",
    "Outremont",###lourd bug
    "Ahuntsic - Cartierville",
    "Saint-Laurent"
    ]

def check_avaialble_arronds():
    arrondissements_from_json = set([])
    agregate_sign_file = 'data/agregate-signalisation.json'
    with open(agregate_sign_file) as f:
        data = json.load(f)
        for i in (data["features"]):
            a = i["properties"]["NOM_ARROND"]
            arrondissements_from_json.add(a)
        for i in arrondissements_from_json:
            print(i)    

def update(arronds):
    os.system("echo -n 'Retrieve online data... '")
    # montreal datas 
    #       old - os.system("wget -N -P data http://donnees.ville.montreal.qc.ca/dataset/8ac6dd33-b0d3-4eab-a334-5a6283eb7940/resource/52cecff0-2644-4258-a2d1-0c4b3b116117/download/signalisation_stationnement.geojson
    #       old - os.system("wget -N -P data http://donnees.ville.montreal.qc.ca/dataset/c5bf5e9c-528b-4c28-b52f-218215992e35/resource/0795f422-b53b-41ca-89be-abc1069a88c9/download/signalisation-codification-rpa.json")
    os.system("wget -N -P data https://storage.googleapis.com/dx-montreal/resources/52cecff0-2644-4258-a2d1-0c4b3b116117/signalisation_stationnement.geojson")
    os.system("wget -N -P data https://storage.googleapis.com/dx-montreal/resources/0795f422-b53b-41ca-89be-abc1069a88c9/signalisation-codification-rpa.json")
    os.system("echo 'done'")

    os.system("echo -n 'create regulations... '")
    os.system("node rpa_to_regulations.js json > data/signalisation-codification-rpa_withRegulation.json")
    os.system("echo 'done'")

    os.system("echo -n 'create pannonceau... '")
    os.system("node pannonceau_to_regulations.js jsonpan > data/agregate-pannonceau-rpa.json")
    os.system("echo -n ' ... '")
    os.system("node pannonceau_to_regulations.js jsonmtl > data/agregate-signalisation.json")
    os.system("echo 'done'")

    os.system("rm data/mtl-subset*")
    os.system("echo -n 'create subset... '")
    
    # with open("s.txt", "w", encoding="utf-8") as f:
    for arrond in arronds:

        f_subset = "data/mtl-subset-" + arrond + ".geojson"
        f_subset = f_subset.replace(" ", "")
        os.system("node subset.js " + arrond + " > " + f_subset)
        os.system("echo 'done'")
        os.system("shst match " + f_subset + " \
            --search-radius=15 \
                --offset-line=10 \
                    --snap-side-of-street \
                            --buffer-points")

        os.system("echo -n 'transform to segment... '")
        f_subset_in = f_subset.replace(".geojson", ".buffered.geojson")
        f_subset_segment_out = f_subset.replace(".geojson", "-segment.geojson")
        os.system("node mtl_to_segment.js " + f_subset_in + " > " + f_subset_segment_out)
        os.system("echo 'done'")

        os.system("shst match " + f_subset_segment_out + " --join-points --join-points-match-fields=PANNEAU_ID_RPA,CODE_RPA \
            --search-radius=15 --snap-intersections --snap-intersections-radius=10 \
            --trim-intersections-radius=5 --buffer-merge-group-fields=POTEAU_ID_POT,PANNEAU_ID_PAN \
            --buffer-points \
            # --direction-field=direction --two-way-value=two --one-way-against-direction-value=against --one-way-with-direction-value=one \
            ")
        os.system("echo -n 'generate curblr... '")

        f_subset_joined_in = f_subset.replace(".geojson", "-segment.joined.geojson")
        f_subset_curblr_out = "mtl-subset-segment_all.curblr.json".replace("_all", "-" + arrond)
        f_subset_curblr_out = f_subset_curblr_out.replace(" ", "").lower()
        
        os.system("node segment_to_curblr.js " + f_subset_joined_in + " > data/" + f_subset_curblr_out)             
        
        assets_curb_map = os.path.join("..", "..", "curb-map", "src", "assets", "data")
        print(assets_curb_map)
        os.system("mv data/" + f_subset_curblr_out + " " + assets_curb_map)
        
        os.system("echo 'done'")
        #os.system("node stats.js > data/mtl-subset-unmanaged.geojson")
            # f.write('{ path: "' + f_subset_curblr_out + '", label: "mtl - ' + arrond + '" },\n')

    os.system("date")
os.system("nvm use 12.7.0")
update(arronds)