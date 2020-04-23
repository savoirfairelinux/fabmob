// curblrizes a geojson output from sharedstreets-js

const fs = require('fs');
const path = require('path');

const inputGeojson = fs.readFileSync('data/mtl-subset-segment.joined.geojson');
const input = JSON.parse(inputGeojson);
const rpaCodeJson = fs.readFileSync('data/signalisation-codification-rpa_withRegulation.json');
const rpaCode = JSON.parse(rpaCodeJson).reduce((acc,val)=>{acc[val.CODE_RPA]=val; return acc;},{});

var geojson = {};
geojson['type'] = 'FeatureCollection';
geojson['features'] = [];

for (var feature of input.features) {

    let {
        referenceId: shstRefId,
        sideOfStreet: sideOfStreet,
        section: [shstLocationStart, shstLocationEnd],
        pp_code_rpa: code_rpa
    } = feature.properties
    

    marker = "signs";

    if(rpaCode[code_rpa].regulations){
      var newTargetFeature = {
          ...feature,
          properties:{
            location:{
              shstRefId,
              sideOfStreet,
              shstLocationStart,
              shstLocationEnd,
              marker
            },
            regulations: rpaCode[code_rpa].regulations
        }
      }
      geojson['features'].push(newTargetFeature);
    }
}
// console.log(geojson.features.length);
console.log(JSON.stringify(geojson, null, 2))


