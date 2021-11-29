const rpaRegex = require("../rpa_regexes");

describe("times", () => {
    test.each([
        ["1h", true],
        ["1h5", true],
        ["1h30", true],
        ["10h", true],
        ["10h5", true],
        ["10h30", true],
        ["lundi1h", true],
        ["1hlundi", true],
        ["10", false],
        ["1ah", false],
        ["h30", false],
    ])("time.test('%s')", (value, expected) => {
        const result = rpaRegex.time.test(value);
        rpaRegex.time.lastIndex = 0;
        expect(result).toBe(expected);
    });

    test.each([
        ["1h-2h", true],
        ["1h - 2h", true],
        ["1hà2h", true],
        ["1h à 2h", true],
        ["1hÀ2h", true],
        ["1h À 2h", true],
        ["1ha2h", true],
        ["1h a 2h", true],
        ["1hA2h", true],
        ["1h A 2h", true],
        ["1h @ 2h", true],
        ["1h@2h", true],
        ["1h    -  2h", true],
        ["1h", false],
        ["1h 2h", false],
        ["1hb2h", false],
        ["1h b 2h", false],
        ["1hàa2h", false],
        ["lundi à vendredi", false],
    ])("timeInterval.test('%s')", (value, expected) => {
        const result = rpaRegex.timeInterval.test(value);
        rpaRegex.timeInterval.lastIndex = 0;
        expect(result).toBe(expected);
    });

    test.each([
        ["1h-2h", "1h-2h"],
        ["1h-2h 2h-3h", "1h-2h 2h-3h"],
        ["1h-2h 2h-3h 4h-5h", "1h-2h 2h-3h 4h-5h"],
        ["1h-2h 2h-3h 4h-5h 6h-7h", "1h-2h 2h-3h 4h-5h 6h-7h"],
        ["1h-2h et 2h-3h", "1h-2h et 2h-3h"],
        ["1h-2h et 2h-3h et 4h-5h", "1h-2h et 2h-3h et 4h-5h"],
        ["1h-2h et 2h-3h 4h-5h", "1h-2h et 2h-3h 4h-5h"],
        ["1h-2h lundi 2h-3h 4h-5h", "1h-2h"],
        ["06h30-09h30, 15h30-18h30", "06h30-09h30, 15h30-18h30"]
    ])("rpaRegex.timesSequence.exec('%s')[0]", (value, expected) => {
        const result = rpaRegex.timesSequence.exec(value)[0];
        expect(result).toBe(expected);
    });
});

describe("days", () => {
    test.each([
        ["LUN", true],
        ["LUN.", true],
        ["LUNDI", true],
        ["MAR", true],
        ["MAR.", true],
        ["MARDI", true],
        ["MER", true],
        ["MER.", true],
        ["MERCREDI", true],
        ["JEU", true],
        ["JEU.", true],
        ["JEUDI", true],
        ["VEN", true],
        ["VEN.", true],
        ["VEMDREDI", true],
        ["VENDREDI", true],
        ["SAM", true],
        ["SAM.", true],
        ["SAMEDI", true],
        ["DIM", true],
        ["DIM.", true],
        ["DIMANCHE", true],
        ["12h LUN 1 MARS", true],
        ["MONDAY", false],
        ["MARS", false],
    ])("anyDayOfWeek.test('%s')", (value, expected) => {
        const result = rpaRegex.anyDayOfWeek.test(value);
        rpaRegex.anyDayOfWeek.lastIndex = 0;
        expect(result).toBe(expected);
    });

    test.each([
        ["LUN À VEN", true],
        ["LUN A VEN", true],
        ["LUN AU VEN", true],
        ["LUN VEN", false],
        ["1h À 2h", false]
    ])("daysOfWeekInterval.test('%s')", (value, expected) => {
        const result = rpaRegex.daysOfWeekInterval.test(value);
        rpaRegex.daysOfWeekInterval.lastIndex = 0
        expect(result).toBe(expected);
    });

    test.each([
        ["LUN MAR", "LUN MAR"],
        ["LUN MAR MER", "LUN MAR MER"],
        ["LUN ET MAR", "LUN ET MAR"],
        ["LUN ET MAR ET MER", "LUN ET MAR ET MER"],
        ["LUN MAR ET MER", "LUN MAR ET MER"],
        ["LUN ET MAR MER", "LUN ET MAR MER"],
        ["1h-2h LUN MAR", "LUN MAR"],
        ["LUN A MER", undefined],
    ])("rpaRegex.daysOfWeekEnumeration.exec('%s')[0]", (value, expected) => {
        const result = rpaRegex.daysOfWeekEnumeration.exec(value)?.[0];
        rpaRegex.daysOfWeekEnumeration.lastIndex = 0
        expect(result).toBe(expected);
    });
});


    
describe( "times of week", () => {
    test.each([
        ["1h-2h", "1h-2h"],
        ["1h-2h LUN", "1h-2h LUN"],
        ["1h-2h 3h-4h LUN", "1h-2h 3h-4h LUN"],
        ["1h-2h LUN MAR", "1h-2h LUN MAR"],
        ["1h-2h 3h-4h LUN MAR", "1h-2h 3h-4h LUN MAR"],
        ["1h-2h LUN À MAR", "1h-2h LUN À MAR"],
        ["1h-2h LUN 3h-4h MAR", "1h-2h LUN"],
    ])("rpaRegex.weekTime.exec('%s')[0]", (value, expected) => {
        rpaRegex.weekTime.lastIndex = 0;
        const result = rpaRegex.weekTime.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["1h-2h LUN 3h-4h MAR", "3h-4h MAR"],
        ["1h-2h LUN, 3h-4h MAR", "3h-4h MAR"],
        ["1h-2h LUN, 3h-4h 5h-6h MAR", "3h-4h 5h-6h MAR"],
        ["1h-2h LUN", undefined],
    ])("rpaRegex.weekTime.exec('%s')[0] second call", (value, expected) => {
        rpaRegex.weekTime.lastIndex = 0;
        rpaRegex.weekTime.exec(value); // first call
        const result = rpaRegex.weekTime.exec(value)?.[0]; // second call
        expect(result).toBe(expected);
    });
});
    
