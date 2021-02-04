#Telechargement
get_files()

#conversion
convert_places()
convert_bornes_hors_rue()
convert_bornes_sur_rue()

'''
    NB:
        Apres cette étape:
        1 - Lancer le script filter_mtl.py et modifier le nom du fichier passé en paramètres ci-après avec le nom de l'arrondissement généré.
        2 - Lancer une commande shared-street avec le fichier filtré:
            ex dans update.sh
'''


#test avec le quartier rosemont
f = "mtl-places-Rosemont-La-Petite-Patrie.filtred.buffered.geojson"
# f = "data/places_with_reglementations.buffered.geojson"
turn_regl_to_regu(f)
