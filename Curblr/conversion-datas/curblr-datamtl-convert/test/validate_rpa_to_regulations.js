const fs = require('fs');

// one or two digits, followed by zero or more spaces, followed by "h" or "min"
const timeRegex = /\d{1,2}\s*(h|min)/i;

const daysRegexes = {
    // beginning of a word, followed by the truncated name of a day or its complete name
    "mo": /\blun(\b|\\|di)/i,
    "tu": /\bmar(\b|\\|di)/i,
    "we": /\bmer(\b|\\|credi)/i,
    "th": /\bjeu(\b|\\|di)/i,
    "fr": /\bve[nm](\b|\\|dredi)/i, // there is a typo in the data
    "sa": /\bsam(\b|\\|medi)/i,
    "su": /\bdim(\b|\\|manche)/i
};

const monthsRegexes = {
    // a digit or the beginning of a word, followed by the truncated name of a month or its complete name.
    "01": /(\d|\b)jan(\b|\.|vier)/i,
    "02": /(\d|\b)f[eé]v(\b|\.|rier)/i,
    "03": /(\d|\b)mar(\b|\.|s)/i,
    "04": /(\d|\b)avr(\b|\.|il)/i,
    "05": /(\d|\b)mai/i,
    "06": /(\d|\b)juin/i,
    "07": /(\d|\b)juillet/i,
    "08": /(\d|\b)ao[uû]t/i,
    "09": /(\d|\b)sep(\b|\.|tembre)/i,
    "10": /(\d|\b)oct(\b|\.|obre)/i,
    "11": /(\d|\b)nov(\b|\.|embre)/i,
    "12": /(\d|\b)d[eé]c(\b|\.|embre)/i,
};

const descriptionContainsTimespanInfos = (description) => {
    return timeRegex.test(description)
        || Object.values(daysRegexes).some( reg => reg.test(description) )
        || Object.values(monthsRegexes).some( reg => reg.test(description) );
}

function loadFromJsonFile(filename) {
    const json = fs.readFileSync(filename);
    return JSON.parse(json);
}

function getUsedRpaCodes(signalisation) {
    const usedRpaCodes = new Set();
    signalisation.features.forEach( (panneau) => {
        usedRpaCodes.add(panneau.properties.CODE_RPA);
    });
    return usedRpaCodes;
}

// Vefiry the converted RPAs and the originalRPAs have the same quantity of data
function verifyLengths(convertedRpa, originalRpa) {
    return Object.keys(convertedRpa).length == Object.keys(originalRpa.PANNEAU_ID_RPA).length;
}


function verifyRegulationIsNotMissing(rpa, usedRpaCodes) {
    if (Array.isArray(rpa.regulations)) {
        // rpa has regulation
        return true;
    }
    if (!usedRpaCodes.has(rpa.code)) {
        // rpa is not used, so won't lose time trying to fix it
        return true;
    }
    if (!descriptionContainsTimespanInfos(rpa.description)) {
        // if there is no timespan, then it is not possible to make a rule
        return true;
    }
    return false;
}

function verify() {
    const convertedRpa = loadFromJsonFile("../data/signalisation-codification-rpa_withRegulation.json");
    const originalRpa = loadFromJsonFile("../data/signalisation-codification-rpa.json");
    const signalisation = loadFromJsonFile("../data/signalisation_stationnement.geojson");
    const usedRpaCodes = getUsedRpaCodes(signalisation);

    if (!verifyLengths(convertedRpa, originalRpa)) {
        console.error("The original RPA and the converted RPA don't have the same number of data");
    }

    const missingRules = [];
    for (const [rpaId, rpa] of Object.entries(convertedRpa)) {
        if (!verifyRegulationIsNotMissing(rpa, usedRpaCodes)) {
            missingRules.push(`${rpaId} ${rpa.code} ${rpa.description}`);
            continue;
        }
        
    }

    console.log("missing rules:", missingRules);
}

verify();
