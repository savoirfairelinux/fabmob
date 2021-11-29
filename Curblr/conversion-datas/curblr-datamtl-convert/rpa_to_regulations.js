const fs = require('fs');
const rpaReg = require("./rpa_regexes")

function descriptionContainsTimespan(description) {
    return rpaReg.anyTimespan.test(description);
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

function extractFirstTwoDigitsNumber(string) {
    const number = /\d{1,2}/.exec(string)?.[0];
    return number?.padStart(2,'0');
}

// Extract a month from a string. Not sure which one when more than two
function extractMonth(string) {
    return Object.entries(rpaReg.months).find( ([monthNumber, regex]) => {
        if (regex.test(string)) {
            return true;
        }
    })?.[0];
}

// Get effective dates for dates which the day is before the month
// ex: 1 MARS AU 1 DEC
function getEffectiveDatesFromDayFirstSyntax(dayOfMonthInterval) {
    const from = rpaReg.dayOfMonthDayFirst.exec(dayOfMonthInterval)[0];
    const to = rpaReg.dayOfMonthDayFirst.exec(dayOfMonthInterval)[0];
    rpaReg.dayOfMonthDayFirst.lastIndex = 0;
    const fromDay = extractFirstTwoDigitsNumber(from);
    const fromMonth = extractMonth(from);
    const toDay = extractFirstTwoDigitsNumber(to);
    const toMonth = extractMonth(to);
    return [{
        "from": `${fromMonth}-${fromDay}`,
        "to": `${toMonth}-${toDay}`
    }];
}

// Get effective dates for dates which the day is after the month
// ex: MARS 1 AU DEC 1
function getEffectiveDatesFromDaySecondSyntax(dayOfMonthInterval) {
    const from = rpaReg.dayOfMonthDaySecond.exec(dayOfMonthInterval)[0];
    const to = rpaReg.dayOfMonthDaySecond.exec(dayOfMonthInterval)[0];
    rpaReg.dayOfMonthDaySecond.lastIndex = 0;
    const fromDay = extractFirstTwoDigitsNumber(from);
    const fromMonth = extractMonth(from);
    const toDay = extractFirstTwoDigitsNumber(to);
    const toMonth = extractMonth(to);
    return [{
        "from": `${fromMonth}-${fromDay}`,
        "to": `${toMonth}-${toDay}`
    }];
}

// Get effective dates for dates which the day is absent
// ex: MARS - DEC 
function getEffectiveDatesFromDayAbsentSyntax(dayOfMonthInterval) {
    const from = rpaReg.anyMonth.exec(dayOfMonthInterval)[0];
    const to = rpaReg.anyMonth.exec(dayOfMonthInterval)[0];
    rpaReg.anyMonth.lastIndex = 0;
    const fromMonth = extractMonth(from);
    const toMonth = extractMonth(to);

    const toDay = (() => {
        if (["04", "06", "09", "01"].includes(toMonth)) {
            return "30";
        }
        else if (toMonth == "02") {
            return "28";
        }
        else {
            return "31";
        }
    })();

    return [{
        "from": `${fromMonth}-01`,
        "to": `${toMonth}-${toDay}`
    }];
}

// Get effective dates for dates which the day and month are numbers separated with a slash
// ex: 01/03 - 01/11
function getEffectiveDatesFromSlashedSyntax(dayOfMonthInterval) {
    const from = rpaReg.dayOfMonthSlashed.exec(dayOfMonthInterval)[0];
    const to = rpaReg.dayOfMonthSlashed.exec(dayOfMonthInterval)[0];
    rpaReg.dayOfMonthSlashed.lastIndex = 0;
    const fromDay = from.slice(0, 2);
    const fromMonth = from.slice(3, 5);
    const toDay = to.slice(0, 2);
    const toMonth = to.slice(3, 5);
    return [{
        "from": `${fromMonth}-${fromDay}`,
        "to": `${toMonth}-${toDay}`
    }];
}

function getEffectiveDates(description) {
    // We assume there is only one set of effective dates
    const daysOfMonthInterval = rpaReg.daysOfMonthInterval.exec(description)?.[0];

    if (!daysOfMonthInterval) {
        return undefined;
    }

    if (rpaReg.daysOfMonthIntervalDayFirst.test(daysOfMonthInterval)) {
        return getEffectiveDatesFromDayFirstSyntax(daysOfMonthInterval);
    }
    if (rpaReg.daysOfMonthIntervalDaySecond.test(daysOfMonthInterval)) {
        return getEffectiveDatesFromDaySecondSyntax(daysOfMonthInterval);
    }
    if (rpaReg.daysOfMonthIntervalDayAbsent.test(daysOfMonthInterval)) {
        return getEffectiveDatesFromDayAbsentSyntax(daysOfMonthInterval);
    }
    if (rpaReg.daysOfMonthIntervalSlashed.test(daysOfMonthInterval)) {
        return getEffectiveDatesFromSlashedSyntax(daysOfMonthInterval);
    }
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

function convertHtime(time) {
    let [h,m] = time.toUpperCase().split("H");
    if (!m) {
        m = "00"
    }
    return `${h.padStart(2,'0')}:${m}`
}


function getTimeOfDay(timeOfDayDescription) {
    const startTime = rpaReg.time.exec(timeOfDayDescription)?.[0];
    const endTime = rpaReg.time.exec(timeOfDayDescription)?.[0];
    rpaReg.time.lastIndex = 0;
    if (startTime && endTime) {
        return {
            from: convertHtime(startTime),
            to: convertHtime(endTime)
        };
    }
    return undefined;
}

function getTimesOfDay(description) {
    const timesOfDay = [];
    let timeOfDayDescription;
    while (timeOfDayDescription = rpaReg.timeInterval.exec(description)?.[0]) {
        const timeOfDay = getTimeOfDay(timeOfDayDescription)
        timesOfDay.push(timeOfDay)
    }
    rpaReg.timeInterval.lastIndex = 0;
    return (timesOfDay.length != 0) ? timesOfDay : undefined;
}

function getTimeSpans(description) {
    const timeSpans = [];
    const timeSpan = {};

    timeSpan["effectiveDates"] = getEffectiveDates(description);
    timeSpan["daysOfWeek"] = getDaysOfWeek(description);
    timeSpan["timesOfDay"] = getTimesOfDay(description);

    if (Object.values(timeSpan).some( (value) => value !== undefined) ) {
        timeSpans.push(timeSpan);
    }

    return (timeSpans.length != 0) ? timeSpans : undefined;
}

function getRegulations(description) {
    const activity = getActivity(description);
    if (activity === undefined) {
        return undefined;
    }
    
    const timeSpans = getTimeSpans(description);

    const regulation = {
        // we assume regulations with timeSpans are more specific than those without, thus have higher priority
        "priorityCategory": timeSpans ? "3" : "4",
        "rule": (activity === null) ? undefined : { activity },
        "timeSpans": timeSpans
    };

    return [regulation];
}

function convert(rpaCodification) {
    const rpaIds = rpaCodification.PANNEAU_ID_RPA;
    const rpaDescriptions = rpaCodification.DESCRIPTION_RPA;
    const rpaCodes = rpaCodification.CODE_RPA;
    const rpaInfos = {};

    for (const [key, rpaId] of Object.entries(rpaIds)) {
        const rpaInfo = {}
        rpaInfos[rpaId] = rpaInfo
        rpaInfo.description = rpaDescriptions[key];
        rpaInfo.code = rpaCodes[key];

        const description = rpaDescriptions[key].toUpperCase();

        if (containsIrrelevantExpression(description)) {
            continue;
        }

        rpaInfo["regulations"] = getRegulations(description);
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
    getDaysOfWeek,
    getEffectiveDates,
    getRegulations,
    getTimeSpans,
    descriptionContainsTimespan,
    extractFirstTwoDigitsNumber,
    extractMonth,
    getEffectiveDatesFromDayFirstSyntax,
    getEffectiveDatesFromDaySecondSyntax,
    getEffectiveDatesFromDayAbsentSyntax,
    getEffectiveDatesFromSlashedSyntax,
    convertHtime,
    getTimeOfDay,
    getTimesOfDay,
};
