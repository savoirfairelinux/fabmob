#!/bin/bash

echo -n "create regulations... "
node rpa_to_regulations.js json > data/signalisation-codification-rpa_withRegulation.json
echo "done"


echo -n "create subset... "
node subset.js > data/mtl-subset.geojson
echo "done"

echo -n "transform to segment... "
node mtl_to_segment.js > data/mtl-subset-segment.geojson
echo "done"

shst match data/mtl-subset-segment.geojson --join-points --join-points-match-fields=CODE_RPA --best-direction --search-radius=15 --snap-intersections --snap-intersections-radius=10 --buffer-intersections-radius=5 --buffer-merge-group-fields=POTEAU_ID_POT,PANNEAU_ID_PAN

echo -n "generate curblr... "
node segment_to_curblr.js > data/mtl-subset-segment.curblr.json
echo "done"
date