describe("months", () => {
    test.each([
        ["janvier", true],
        ["jan", true],
        ["jan.", true],
        ["1 janvier", true],
        ["1janvier", true],
        ["jantest", false],
    ])("rpaRegex.months['01'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['01'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["février", true],
        ["fevrier", true],
        ["fév", true],
        ["fev", true],
        ["fév.", true],
        ["fev.", true],
        ["1 février", true],
        ["1février", true],
        ["févtest", false],
    ])("rpaRegex.months['02'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['02'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["mars", true],
        ["mar", true],
        ["mar.", true],
        ["mrs.", true],
        ["mr", true], // uncertain
        ["1 mars", true],
        ["1mars", true],
        ["marsl", true],
        ["martest", false],
        ["champ-de-mars", false],
    ])("rpaRegex.months['03'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['03'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["avril", true],
        ["avr", true],
        ["avr.", true],
        ["1 avril", true],
        ["1avril", true],
        ["avil", true],
        ["avrils", true],
        ["avrtest", false],
    ])("rpaRegex.months['04'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['04'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["mai", true],
        ["1 mai", true],
        ["1mai", true],
        ["maitest", false],
    ])("rpaRegex.months['05'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['05'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["juin", true],
        ["1 juin", true],
        ["1juin", true],
        ["juintest", false],
    ])("rpaRegex.months['06'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['06'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["juillet", true],
        ["juil", true],
        ["juil.", true],
        ["1 juillet", true],
        ["1juillet", true],
        ["juiltest", false],
    ])("rpaRegex.months['07'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['07'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["août", true],
        ["aout", true],
        ["1 août", true],
        ["1août", true],
        ["aoûttest", false],
    ])("rpaRegex.months['08'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['08'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["septembre", true],
        ["sept", true],
        ["sept.", true],
        ["1 septembre", true],
        ["1septembre", true],
        ["septest", false],
    ])("rpaRegex.months['09'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['09'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["octobre", true],
        ["oct", true],
        ["oct.", true],
        ["1 octobre", true],
        ["1octobre", true],
        ["octtest", false],
    ])("rpaRegex.months['10'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['10'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["novembre", true],
        ["nov", true],
        ["nov.", true],
        ["1 novembre", true],
        ["1novembre", true],
        ["novtest", false],
    ])("rpaRegex.months['11'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['11'].test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["décembre", true],
        ["decembre", true],
        ["déc", true],
        ["dec", true],
        ["déc.", true],
        ["dec.", true],
        ["1 décembre", true],
        ["1décembre", true],
        ["déctest", false],
    ])("rpaRegex.months['12'].test('%s')", (value, expected) => {
        const result = rpaRegex.months['12'].test(value);
        expect(result).toBe(expected);
    });
});

