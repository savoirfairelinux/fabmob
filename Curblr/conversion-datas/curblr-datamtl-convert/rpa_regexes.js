// one or two digits, followed by zero or more spaces, followed by "h", followed by 0 to two digits
const timeStr = "\\d{1,2}\\s*h\\d{0,2}";
const time = new RegExp(timeStr, "i");

const timeIntervalStr = `(?:${timeStr})\\s*[Aaà@-]\\s*(?:${timeStr})`;
const timeInterval = new RegExp(timeIntervalStr, "i");

// one or two digits, followed by zero or more spaces, followed by "min"
const maxStayStr = "\\d{1,2}\\s*min";
const maxStay = new RegExp(maxStayStr, "i");

// match a sequence of time intervals
// examples: "6h-7h30", "6h-7h30, 8h-10",  or "6h-7h30 8h À 10h et 11h@12h"
const timesSequenceStr = `(?:${timeIntervalStr})(?:,?\\s+(?:et\\s+)?(?:${timeIntervalStr}))*`;
const timesSequence = new RegExp(timesSequenceStr, "i");

// mapping of days of the week with the regex that will match that day
const daysOfWeekStrs = {
    // beginning of a word, followed by the truncated name of a day or its complete name
    "mo": "\\blun(?:\\b|di)",
    "tu": "\\bmar(?:\\b|di)",
    "we": "\\bmer(?:\\b|credi)",
    "th": "\\bjeu(?:\\b|di)",
    "fr": "\\bve[nm](?:\\b|dredi)", // there is a typo in the data
    "sa": "\\bsam(?:\\b|edi)",
    "su": "\\bdim(?:\\b|anche)"
};
const daysOfWeek = Object.entries(daysOfWeekStrs)
                          .reduce( (acc, [key, value]) => {
                              acc[key] = new RegExp(value, "i");
                              return acc;
                            }, {});

// regex that will match any day of the week
const anyDayOfWeekStr = Object.values(daysOfWeekStrs).join("|");
const anyDayOfWeek = new RegExp(anyDayOfWeekStr, "i");

// regex that will match any interval of days
const daysOfWeekIntervalStr = `(${anyDayOfWeekStr})\\s+(?:A|À|AU)\\s+(${anyDayOfWeekStr})`;
const daysOfWeekInterval = new RegExp(daysOfWeekIntervalStr, "i");

// Matches an enumeration of days
const daysOfWeekEnumerationStr = `(${anyDayOfWeekStr})(?:\\s+(?:et\\s+)?(?:${anyDayOfWeekStr}))*`
const daysOfWeekEnumeration = new RegExp(daysOfWeekEnumerationStr, "i");

// Matches week times
const weekTimeStr = `(?:${timesSequenceStr})\\s*(?:(?:${daysOfWeekIntervalStr})|(?:${daysOfWeekEnumerationStr}))?`
const weekTime = new RegExp(weekTimeStr, "ig");

// mapping of months names with the regex that will match that month
const monthsStrs = {
    // a digit or the beginning of a word, followed by the truncated name of a month or its complete name.
    "01": "(?:\\d|\\b)jan(?:\\b|vier)",
    "02": "(?:\\d|\\b)f[eé]v(?:\\b|rier)",
    "03": "(?<!de-)(?:\\d|\\b)mar(?:\\b|s)", // exclude champ-de-mars
    "04": "(?:\\d|\\b)avr(?:\\b|il)",
    "05": "(?:\\d|\\b)mai",
    "06": "(?:\\d|\\b)juin",
    "07": "(?:\\d|\\b)jui(?:\\b|llet)",
    "08": "(?:\\d|\\b)ao[uû]t",
    "09": "(?:\\d|\\b)sep(?:\\b|tembre)",
    "10": "(?:\\d|\\b)oct(?:\\b|obre)",
    "11": "(?:\\d|\\b)nov(?:\\b|embre)",
    "12": "(?:\\d|\\b)d[eé]c(?:\\b|embre)",
}
const months = Object.entries(monthsStrs)
                          .reduce( (acc, [key, value]) => {
                              acc[key] = new RegExp(value);
                              return acc;
                            }, {});

