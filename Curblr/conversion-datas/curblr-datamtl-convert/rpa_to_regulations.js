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
    "03": /(?<!de-)(\d|\b)mar(\b|\.|s)/i, // excludes champ-de-mars
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

function descriptionContainsTimespan(description) {
    return timeRegex.test(description)
        || Object.values(daysRegexes).some( reg => reg.test(description) )
        || Object.values(monthsRegexes).some( reg => reg.test(description) );
}

const irrelevantExpressions = [
    "RUELLE FERMEE",
    "PASSAGE INTERDIT",
    "DECHETS INTERDITS"
];

function containsIrrelevantExpression(description) {
    return irrelevantExpressions.some( expression => description.includes(expression));
}

function getActivity(description) {
    if(description.includes("\\P ") || description.startsWith("/P ") || description.startsWith("STAT. INT. ") || description.startsWith("INTERDICTION DE STAT. ")) {
        return 'no parking';
    } else if(description.includes("\\A ") || description.startsWith("A ")) {
        return 'no standing';
    } else if(description.startsWith("P ")) {
        return'parking';
    } else if(description.startsWith("PANONCEAU ") || description.startsWith("PANNONCEAU")) {
        return null;
    } else if (descriptionContainsTimespan(description)) {
        // We assume descriptions containing timespan without further indications are no parking
        // This might be a wrong assumption
        return 'no parking';
    }
    else {
        return undefined;
    }
}

