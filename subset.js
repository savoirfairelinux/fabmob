// curblrizes a geojson output from sharedstreets-js

const fs = require('fs');
const path = require('path');

const inputGeojson = fs.readFileSync('data/signalisation_stationnement.geojson');
const input = JSON.parse(inputGeojson);

var geojson = {"crs":input.crs};
geojson['type'] = 'FeatureCollection';

function zoneFilter (feature, lon,lat){
  return Math.min(...lon)<feature.geometry.coordinates[0] 
      && Math.max(...lon)>feature.geometry.coordinates[0] 
      && Math.min(...lat)<feature.geometry.coordinates[1] 
      && Math.max(...lat)>feature.geometry.coordinates[1]
}

// aucun filtre
//geojson['features'] = input.features;
// proche de SFL
geojson['features'] = input.features.filter(feature=>zoneFilter(feature,[-73.635009,-73.610089],[45.526366,45.538541]));
// rosemont / papineau  beaucoup de pannonceau et vignette
//geojson['features'] = input.features.filter(feature=>zoneFilter(feature,[-73.6045,-73.5738],[45.5485,45.5355]));

geojson['features'] = geojson.features.map(feature=>{
    feature.properties.title = feature.properties.PANNEAU_ID_PAN;
    feature.properties.description = `${feature.properties.PANNEAU_ID_RPA} --- ${feature.properties.DESCRIPTION_RPA}
    ${feature.properties.POSITION_POP} --- ${feature.properties.FLECHE_PAN}`;
    return feature;
});

// console.log(geojson.features.length);
console.log(JSON.stringify(geojson, null, 2))