// regex that will match any month
const anyMonthStr = Object.values(monthsStrs).join("|");
const anyMonth = new RegExp(anyMonthStr, "i");

// regex that will match any day of the month for which the day comes before the month
// One or two digits, followed by zero or more whitespaces, followed by any month
const dayOfMonthDayFirstStr = `(?:\\d{1,2}|1er) *(?:${anyMonthStr})`;
const dayOfMonthDayFirst = new RegExp(dayOfMonthDayFirstStr, "i");

// regex that will match any day of the month for which the day comes after the month
// Any month, followed by zero or more whitespaces, followed by one or two digits
const dayOfMonthDaySecondStr = `(?:${anyMonthStr}) *(?:\\d{1,2}|1er)`;
const dayOfMonthDaySecond = new RegExp(dayOfMonthDaySecondStr, "i");

// regex that will match days of the month with the day and the month separated by a slash
// The month is expressed with its number. Ex: 12/12
const dayOfMonthSlashedStr = "\\d{2}/\\d{2}";
const dayOfMonthSlashed = new RegExp(dayOfMonthSlashedStr, "i");

// regex will match any interval of days of the month, for which the day comes before the month
const daysOfMonthIntervalDayFirstStr = `(?:${dayOfMonthDayFirstStr})\\s*(?:A|À|AU|-)\\s*(?:${dayOfMonthDayFirstStr})`;
const daysOfMonthIntervalDayFirst = new RegExp(daysOfMonthIntervalDayFirstStr, "i");

// regex will match any interval of days of the month, for which the day comes after the month
const daysOfMonthIntervalDaySecondStr = `(?:${dayOfMonthDaySecondStr})\\s*(?:A|À|AU|-)\\s*(?:${dayOfMonthDaySecondStr})`;
const daysOfMonthIntervalDaySecond = new RegExp(daysOfMonthIntervalDaySecondStr, "i");

// regex will match any interval of days of the month, for which the day is not indicated
const daysOfMonthIntervalDayAbsentStr = `(?:${anyMonthStr})\\s*(?:A|À|AU|-)\\s*(?:${anyMonthStr})`;
const daysOfMonthIntervalDayAbsent = new RegExp(daysOfMonthIntervalDayAbsentStr, "i");


const daysOfMonthIntervalSlashedStr = `(?:${dayOfMonthSlashedStr})\\s*(?:A|À|AU|-)\\s*(?:${dayOfMonthSlashedStr})`;
const daysOfMonthIntervalSlashed = new RegExp(daysOfMonthIntervalSlashedStr, "i");

// regex will match any interval of days of the month
const daysOfMonthIntervalStr = `(?:${daysOfMonthIntervalDayFirstStr})|(?:${daysOfMonthIntervalDaySecondStr})|${daysOfMonthIntervalDayAbsentStr}|${daysOfMonthIntervalSlashedStr}`;
const daysOfMonthInterval = new RegExp(daysOfMonthIntervalStr, "i");

const anyTimespanStr = [
    timeStr,
    maxStayStr,
    anyDayOfWeekStr,
    anyMonth,
].join("|")
const anyTimespan = new RegExp(anyTimespanStr, "i");

const noTimespanBeforeStr = `(?<!(${anyTimespanStr}).*)`;
const noTimespanAfterStr = `(?!.*(${anyTimespanStr}))`;

module.exports = {
    time,
    timeInterval,
    maxStay,
    timesSequence,
    daysOfWeek,
    anyDayOfWeek,
    daysOfWeekInterval,
    daysOfWeekEnumeration,
    months,
    anyMonth,
    dayOfMonthDayFirst,
    dayOfMonthDaySecond,
    dayOfMonthSlashed,
    daysOfMonthIntervalDayFirst,
    daysOfMonthIntervalDaySecond,
    daysOfMonthIntervalDayAbsent,
    daysOfMonthIntervalSlashed,
    daysOfMonthInterval,
    anyTimespan,
    weekTime
}