const monthValues = {
    "1 MARS AU 1 DEC":[{"from":"03-01","to":"12-01"}],
    "1ER MARS 1ER DEC":[{"from":"03-01","to":"12-01"}],
    "1ER MARS - 1ER DÉC":[{"from":"03-01","to":"12-01"}],
    "1ER MARS - 1ER  DÉC":[{"from":"03-01","to":"12-01"}],
    "1ER MARS AU 1ER DECEMBRE":[{"from":"03-01","to":"12-01"}],
    "1ER MARS AU 1ER DEC":[{"from":"03-01","to":"12-01"}],
    "MARS 01 A DEC. 01":[{"from":"03-01","to":"12-01"}],
    "1 MARSL AU 1 DEC":[{"from":"03-01","to":"12-01"}],
    "1MARS AU 1 DEC.":[{"from":"03-01","to":"12-01"}],
    "15 MRS - 15 NOV.":[{"from":"03-15","to":"11-15"}],
    "15 MARS AU 15 NOV":[{"from":"03-15","to":"11-15"}],
    "15 MARS À 15 NOV":[{"from":"03-15","to":"11-15"}],
    "15 MARS - 15 NOVEMBRE":[{"from":"03-15","to":"11-15"}],
    "15 MARS AU 15 NOVEMBRE":[{"from":"03-15","to":"11-15"}],
    "1 AVRIL AU 30 SEPT":[{"from":"04-01","to":"09-30"}],
    "1 AVRIL AU 15 OCT":[{"from":"05-01","to":"10-15"}],
    "1 AVRIL AU 31 OCT":[{"from":"05-01","to":"10-31"}],
    "1 AVRIL AU 1 NOVEMBRE":[{"from":"05-01","to":"11-01"}],
    "1 AVRIL AU 15 NOV":[{"from":"05-01","to":"11-15"}],
    "1 AVRIL AU 15 NOVEMBRE":[{"from":"05-01","to":"11-15"}],
    "1 AVRIL AU 30 NOV":[{"from":"04-01","to":"11-30"}],
    "1ER AVRIL - 30 NOV":[{"from":"04-01","to":"11-30"}],
    "1 AVRILAU 1 DEC":[{"from":"04-01","to":"12-01"}],
    "1 AVRIL AU 1 DEC":[{"from":"04-01","to":"12-01"}],
    "1 AVIL AU 1 DEC":[{"from":"04-01","to":"12-01"}],
    "1 AVRIL ET 1 DEC":[{"from":"04-01","to":"12-01"}],
    "1AVRIL AU 1 DEC":[{"from":"04-01","to":"12-01"}],
    "1AVRIL AU 1DEC":[{"from":"04-01","to":"12-01"}],
    "1ER AVRIL AU 1ER DEC":[{"from":"04-01","to":"12-01"}],
    "AVRIL 01 A DEC. 01":[{"from":"04-01","to":"12-01"}],
    "1 AVRILS AU 1 DEC":[{"from":"04-01","to":"12-01"}],
    "1 AVRIL  AU 1 DEC":[{"from":"04-01","to":"12-01"}],
    "15 AVRIL AU 15 OCTOBRE":[{"from":"04-15","to":"10-15"}],
    "15 AVRIL AU 1 NOV":[{"from":"05-15","to":"11-01"}],
    "15 AVRIL AU 1ER NOV.":[{"from":"04-15","to":"11-01"}],
    "15 AVRIL AU 1 NOVEMBRE":[{"from":"04-15","to":"11-01"}],
    "15 AVRIL AU 15 NOVEMBRE":[{"from":"04-15","to":"11-15"}],
    "15 AVR - 15 NOV":[{"from":"04-15","to":"11-15"}],
    "15 AVR AU 15 NOV":[{"from":"04-15","to":"11-15"}],
    "15 AVRIL AU 1ER DEC":[{"from":"05-15","to":"12-01"}],
    "MAI-JUIN":[{"from":"05-01","to":"06-01"}],
    "1MAI AU 1 SEPT":[{"from":"05-01","to":"09-01"}],
    "1MAI AU 1OCT":[{"from":"05-01","to":"10-01"}],
    "1 MAI AU 1 NOV":[{"from":"06-01","to":"11-01"}],
    "15 MAI AU 15 OCT":[{"from":"05-15","to":"10-15"}],
    "15 MAI AU 15 SEPT":[{"from":"05-15","to":"09-15"}],
    "1 JUIN AU 1 OCT":[{"from":"06-01","to":"10-01"}],
    "15 JUIN AU 1ER SEPT.":[{"from":"06-15","to":"09-01"}],
    "21 JUIN AU 1 SEPT":[{"from":"06-21","to":"09-01"}],
    "30 JUIN AU 30 AOUT":[{"from":"06-30","to":"08-30"}],
    "16 JUIL. AU 4 SEPT.":[{"from":"07-16","to":"09-04"}],
    "15 AOUT - 28 JUIN":[{"from":"08-15","to":"06-28"}],
    "20 AOÛT AU 30 JUIN":[{"from":"08-20","to":"06-30"}],
    "1 SEPT. AU 23 JUIN":[{"from":"09-01","to":"06-23"}],
    "SEPT A JUIN":[{"from":"09-01","to":"06-30"}],
    "SEPT À JUIN":[{"from":"09-01","to":"06-30"}],
    "SEPT. A JUIN":[{"from":"09-01","to":"06-30"}],
    "SEPT. À JUIN":[{"from":"09-01","to":"06-30"}],
    "1 SEPT. AU 30 JUIN":[{"from":"09-01","to":"06-30"}],
    "1 SEPT. AU 31 MAI":[{"from":"09-01","to":"05-31"}],
    "1ER SEPT AU 31 MAI":[{"from":"09-01","to":"05-31"}],
    "1 NOV. AU 31 MARS":[{"from":"11-01","to":"03-31"}],
    "1 NOV. AU 1 AVRIL":[{"from":"11-01","to":"04-01"}],
    "1 NOVEMBRE AU 15 AVRIL":[{"from":"11-01","to":"04-15"}],
    "1 NOV. AU 1 MAI":[{"from":"11-01","to":"05-01"}],
    "15 NOV. AU 15 MARS":[{"from":"11-15","to":"03-15"}],
    "15 NOV. AU 1 AVRIL":[{"from":"11-15","to":"04-01"}],
    "15 NOV - 15 AVR":[{"from":"11-15","to":"04-15"}],
    "15NOV - 15AVRIL":[{"from":"11-15","to":"04-15"}],
    "16 NOV. AU 14 MARS":[{"from":"11-16","to":"03-14"}],
    "30 NOV - 1ER AVRIL":[{"from":"11-30","to":"04-01"}],
    "1 DEC. AU 1 MARS":[{"from":"12-01","to":"03-01"}],
    "1ER DECEMBRE AU 1ER MARS":[{"from":"12-01","to":"03-01"}],
    "1 DEC. AU 1 AVRIL":[{"from":"12-01","to":"04-01"}]
};

function getEffectiveDates(description) {
    Object.entries(monthValues)
    .reduce( (ret,val) => {
        description.includes(val[0]) ? val[1] : ret;
    }, undefined);
}

const dayValues = {
    "mo":["LUNDI","LUN\\.","LUN"],
    "tu":["MARDI","MAR\\.","MAR"],
    "we":["MERCREDI","MER\\.","MER"],
    "th":["JEUDI","JEU\\.","JEU"],
    "fr":["VENDREDI","VEN\\.","VEN","VEMDREDI"],
    "sa":["SAMEDI","SAM\\.","SAM"],
    'su':["DIMANCHE","DIM\\.","DIM"]
};
const dayMap = Object.entries(dayValues).reduce((acc,val)=>{
    const [key, value] = val;
    value.forEach(val2=>acc[val2.replace("\\","")]=key);
    return acc;
}, {});
const dayText = Object.values(dayValues).flat().join('|');
const threeDaysRegex = new RegExp(`(${dayText})\\s(${dayText})\\s(${dayText})`);

