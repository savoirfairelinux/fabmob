#!/bin/bash

# shst match data/places.geojson --join-points \ 
#     --search-radius=15 --snap-intersections --snap-intersections-radius=10 \
#     --trim-intersections-radius=5 \
#     --buffer-points \
#     --direction-field=direction --two-way-value=two --one-way-against-direction-value=against --one-way-with-direction-value=one

    # --buffer-merge-group-fields=POTEAU_ID_POT,PANNEAU_ID_PAN \

# --join-points-match-fields=PANNEAU_ID_RPA,CODE_RPA \ls

# mv last_converted.curblr.json last_converted_test.curblr.json 
# mv last_converted_test.curblr.json ../../CurbLr/conversion-mt-qc-et-map/erwin_fork/curb-map/src/assets/data/
# mv last_converted.curblr.json ../../CurbLr/conversion-mt-qc-et-map/erwin_fork/curb-map/src/assets/data/
# shst match data/places_with_reglementations.geojson --join-points --search-radius=15 --snap-intersections --snap-intersections-radius=10 --trim-intersections-radius=5 --buffer-points --direction-field=direction --two-way-value=two --one-way-against-direction-value=against --one-way-with-direction-value=one
# shst match data/bornes_sur_rue.geojson --join-points --search-radius=15 --snap-intersections --snap-intersections-radius=10 --trim-intersections-radius=5 --buffer-points --direction-field=direction --two-way-value=two --one-way-against-direction-value=against --one-way-with-direction-value=one
# shst match data/bornes_hors_rue.geojson --join-points --search-radius=15 --snap-intersections --snap-intersections-radius=10 --trim-intersections-radius=5 --buffer-points --direction -field=direction --two-way-value=two --one-way-against-direction-value=against --one-way-with-direction-value=one
# shst match mtl-places-Rosemont-La-Petite-Patrie.filtred.geojson --join-points --search-radius=15 --snap-intersections --snap-intersections-radius=10 --trim-intersections-radius=5 --buffer-points --direction-field=direction --two-way-value=two --one-way-against-direction-value=against --one-way-with-direction-value=one


# shst match data/places_with_reglementations.geojson --join-points --join-point-sequence-field= --search-radius=15 --snap-intersections --snap-intersections-radius=10 --trim-intersections-radius=5 --buffer-points