describe( "dates", () => {
    test.each([
        ["1 MARS", true],
        ["1ER MARS", true],
        ["1 MARSL", true],
        ["1 AVRILAU", true],
        ["1 DEC", true],
        ["9NOV", true],
        ["15NOV", true],
        ["AVRIL 01", false],
        ["MAI-JUIN", false],
    ])("rpaRegex.dayOfMonthDayFirst.test('%s')", (value, expected) => {
        rpaRegex.dayOfMonthDayFirst.lastIndex = 0;
        const result = rpaRegex.dayOfMonthDayFirst.test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["AVRIL 01", true],
        ["01 AVRIL AU 01 DEC", false],
        ["1 MARS", false],
    ])("rpaRegex.dayOfMonthDaySecond.test('%s')", (value, expected) => {
        rpaRegex.dayOfMonthDaySecond.lastIndex = 0;
        const result = rpaRegex.dayOfMonthDaySecond.test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["01/01", true],
        ["12/12", true],
        ["1/1", false],
        ["01/1", false],
        ["1/01", false],
    ])("rpaRegex.dayOfMonthSlashed.test('%s')", (value, expected) => {
        rpaRegex.dayOfMonthSlashed.lastIndex = 0;
        const result = rpaRegex.dayOfMonthSlashed.test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["1 MARS 1 DEC", true],
        ["1 MARS - 1 DEC", true],
        ["1 MARS A 1 DEC", true],
        ["1 MARS À 1 DEC", true],
        ["1 MARS AU 1 DEC", true],
        ["1 AVRIL ET 1 DEC", true], // this is in data
        ["MAI", false],
        ["1 MARS TEST 1 DEC", false],
        ["MAI-JUIN", false],
        ["MARS 01 A DEC 01", false],
        ["MARS 1 AU 1 DEC", false],
    ])("rpaRegex.daysOfMonthIntervalDayFirst.test('%s')", (value, expected) => {
        const result = rpaRegex.daysOfMonthIntervalDayFirst.test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["MARS 1 DEC 1", true],
        ["MARS 1 - DEC 1", true],
        ["MARS 1 A DEC 1", true],
        ["MARS 1 À DEC 1", true],
        ["MARS 1 AU DEC 1", true],
        ["MAI", false],
        ["MARS 1 TEST DEC 1", false],
        ["MAI-JUIN", false],
        ["1 MARS - 1 DEC", false],
        ["MARS 1 AU 1 DEC", false],
    ])("rpaRegex.daysOfMonthIntervalDaySecond.test('%s')", (value, expected) => {
        const result = rpaRegex.daysOfMonthIntervalDaySecond.test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["MAI JUIN", true],
        ["MAI-JUIN", true],
        ["MARS A DEC", true],
        ["MARS À DEC", true],
        ["MARS AU DEC", true],
        ["1 MARS-DEC 1", true], // wrong
        ["MAI", false],
        ["MAI TEST JUIN", false],
        ["1 MARS - 1 DEC", false],
        ["MARS 1 AU 1 DEC", false],
        ["MARS 1 AU DEC 1", false],
    ])("rpaRegex.daysOfMonthIntervalDayAbsent.test('%s')", (value, expected) => {
        const result = rpaRegex.daysOfMonthIntervalDayAbsent.test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["01/05 01/10", true],
        ["01/05-01/10", true],
        ["01/05 A 01/10", true],
        ["01/05 À 01/10", true],
        ["01/05 AU 01/10", true],
        ["MAI", false],
        ["01/05 TEST 01/10", false],
        ["1 MARS - 1 DEC", false],
    ])("rpaRegex.daysOfMonthIntervalSlashed.test('%s')", (value, expected) => {
        const result = rpaRegex.daysOfMonthIntervalSlashed.test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["MAI JUIN", true],
        ["MAI-JUIN", true],
        ["1 MARS - 1 DEC", true],
        ["MARS 1 - DEC 1", true],
        ["01/05-01/10", true],
        ["1 MARS-DEC 1", true], // wrong
        ["MAI", false],
        ["MARS 1 TEST 1 DEC", false],
        ["MARS 1 AU 1 DEC", false],
    ])("rpaRegex.daysOfMonthInterval.test('%s')", (value, expected) => {
        const result = rpaRegex.daysOfMonthInterval.test(value);
        expect(result).toBe(expected);
    });
});
