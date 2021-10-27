const fs = require('fs');

const ignoredValidations = {};

function addIgnoredValidation(description) {
    if (ignoredValidations[description]) {
        ignoredValidations[description] += 1;
    }
    else {
        ignoredValidations[description] = 1;
    }
}

function valid() {
    return { "ok": true, "message": ""};
}

function invalid(message) {
    return { "ok": false, message };
}

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

// validate the converted RPAs and the originalRPAs have the same quantity of data
function validateLengths(convertedRpa, originalRpa) {
    return Object.keys(convertedRpa).length == Object.keys(originalRpa.PANNEAU_ID_RPA).length;
}

function validateRegulations(description, regulations) {
    if (!Array.isArray(regulations) || regulations.length == 0) {
        return invalid("Regulations are missing")
    }

    if (regulations.length > 1) {
        return invalid("The convertion script does not support multiple rules yet");
    }

    return validateRule(description, regulations[0].rule);
}

function validateRule(description, rule) {
    if (!rule) {
        // TODO: add rules for panonceaux
        if (/pan{1,2}onceau/i.test(description)) {
            addIgnoredValidation("panonceau rule");
            return valid();
        }
        return invalid("Rule is missing");
    }
    return validateActivity(description, rule.activity);
}

function validateActivity(description, activity) {
    switch (activity) {
        case "no standing":
            return validateIsNoStanding(description);
        case "no parking":
            return validateIsNoParking(description);
        case "parking":
            return validateIsParking(description);
        default:
            return invalid("unknown activity");
    }
}

function validateIsNoStanding(description) {
    return valid();
}

function validateIsNoParking(description) {
    return valid();
}

function validateIsParking(description) {
    return valid();
}

function validate() {
    const convertedRpa = loadFromJsonFile("../data/signalisation-codification-rpa_withRegulation.json");
    const originalRpa = loadFromJsonFile("../data/signalisation-codification-rpa.json");
    const signalisation = loadFromJsonFile("../data/signalisation_stationnement.geojson");
    const usedRpaCodes = getUsedRpaCodes(signalisation);

    if (!validateLengths(convertedRpa, originalRpa)) {
        console.error("The original RPA and the converted RPA don't have the same number of data");
    }

    const errors = [];
    for (const [rpaId, rpa] of Object.entries(convertedRpa)) {
        if (!usedRpaCodes.has(rpa.code)) {
            // Lets not put efforts into validating unused RPAs
            addIgnoredValidation("not used");
            continue;
        }

        if (!descriptionContainsTimespanInfos(rpa.description)) {
            // There's nothing to do without timespan
            addIgnoredValidation("no timespan");
            continue;
        }

        // TODO: handle maxStays.
        if (/\d{1,2}\s*min/i.test(rpa.description)) {
            addIgnoredValidation("maxStay");
            continue;
        }

        const result = validateRegulations(rpa.description, rpa.regulations)
        if (!result.ok) {
            errors.push(`${result.message}: ${rpa.code} ${rpa.description}`);
        }
    }

    console.log("errors:", errors);
    console.log("ignored validations:", ignoredValidations);
}

validate();
