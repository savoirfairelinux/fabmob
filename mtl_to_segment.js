// curblrizes a geojson output from sharedstreets-js

const fs = require('fs');

const inputGeojson = fs.readFileSync('data/mtl-subset.geojson');
const input = JSON.parse(inputGeojson);

var geojson = {"crs":input.crs};
geojson['type'] = 'FeatureCollection';

fleche_map={0:2,  // no arrow -> middle
            2:1,  // left arrow -> start
            3:3}  // right arrow -> end

geojson['features'] = input.features.map(feature=>{
    feature.properties.point_sequence = fleche_map[feature.properties.FLECHE_PAN]
    return feature;
});

// console.log(geojson.features.length);
console.log(JSON.stringify(geojson, null, 2))


