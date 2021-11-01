// one or two digits, followed by zero or more spaces, followed by "h", followed by 0 to two digits
const timeStr = "\\d{1,2}\\s*h\\d{0,2}";
const time = new RegExp(timeStr, "i");

const timeIntervalStr = `(${timeStr})\\s*[Aaà@-]\\s*(${timeStr})`;
const timeInterval = new RegExp(timeIntervalStr, "i");

// one or two digits, followed by zero or more spaces, followed by "min"
const maxStayStr = "\\d{1,2}\\s*min";
const maxStay = new RegExp(maxStayStr, "i");

// match a sequence of time intervals
// examples: "6h-7h30" or "6h-7h30 8h À 10h et 11h@12h"
const timesSequenceStr = `(${timeIntervalStr})(\\s+(?:et\\s+)?(${timeIntervalStr}))*`;
const timesSequence = new RegExp(timesSequenceStr, "i");

// mapping of days of the week with the regex that will match that day
const daysStrs = {
    // beginning of a word, followed by the truncated name of a day or its complete name
    "mo": "\\blun(?:\\b|di)",
    "tu": "\\bmar(?:\\b|di)",
    "we": "\\bmer(?:\\b|credi)",
    "th": "\\bjeu(?:\\b|di)",
    "fr": "\\bve[nm](?:\\b|dredi)", // there is a typo in the data
    "sa": "\\bsam(?:\\b|edi)",
    "su": "\\bdim(?:\\b|anche)"
};
const days = Object.entries(daysStrs)
                          .reduce( (acc, [key, value]) => {
                              acc[key] = new RegExp(value, "i");
                              return acc;
                            }, {});

// regex that will match any day of the week
const anyDayStr = Object.values(daysStrs).join("|");
const anyDay = new RegExp(anyDayStr, "i");

// regex that will match any interval of time
const daysIntervalStr = `(${anyDayStr})\\s+(?:A|À|AU)\\s+(${anyDayStr})`;
const daysInterval = new RegExp(daysIntervalStr, "i");

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

// regex that will match any day of the week
const anyMonthStr = Object.values(monthsStrs).join("|");
const anyMonth = new RegExp(anyMonthStr, "i");

const anyTimespanStr = [
    timeStr,
    maxStayStr,
    anyDayStr,
    anyMonth,
].join("|")
const anyTimespan = new RegExp(anyTimespanStr, "i");

const noTimespanBeforeStr = `(?<!(${anyTimespanStr}).*)`;
const noTimespanAfterStr = `(?!.*(${anyTimespanStr}))`;

module.exports = {
    timeStr,
    time,
    timeIntervalStr,
    timeInterval,
    maxStayStr,
    maxStay,
    timesSequenceStr,
    timesSequence,
    daysStrs,
    days,
    anyDayStr,
    anyDay,
    daysIntervalStr,
    daysInterval,
    monthsStrs,
    months,
    anyMonthStr,
    anyMonth,
    anyTimespanStr,
    anyTimespan,
    noTimespanBeforeStr,
    noTimespanAfterStr
}