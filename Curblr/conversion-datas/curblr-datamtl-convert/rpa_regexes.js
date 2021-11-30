// one or two digits, followed by zero or more spaces, followed by "h", followed by 0 to two digits
const timeStr = "\\d{1,2}\\s*h\\d{0,2}";
const time = new RegExp(timeStr, "ig");

const timeIntervalStr = `(?:${timeStr})\\s*[Aaà@-]\\s*(?:${timeStr})`;
const timeInterval = new RegExp(timeIntervalStr, "ig");

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
    "mo": "\\blun(?:\\.|\\b|di)",
    "tu": "\\bmar(?:\\.|\\b|di)",
    "we": "\\bmer(?:\\.|\\b|credi)",
    "th": "\\bjeu(?:\\.|\\b|di)",
    "fr": "\\bve[nm](?:\\.|\\b|dredi)", // there is a typo in the data
    "sa": "\\bsam(?:\\.|\\b|edi)",
    "su": "\\bdim(?:\\.|\\b|anche)"
};
const daysOfWeek = Object.entries(daysOfWeekStrs)
                          .reduce( (acc, [key, value]) => {
                              acc[key] = new RegExp(value, "i");
                              return acc;
                            }, {});

// regex that will match any day of the week
const anyDayOfWeekStr = Object.values(daysOfWeekStrs).join("|");
const anyDayOfWeek = new RegExp(anyDayOfWeekStr, "ig");

// regex that will match any interval of days
// Day of week not preceded or followed by A|À|AU, optionnaly followed by ET, and optionnaly followed by more days
const daysOfWeekIntervalStr = `(${anyDayOfWeekStr})\\s*(?:A|À|AU)\\s+(${anyDayOfWeekStr})`;
const daysOfWeekInterval = new RegExp(daysOfWeekIntervalStr, "ig");

// Matches an enumeration of days
const daysOfWeekEnumerationStr = `(?<!(?:A|À|AU)\\s+)(${anyDayOfWeekStr})(?!\\s*(?:A|À|AU))(?:\\s*(?:et\\s+)?(?:${anyDayOfWeekStr}))*`
const daysOfWeekEnumeration = new RegExp(daysOfWeekEnumerationStr, "ig");

// Either an interval of days or an enumeration of days
const daysOfTimeSpanStr = `(?:${daysOfWeekIntervalStr})|(?:${daysOfWeekEnumerationStr})`;

const separatorDaysWithTimeStr = "\\s*(?:-\\s*)?"

// Matches week times, for which the days come before the times
// days of week, followed by spaces and optionally a -, followed by time sequence
const weekTimeDaysFirstStr = `(?:${daysOfTimeSpanStr})${separatorDaysWithTimeStr}(?:${timesSequenceStr})`
const weekTimeDaysFirst = new RegExp(weekTimeDaysFirstStr, "ig");

// Matches week times, for which the days come after the times
// time sequence, followed by spaces and optionally a -, followed by days of week
const weekTimeDaysSecondStr = `(?:${timesSequenceStr})${separatorDaysWithTimeStr}(?:(?:${daysOfTimeSpanStr}))`
const weekTimeDaysSecond = new RegExp(weekTimeDaysSecondStr, "ig");

// Matches week times, for which the days are absent
// time sequence, not preceded by days and spaces, not followed by days and spaces.
const weekTimeDaysAbsentStr = `(?<!(?:${anyDayOfWeekStr})${separatorDaysWithTimeStr})(?:${timesSequenceStr})(?!${separatorDaysWithTimeStr}(?:${anyDayOfWeekStr}))`
const weekTimeDaysAbsent = new RegExp(weekTimeDaysAbsentStr, "ig");

// Matches week times, for which the hours are absent
// days sequence, not preceded by hours and spaces, not followed by hours and spaces.
const weekTimeDaysOnlyStr = `(?<!(?:${timeStr})${separatorDaysWithTimeStr})(?:${daysOfTimeSpanStr})(?!${separatorDaysWithTimeStr}(?:${timeStr}))`
const weekTimeDaysOnly = new RegExp(weekTimeDaysOnlyStr, "ig");

