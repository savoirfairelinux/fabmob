// curblrizes a geojson output from sharedstreets-js

const fs = require('fs');

const inputGeojson = fs.readFileSync('data/mtl-subset.buffered.geojson');
const input = JSON.parse(inputGeojson);
const InputFeatur = input.features;

var geojson = {};
geojson['type'] = 'FeatureCollection';
var fleche_pan = '';



fleche_map={
    left:
        {'double':2,  // no arrow -> middle
            'left':3,   // left arrow -> end
            'right':1},  // right arrow -> start
    right:
        {'double':2,  // no arrow -> middle
            'left':1,   // left arrow -> start
            'right':3}   // right arrow -> end
};



geojson['features'] = input.features.map(feature=>{
    var dir = feature.properties.pp_description

    if (dir != ""){
        dir = dir.toUpperCase();}
    if(dir.includes("DR")) {
        fleche_pan = 'right';
    } else if(dir.includes("GA")) {
        fleche_pan = 'left';
    } else if(dir.includes("DOU")) {
        fleche_pan = 'double';
    } else if(dir.includes("TOUT")) {
        fleche_pan = 'straight';
    }
    return {
        properties: {
            point_sequence : fleche_map[feature.properties.sideOfStreet][fleche_pan],

            ID: feature.properties.pp_id,
            TYPE_CODE : feature.properties.pp_type_code,
            //POTEAU_ID_POT: feature.properties.pp_poteau_id_pot,
            //PANNEAU_ID_PAN: feature.properties.pp_panneau_id_pan,
            DESCRIPTION: feature.properties.pp_description
        },
        type: feature.type,
        geometry: feature.properties.pp_original_geometry
    }
});

// console.log(geojson.features.length);
console.log(JSON.stringify(geojson, null, 2))


