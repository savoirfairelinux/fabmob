// curblrizes a geojson output from sharedstreets-js

const fs = require('fs');
const path = require('path');

const inputGeojson = fs.readFileSync('data/agregate-signalisation.json');
const input = JSON.parse(inputGeojson);

var geojson = {
    "crs": input.crs
};
geojson['type'] = 'FeatureCollection';

//filtrer avec un arrondissement recu en ligne de commande
process.argv.shift();
process.argv.shift();
const arrond_from_cmd = process.argv.join(" ");
// console.log('myArgs: ', arrond_from_cmd);

function zoneFilter(feature, lon, lat) {
    return Math.min(...lon) < feature.geometry.coordinates[0] &&
        Math.max(...lon) > feature.geometry.coordinates[0] &&
        Math.min(...lat) < feature.geometry.coordinates[1] &&
        Math.max(...lat) > feature.geometry.coordinates[1]
}

// aucun filtre
// geojson['features'] = input.features;

// // proche de SFL
// geojson['features'] = input.features.filter(feature=>zoneFilter(feature,[-73.635009,-73.610089],[45.526366,45.538541]));
// // clark sfl
// geojson['features'] = input.features.filter(feature=>zoneFilter(feature,[-73.62041,-73.61931],[45.53486,45.53416]));
// // carré jean-talon/st-laurent
// geojson['features'] = input.features.filter(feature=>zoneFilter(feature,[-73.61848,-73.61600],[45.53518,45.53400]));
// rosemont / papineau  beaucoup de pannonceau et vignette
// geojson['features'] = input.features.filter(feature=>zoneFilter(feature,[-73.6045,-73.5738],[45.5485,45.5355]));


// {filtersArray:[{spatialFilter:[{"rings" : [ [ [-97.7325, 30.259],[97.7180,30.259 ], [-97.7180, 30.2687],[-97.7325, 30.2687],[-97.7325, 30.259] ]],"spatialReference" : {"wkid" : 4326}}]}]}

// arrond = [
//     'Mercier - Hochelaga-Maisonneuve',
//     'Rosemont - La Petite-Patrie',
//     'Villeray - Saint-Michel - Parc-Extension',
//     'Ville-Marie',
//     'Plateau-Mont-Royal',
//     'Ahuntsic - Cartierville',
//     'Outremont',
// // err
//     'Côte-des-Neiges - Notre-Dame-de-Grâce',
//     'Rivière-des-Prairies - Pointe-aux-Trembles',
//     'Saint-Laurent',           //partiel  4318 panneau non gérer
//     'Sud-Ouest',
// //err    'Saint-Léonard',
//     'LaSalle',                 //partiel data missing?
//     'Verdun',                  //partiel data missing?
//     'Montréal-Nord',           //partiel data missing?
//     'Anjou',                   //partiel data missing?
//     'Lachine',
//     'Pierrefonds - Roxboro'      //partiel data missing?
// ]
// console.log("XXXXXXXXXXXXXXXXXXXXXXXXX =>>>>>>>>", arrond_from_cmd);
arrond = [arrond_from_cmd]
geojson['features'] = input.features.filter(feature => arrond.indexOf(feature.properties.NOM_ARROND) >= 0);
geojson['features'] = input.features

// geojson['features'] = geojson.features.filter(feature=>feature.properties.DESCRIPTION_REP!="Enlevé");

geojson['features'] = geojson.features.map(feature => {
    feature.properties.title = feature.properties.PANNEAU_ID_PAN;
    feature.properties.description = `${feature.properties.PANNEAU_ID_RPA} --- ${feature.properties.DESCRIPTION_RPA}
    ${feature.properties.POSITION_POP} --- ${feature.properties.FLECHE_PAN}`;
    feature.properties.original_geometry = feature.geometry;
    return feature;
});

console.error(geojson.features.length);
console.log(JSON.stringify(geojson, null, 2))