// Match periods of time that overlap over multiple days
// ex: MER 17H À JEU 17H
const weekTimeDaysOverlapStr = `(${anyDayOfWeekStr})(${separatorDaysWithTimeStr}${timeStr})\\s+À\\s+(${anyDayOfWeekStr})(${separatorDaysWithTimeStr}${timeStr})`;
const weekTimeDaysOverlap = new RegExp(weekTimeDaysOverlapStr, "ig");

// Match any syntax of week times
const weekTimeStr = `(?:(${weekTimeDaysFirstStr})|(${weekTimeDaysSecondStr})|(${weekTimeDaysAbsentStr})|(${weekTimeDaysOnlyStr})|(${weekTimeDaysOverlapStr}))`;
const weekTime = new RegExp(weekTimeStr, "ig");

// mapping of months names with the regex that will match that month
const monthsStrs = {
    // the truncated name of a month or its complete name.
    "01": "jan(?:\\.|\\b|vier)",
    "02": "f[eé]v(?:\\.|\\b|rier)",
    "03": "(?<!de-)m(?:a)?r(?:\\.|\\b|s)(:?l)?", // exclude champ-de-mars
    "04": "av(?:r)?(?:\\.|\\b|il)(:?s)?",
    "05": "mai\\b",
    "06": "juin\\b",
    "07": "juil(?:\\.|\\b|let)",
    "08": "ao[uû]t\\b",
    "09": "sept(?:\\.|\\b|embre)",
    "10": "oct(?:\\.|\\b|obre)",
    "11": "nov(?:\\.|\\b|embre)",
    "12": "d[eé]c(?:\\.|\\b|embre)",
}
const months = Object.entries(monthsStrs)
                          .reduce( (acc, [key, value]) => {
                              acc[key] = new RegExp(value, "i");
                              return acc;
                            }, {});

// regex that will match any month
const anyMonthStr = Object.values(monthsStrs).join("|");
const anyMonth = new RegExp(anyMonthStr, "ig");

// regex that will match any day of the month for which the day comes before the month
// One or two digits, followed by zero or more whitespaces, followed by any month
const dayOfMonthDayFirstStr = `(?:\\d{1,2}|1er) *(?:${anyMonthStr})`;
const dayOfMonthDayFirst = new RegExp(dayOfMonthDayFirstStr, "ig");

// regex that will match any day of the month for which the day comes after the month
// Any month, followed by zero or more whitespaces, followed by one or two digits
const dayOfMonthDaySecondStr = `(?:${anyMonthStr}) *(?:\\d{1,2}|1er)`;
const dayOfMonthDaySecond = new RegExp(dayOfMonthDaySecondStr, "ig");

// regex that will match days of the month with the day and the month separated by a slash
// The month is expressed with its number. Ex: 12/12
const dayOfMonthSlashedStr = "\\d{2}/\\d{2}";
const dayOfMonthSlashed = new RegExp(dayOfMonthSlashedStr, "ig");

// regex will match any interval of days of the month, for which the day comes before the month
const daysOfMonthIntervalDayFirstStr = `(?:${dayOfMonthDayFirstStr})\\s*(?:A|À|AU|ET|-)?\\s*(?:${dayOfMonthDayFirstStr})`;
const daysOfMonthIntervalDayFirst = new RegExp(daysOfMonthIntervalDayFirstStr, "i");

// regex will match any interval of days of the month, for which the day comes after the month
const daysOfMonthIntervalDaySecondStr = `(?:${dayOfMonthDaySecondStr})\\s*(?:A|À|AU|-)?\\s*(?:${dayOfMonthDaySecondStr})`;
const daysOfMonthIntervalDaySecond = new RegExp(daysOfMonthIntervalDaySecondStr, "i");

// regex will match any interval of days of the month, for which the day is not indicated
const daysOfMonthIntervalDayAbsentStr = `(?:${anyMonthStr})\\s*(?:A|À|AU|-)?\\s*(?:${anyMonthStr})`;
const daysOfMonthIntervalDayAbsent = new RegExp(daysOfMonthIntervalDayAbsentStr, "i");


const daysOfMonthIntervalSlashedStr = `(?:${dayOfMonthSlashedStr})\\s*(?:A|À|AU|-)?\\s*(?:${dayOfMonthSlashedStr})`;
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
    weekTimeDaysFirst,
    weekTimeDaysSecond,
    weekTimeDaysAbsent,
    weekTimeDaysOnly,
    weekTimeDaysOverlap,
    weekTime,
}