#!/bin/bash

echo -n "Retrieve online data... "
wget -N -P data http://donnees.ville.montreal.qc.ca/dataset/8ac6dd33-b0d3-4eab-a334-5a6283eb7940/resource/52cecff0-2644-4258-a2d1-0c4b3b116117/download/signalisation_stationnement.geojson
wget -N -P data http://donnees.ville.montreal.qc.ca/dataset/c5bf5e9c-528b-4c28-b52f-218215992e35/resource/0795f422-b53b-41ca-89be-abc1069a88c9/download/signalisation-codification-rpa.json
echo "done"

echo -n "create regulations... "
node rpa_to_regulations.js json > data/signalisation-codification-rpa_withRegulation.json
echo "done"

echo -n "create pannonceau... "
node pannonceau_to_regulations.js jsonpan > data/agregate-pannonceau-rpa.json
echo -n " ... "
node pannonceau_to_regulations.js jsonmtl > data/agregate-signalisation.json
echo "done"


rm data/mtl-subset*
echo -n "create subset... "
node subset.js > data/mtl-subset.geojson
echo "done"

shst match data/mtl-subset.geojson --search-radius=15 --offset-line=10 --snap-side-of-street --buffer-points

echo -n "transform to segment... "
node mtl_to_segment.js > data/mtl-subset-segment.geojson
echo "done"


shst match data/mtl-subset-segment.geojson --join-points --join-points-match-fields=PANNEAU_ID_RPA,CODE_RPA \
    --search-radius=15 --snap-intersections --snap-intersections-radius=10 \
    --trim-intersections-radius=5 --buffer-merge-group-fields=POTEAU_ID_POT,PANNEAU_ID_PAN \
    --buffer-points \
    #--direction-field=direction --two-way-value=two --one-way-against-direction-value=against --one-way-with-direction-value=one


echo -n "generate curblr... "
node segment_to_curblr.js > data/mtl-subset-segment.curblr.json
echo "done"

#node stats.js > data/mtl-subset-unmanaged.geojson

date