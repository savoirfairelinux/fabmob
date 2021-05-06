from parcometres import *
from filter_mtl import *
import os

'''
    arrondissements: liste de tous les arrondissements de la ville de Montreal
    arronds: liste des arrondissements pour lesquels les donnees de parcometres sont presents
    Les arrondissements en commentaire sont ceux pour lesquels les donnees sont soit absentes soit corrompues
    Étant donné le temps de conversion assez long pour l'intégralité des arrondissements, je conseille de procéder avec deux ou trois arrondissements pour les tests

    Ce script est le code de conversion principal basé sur les fichiers téléchargés 
'''

arrondissements = [
    "plaza",
    "Outremont",#0
    "LaSalle",
    "Mont-Royal", #absent dans curbconvert
    "Ville-Marie",
    "Le Plateau-Mont-Royal", #4 #Plateau-Mont-Royal
    "Hampstead", #absent dans curbconvert
    "Le Sud-Ouest", #"Sud-Ouest"
    "Rivière-des-Prairies-Pointe-aux-Trembles", #"Rivière-des-Prairies - Pointe-aux-Trembles"
    "Lachine", #8
    "Dorval", #absent
    "Montréal-Nord", 
    "L'Île-Bizard-Sainte-Geneviève", #un script pour extraire tous les noms arrond? #"L'Île-Bizard - Sainte-Geneviève"
    "Kirkland", #12 #Absent
    "Dollard-des-Ormeaux",
    "Senneville",
    "Ahuntsic-Cartierville",
    "Côte-Saint-Luc", #16
    "Saint-Léonard",
    "Montréal-Ouest",
    "Pointe-Claire",
    "L'Île-Dorval", #20
    "Mercier-Hochelaga-Maisonneuve",
    "Côte-des-Neiges-Notre-Dame-de-Grâce",
    "Rosemont-La Petite-Patrie",
    "Saint-Laurent", #24
    "Beaconsfield",
    "Villeray-Saint-Michel-Parc-Extension",
    "Westmount",
    "Montréal-Est", #28
    "Anjou",
    "Pierrefonds-Roxboro",
    "Sainte-Anne-de-Bellevue",
    "Verdun", #32
    "Baie-d'Urfé"
]
arronds = [
    "plaza", 
    "Outremont",#0
    # "LaSalle",
    # "Mont-Royal", #absent dans curbconvert
    "Ville-Marie",
    "Le Plateau-Mont-Royal", #4 #Plateau-Mont-Royal
    # "Hampstead", #absent dans curbconvert
    "Le Sud-Ouest", #"Sud-Ouest"
    # "Rivière-des-Prairies-Pointe-aux-Trembles", #"Rivière-des-Prairies - Pointe-aux-Trembles"
    "Lachine", #8
    # "Dorval", #absent
    # "Montréal-Nord", 
    # "L'Île-Bizard-Sainte-Geneviève", #un script pour extraire tous les noms arrond? #"L'Île-Bizard - Sainte-Geneviève"
    # "Kirkland", #12 #Absent
    # "Dollard-des-Ormeaux",
    # "Senneville",
    "Ahuntsic-Cartierville",
    # "Côte-Saint-Luc", #16
    # "Saint-Léonard",
    # "Montréal-Ouest",
    # "Pointe-Claire",
    # "L'Île-Dorval", #20
    "Mercier-Hochelaga-Maisonneuve",
    "Côte-des-Neiges-Notre-Dame-de-Grâce",
    "Rosemont-La Petite-Patrie",
    "Saint-Laurent", #24
    # "Beaconsfield",
    "Villeray-Saint-Michel-Parc-Extension",
    # "Westmount",
    # "Montréal-Est", #28
    # "Anjou",
    # "Pierrefonds-Roxboro",
    # "Sainte-Anne-de-Bellevue",
    "Verdun", #32
    # "Baie-d'Urfé"
]
def run(arronds, dateTime_reservation:Optional[datetime]=None, price=None, minStay=None):
    #Telechargement
    print("1a - début téléchargements")
    get_files()
    print("1b - fin téléchargements")
    
    #conversion
    print("\n2a - début conversions")
    convert_bornes_hors_rue()
    convert_bornes_sur_rue()
    convert_places(dateTime_reservation, price, minStay)
    print("2b - fin conversions")

    #filtrage
    print("\n3a - début filtrage")
    # files = filter_mtl([arronds[0]])#[:4]
    files = filter_mtl(arronds)#[:2])
    print("3b - fin filtrage")
    '''
    NB:
        Apres cette étape:
        1 - Lancer le script filter_mtl.py et modifier le nom du fichier passé en paramètres ci-après avec le nom de l'arrondissement généré.
        2 - Lancer une commande shared-street avec le fichier filtré:
            ex dans update.sh
    '''

    print("\n4a - début match shst")
    for file_i in files:
        c = "shst match " + PATH + file_i + " --join-points \
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
        os.system(c)
    print("4b - fin match shst")

    #test avec le quartier rosemont
    
    print("\n5a - début curblr")
    files_to_mv = []
    geojson = {}
    for file_i in files:
        try:
            # f = "mtl-places-Rosemont-La-Petite-Patrie.filtred.buffered.geojson"
            # f = "data/places_with_reglementations.buffered.geojson"
            f = file_i.replace(".filtred.geojson", ".filtred.buffered.geojson")
            out, geojson = turn_regl_to_regu(f)
            files_to_mv.append(out)
            print("\n5b - fin curblr pour " + f)
        except FileNotFoundError:
            print("Pas de match pour,", file_i, ". Fichier buffered manquant")
        except KeyError:
            print("Pas de match pour,", file_i, ". Fichier buffered probablement vide")
        except TypeError as e: 
            print("Il n'y aura pas de match pour", file_i, "car la propriété 'geometry' du fichier manque probablement")
            print("Type error", e)
    print("\n5c - fin curblr")

    print("déplacement vers curb map")
    for file_i in files_to_mv:
        c = "mv " + PATH + file_i + " ../../../old/Curblr/erwin_fork_deployed_curb_map/curb-map/src/assets/data/"
        # c = "mv " + PATH + file_i + " ../curb-map/src/assets/data/"
        os.system(c)

    return geojson

# f = "mtl-places-Rosemont-La-Petite-Patrie.filtred.buffered.geojson"  
# turn_regl_to_regu(f)    
# (cd ../curb-map/; yarn start)


run(arronds)
