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
    rpaReg.dayOfMonthDayFirst.lastIndex = 0;
    const from = rpaReg.dayOfMonthDayFirst.exec(dayOfMonthInterval)[0];
    const to = rpaReg.dayOfMonthDayFirst.exec(dayOfMonthInterval)[0];
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
    rpaReg.dayOfMonthDaySecond.lastIndex = 0;
    const from = rpaReg.dayOfMonthDaySecond.exec(dayOfMonthInterval)[0];
    const to = rpaReg.dayOfMonthDaySecond.exec(dayOfMonthInterval)[0];
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
    rpaReg.anyMonth.lastIndex = 0;
    const from = rpaReg.anyMonth.exec(dayOfMonthInterval)[0];
    const to = rpaReg.anyMonth.exec(dayOfMonthInterval)[0];
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
    rpaReg.dayOfMonthSlashed.lastIndex = 0;
    const from = rpaReg.dayOfMonthSlashed.exec(dayOfMonthInterval)[0];
    const to = rpaReg.dayOfMonthSlashed.exec(dayOfMonthInterval)[0];
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

function extractDayOfWeek(string) {
    return Object.entries(rpaReg.daysOfWeek).find( ([dayAbbreviation, regex]) => {
        if (regex.test(string)) {
            return true;
        }
    })?.[0];
}

// Get an interval of days. Days separated with "A", "À", "AU",
// ex: "LUN A MAR"
const orderedDays = ["mo", "tu", "we", "th", "fr", "sa", "su", "mo", "tu", "we", "th", "fr", "sa"];
function getDaysOfWeekFromInterval(weekTimeDescription) {
    rpaReg.anyDayOfWeek.lastIndex = 0;
    const startDayDescription = rpaReg.anyDayOfWeek.exec(weekTimeDescription)?.[0];
    const endDayDescription = rpaReg.anyDayOfWeek.exec(weekTimeDescription)?.[0];
    const startDay = extractDayOfWeek(startDayDescription);
    const endDay = extractDayOfWeek(endDayDescription);
    const startDayIndex = orderedDays.indexOf(startDay);
    const endDayIndex = orderedDays.indexOf(endDay, startDayIndex);
    const days = orderedDays.slice(startDayIndex, endDayIndex + 1);
    return (days.length != 0) ? {days} : undefined;
}

// Get an enumeration of days. Days separated with spaces or "ET"
// ex: "LUN MAR JEU", "LUN ET MAR ET JEU"
function getDaysOfWeekFromEnumeration(weekTimeDescription) {
    const days = [];
    let dayDescription;
    rpaReg.anyDayOfWeek.lastIndex = 0;
    while (dayDescription = rpaReg.anyDayOfWeek.exec(weekTimeDescription)?.[0]) {
        const day = extractDayOfWeek(dayDescription);
        days.push(day)
    }
    return (days.length != 0) ? {days} : undefined;
}

function getDaysOfWeek(weekTimeDescription) {
    let days;
    rpaReg.daysOfWeekInterval.lastIndex = 0;
    rpaReg.daysOfWeekEnumeration.lastIndex = 0;
    if (rpaReg.daysOfWeekInterval.test(weekTimeDescription)) {
        return getDaysOfWeekFromInterval(weekTimeDescription)
    }
    if (rpaReg.daysOfWeekEnumeration.test(weekTimeDescription)) {
        return getDaysOfWeekFromEnumeration(weekTimeDescription);
    }
}

function convertHtime(time) {
    let [h,m] = time.toUpperCase().split("H");
    if (!m) {
        m = "00"
    }
    return `${h.padStart(2,'0')}:${m}`
}

function getTimeOfDay(timeOfDayDescription) {
    rpaReg.time.lastIndex = 0;
    const startTime = rpaReg.time.exec(timeOfDayDescription)?.[0];
    const endTime = rpaReg.time.exec(timeOfDayDescription)?.[0];
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
    rpaReg.timeInterval.lastIndex = 0;
    while (timeOfDayDescription = rpaReg.timeInterval.exec(description)?.[0]) {
        const timeOfDay = getTimeOfDay(timeOfDayDescription)
        timesOfDay.push(timeOfDay)
    }
    return (timesOfDay.length != 0) ? timesOfDay : undefined;
}

// Get a list of timespans from the syntax where the time overlaps multiple days.
// ex: LUN 17H À MAR 17H
function getTimeSpansFromDaysOverlapSyntax(description, effectiveDates) {
    const timeSpans = [];
    rpaReg.time.lastIndex = 0;
    const startTimeDescription = rpaReg.time.exec(description)?.[0];
    const startTime = convertHtime(startTimeDescription);
    const endTimeDescription = rpaReg.time.exec(description)?.[0];
    const endTime = convertHtime(endTimeDescription);
    const days = getDaysOfWeekFromInterval(description)["days"];

    // start timeSpan
    timeSpans.push({
        "effectiveDates": effectiveDates,
        "daysOfWeek": {"days": [days[0]]},
        "timesOfDay": {"from": startTime, "to": "23:59"}
    });

    // midde timeSpans
    if (days.length > 2) {
        timeSpans.push({
            "effectiveDates": effectiveDates,
            "daysOfWeek": {"days": days.slice(1, days.length-1)},
            "timesOfDay": {"from": "00:00", "to": "23:59"}
        });
    }

    // end timeSpan
    timeSpans.push({
        "effectiveDates": effectiveDates,
        "daysOfWeek": {"days": [days[days.length-1]]},
        "timesOfDay": {"from": "00:00", "to": endTime}
    });

    return timeSpans
}

// Return a single timespan for all syntaxes except the one handled by getTimeSpansFromDaysOverlapSyntax
// ex: "1H-2H", "LUN À VEN", "LUN ET VEN", "LUN 1H-2H", "1H-2H LUN"
function getTimeSpan(description, effectiveDates) {
    const timeSpan = {};

    timeSpan["effectiveDates"] = effectiveDates;
    timeSpan["daysOfWeek"] = getDaysOfWeek(description);
    timeSpan["timesOfDay"] = getTimesOfDay(description);
    
    return timeSpan;
}

function getTimeSpans(description) {
    const timeSpans = [];

    // We assume there is only one set of effective dates
    const effectiveDates = getEffectiveDates(description);

    let timeSpanDescription;
    rpaReg.weekTime.lastIndex = 0;
    while (timeSpanDescription = rpaReg.weekTime.exec(description)?.[0]) {
        rpaReg.weekTimeDaysOverlap.lastIndex = 0;
        if (rpaReg.weekTimeDaysOverlap.exec(timeSpanDescription)) {
            // special syntax
            const daysOverlapTimespans = getTimeSpansFromDaysOverlapSyntax(timeSpanDescription, effectiveDates);
            timeSpans.push(...daysOverlapTimespans);
        }
        else {
            // All the other syntaxes can be handled the same way
            const timeSpan = getTimeSpan(timeSpanDescription, effectiveDates);
            timeSpans.push(timeSpan);
        }
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
    extractDayOfWeek,
    getDaysOfWeekFromEnumeration,
    getDaysOfWeekFromInterval,
    getTimeSpansFromDaysOverlapSyntax,
};