function getDaysOfWeek(description) {
    let days = [];
    const threeDaysRule = threeDaysRegex.exec(description);
    if(threeDaysRule){
        days.push(dayMap[threeDaysRule[1]]);
        days.push(dayMap[threeDaysRule[2]]);
        days.push(dayMap[threeDaysRule[3]]);
    } else {
        const daysRegex = new RegExp(`(${dayText})(\\s?\\S*\\s)(${dayText})`);
        const daysRule = daysRegex.exec(description);

        if(daysRule){
            if(/.*(A|À|AU).*/.exec(daysRule[2])) {
                const daysAbbr = Object.keys(dayValues);
                days = daysAbbr.slice(daysAbbr.findIndex(val=>val===dayMap[daysRule[1]]),daysAbbr.findIndex(val=>val===dayMap[daysRule[3]])+1)
            } else if(/(ET|\s)/.exec(daysRule[2])) {
                days.push(dayMap[daysRule[1]]);
                days.push(dayMap[daysRule[3]]);
            } else {
                console.error("day rules verbe unknown",daysRule[2], rpaCode, description);
            }
        } else {
            const dayRegex = new RegExp(`(${dayText})`);
            const dayRule = dayRegex.exec(description);
            if(dayRule) {
                days.push(dayMap[dayRule[1]]);
            }
        }
    }

    return (days.length != 0) ? {days} : undefined;
}

const timeRegexp = /(\d+[H]\d*)\s?[Aaà@-]\s?(\d+[H]\d*)/g;

function convert(rpaCodification) {
    const rpaIds = rpaCodification.PANNEAU_ID_RPA;
    const rpaDescriptions = rpaCodification.DESCRIPTION_RPA;
    const rpaCodes = rpaCodification.CODE_RPA;
    const rpaInfos = {};

    for (let [key, rpaId] of Object.entries(rpaIds)) {
        const rpaInfo = {}
        rpaInfos[rpaId] = rpaInfo

        rpaInfo.description = rpaDescriptions[key];
        rpaInfo.code = rpaCodes[key];

        description = rpaDescriptions[key].toUpperCase();

        if (containsIrrelevantExpression(description)) {
            continue;
        }

        let activity = getActivity(description);
        if (activity === undefined) {
            continue;
        }

        let timeSpans = [];
        let timeSpan = {};

        timeSpan["effectiveDates"] = getEffectiveDates(description);
        timeSpan["daysOfWeek"] = getDaysOfWeek(description);

        //   ********** time
        if(time = timeRegexp.exec(description)){
            do{
                const convertHtime = (time) => {
                    [h,m] = time.split("H")
                    if(!m){
                        m="00"
                    }
                    return `${h.padStart(2,'0')}:${m}`
                }
                if(time){
                    startTime = convertHtime(time[1]);
                    endTime = convertHtime(time[2]);
                }

                if(startTime && endTime) {
                    timeSpan['timesOfDay'] = [{
                        from: startTime,
                        to: endTime
                    }]
                }

                if(Object.keys(timeSpan).length){
                    timeSpans.push({...timeSpan});
                }
            } while(time = timeRegexp.exec(description))
        } else {
            if(Object.keys(timeSpan).length){
                timeSpans.push({...timeSpan});
            }
        }

        const priorityCategory = timeSpans.length>0?"3":"4";
        
        if(activity){
            rpaInfo['regulations'] = [{
                priorityCategory,
                rule:{
                    activity
                },
                timeSpans
            }];
        } else if(timeSpans.length>0){
            rpaInfo['regulations'] = [{
                timeSpans
            }];
        }
    }
    return rpaInfos;
}

if (typeof require !== 'undefined' && require.main === module) {
    const inputFilename = process.argv[2];
    const outputFilename = process.argv[3];

    const rpaCodificationJson = fs.readFileSync(inputFilename);
    const rpaCodification = JSON.parse(rpaCodificationJson);

    const rpaInfos = convert(rpaCodification);
    const rpaInfosJson = JSON.stringify(rpaInfos, null, 2);
    fs.writeFile(outputFilename, rpaInfosJson, err => {if (err) throw err});
}

module.exports = {
    convert,
    getActivity,
    getEffectiveDates,
    getDaysOfWeek,
    descriptionContainsTimespan
};
