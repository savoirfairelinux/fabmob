const rpaRegex = require("../rpa_regexes");

describe("times", () => {
    test.each([
        ["1h", "1h"],
        ["1h5", "1h5"],
        ["1h30", "1h30"],
        ["10h", "10h"],
        ["10h5", "10h5"],
        ["10h30", "10h30"],
        ["lundi1h", "1h"],
        ["1hlundi", "1h"],
        ["10", undefined],
        ["1ah", undefined],
        ["h30", undefined],
    ])("time.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.time.lastIndex = 0;
        const result = rpaRegex.time.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["1h-2h", "1h-2h"],
        ["1h - 2h", "1h - 2h"],
        ["1hà2h", "1hà2h"],
        ["1h à 2h", "1h à 2h"],
        ["1hÀ2h", "1hÀ2h"],
        ["1h À 2h", "1h À 2h"],
        ["1ha2h", "1ha2h"],
        ["1h a 2h", "1h a 2h"],
        ["1hA2h", "1hA2h"],
        ["1h A 2h", "1h A 2h"],
        ["1h @ 2h", "1h @ 2h"],
        ["1h@2h", "1h@2h"],
        ["1h    -  2h", "1h    -  2h"],
        ["1h", undefined],
        ["1h 2h", undefined],
        ["1hb2h", undefined],
        ["1h b 2h", undefined],
        ["1hàa2h", undefined],
        ["lundi à vendredi", undefined],
    ])("timeInterval.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.timeInterval.lastIndex = 0;
        const result = rpaRegex.timeInterval.exec(value)?.[0];
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
        ["06h30-09h30, 15h30-18h30", "06h30-09h30, 15h30-18h30"],
    ])("rpaRegex.timesSequence.exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.timesSequence.exec(value)[0];
        expect(result).toBe(expected);
    });
});

describe("days", () => {
    test.each([
        ["LUN", "LUN"],
        ["LUN.", "LUN."],
        ["LUNDI", "LUNDI"],
        ["MAR", "MAR"],
        ["MAR.", "MAR."],
        ["MARDI", "MARDI"],
        ["MER", "MER"],
        ["MER.", "MER."],
        ["MERCREDI", "MERCREDI"],
        ["JEU", "JEU"],
        ["JEU.", "JEU."],
        ["JEUDI", "JEUDI"],
        ["VEN", "VEN"],
        ["VEN.", "VEN."],
        ["VEMDREDI", "VEMDREDI"],
        ["VENDREDI", "VENDREDI"],
        ["SAM", "SAM"],
        ["SAM.", "SAM."],
        ["SAMEDI", "SAMEDI"],
        ["DIM", "DIM"],
        ["DIM.", "DIM."],
        ["DIMANCHE", "DIMANCHE"],
        ["12h LUN 1 MARS", "LUN"],
        ["MONDAY", undefined ],
        ["MARS", undefined ],
    ])("anyDayOfWeek.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.anyDayOfWeek.lastIndex = 0;
        const result = rpaRegex.anyDayOfWeek.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["LUN À VEN", "LUN À VEN"],
        ["LUN A VEN", "LUN A VEN"],
        ["LUN AU VEN", "LUN AU VEN"],
        ["LUN. AU VEN.", "LUN. AU VEN."],
        ["LUN.AU VEN.", "LUN.AU VEN."],
        ["LUN VEN", undefined ],
        ["1h À 2h", undefined ],
    ])("daysOfWeekInterval.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.daysOfWeekInterval.lastIndex = 0;
        const result = rpaRegex.daysOfWeekInterval.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["LUN MAR", "LUN MAR"],
        ["LUN MAR MER", "LUN MAR MER"],
        ["LUN ET MAR", "LUN ET MAR"],
        ["LUN ET MAR ET MER", "LUN ET MAR ET MER"],
        ["LUN MAR ET MER", "LUN MAR ET MER"],
        ["LUN ET MAR MER", "LUN ET MAR MER"],
        ["LUN.ET VEN.", "LUN.ET VEN."],
        ["1h-2h LUN MAR", "LUN MAR"],
        ["LUN A MER", undefined],
    ])("rpaRegex.daysOfWeekEnumeration.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.daysOfWeekEnumeration.lastIndex = 0;
        const result = rpaRegex.daysOfWeekEnumeration.exec(value)?.[0];
        expect(result).toBe(expected);
    });
});


    
describe( "times of week", () => {
    test.each([
        ["LUN 1h-2h", "LUN 1h-2h"],
        ["LUN 1h-2h 3h-4h", "LUN 1h-2h 3h-4h"],
        ["LUN MAR 1h-2h", "LUN MAR 1h-2h"],
        ["LUN. MAR. 1h-2h", "LUN. MAR. 1h-2h"],
        ["LUN MAR 1h-2h 3h-4h", "LUN MAR 1h-2h 3h-4h"],
        ["LUN À MAR 1h-2h", "LUN À MAR 1h-2h"],
        ["LUN 1h-2h MAR 3h-4h ", "LUN 1h-2h"],
        ["MARDI - 8H à 16H30", "MARDI - 8H à 16H30"],
        ["LUN MER VEN 8H À 12H - MAR JEU 13H À 17H", "LUN MER VEN 8H À 12H"],
        ["1h-2h", undefined],
        ["LUN", undefined],
        ["1h-2h LUN", undefined],
        ["MER 17H À JEU 17H", undefined],
    ])("rpaRegex.weekTimeDaysFirst.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.weekTimeDaysFirst.lastIndex = 0;
        const result = rpaRegex.weekTimeDaysFirst.exec(value)?.[0];
        expect(result).toBe(expected);
    });


    test.each([
        ["1h-2h LUN", "1h-2h LUN"],
        ["1h-2h 3h-4h LUN", "1h-2h 3h-4h LUN"],
        ["1h-2h LUN MAR", "1h-2h LUN MAR"],
        ["1h-2h LUN. MAR.", "1h-2h LUN. MAR."],
        ["1h-2h 3h-4h LUN MAR", "1h-2h 3h-4h LUN MAR"],
        ["1h-2h LUN À MAR", "1h-2h LUN À MAR"],
        ["1h-2h LUN 3h-4h MAR", "1h-2h LUN"],
        ["8H à 16H30 - MARDI", "8H à 16H30 - MARDI"],
        ["1h-2h", undefined],
        ["LUN", undefined],
        ["LUN 1h-2h", undefined],
        ["MER 17H À JEU 17H", undefined],
    ])("rpaRegex.weekTimeDaysSecond.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.weekTimeDaysSecond.lastIndex = 0;
        const result = rpaRegex.weekTimeDaysSecond.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["1h-2h LUN 3h-4h MAR", "3h-4h MAR"],
        ["1h-2h LUN, 3h-4h MAR", "3h-4h MAR"],
        ["1h-2h LUN, 3h-4h MAR. MER.", "3h-4h MAR. MER."],
        ["1h-2h LUN, 3h-4h 5h-6h MAR", "3h-4h 5h-6h MAR"],
        ["1h-2h LUN", undefined],
    ])("rpaRegex.weekTimeDaysSecond.exec('%s')?.[0] second call", (value, expected) => {
        rpaRegex.weekTimeDaysSecond.lastIndex = 0;
        rpaRegex.weekTimeDaysSecond.exec(value); // first call
        const result = rpaRegex.weekTimeDaysSecond.exec(value)?.[0]; // second call
        expect(result).toBe(expected);
    });

    test.each([
        ["1h-2h", "1h-2h"],
        ["1h-2h 3h-4h", "1h-2h 3h-4h"],
        ["LUN", undefined],
        ["LUN 1h-2h", undefined],
        ["1h-2h LUN", undefined],
        ["MER 17H À JEU 17H", undefined],
    ])("rpaRegex.weekTimeDaysAbsent.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.weekTimeDaysAbsent.lastIndex = 0;
        const result = rpaRegex.weekTimeDaysAbsent.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["LUN", "LUN"],
        ["LUN MAR", "LUN MAR"],
        ["1h-2h", undefined],
        ["LUN 1h-2h", undefined],
        ["1h-2h LUN", undefined],
        ["MER 17H À JEU 17H", undefined],
    ])("rpaRegex.weekTimeDaysOnly.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.weekTimeDaysOnly.lastIndex = 0;
        const result = rpaRegex.weekTimeDaysOnly.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["MER 17H À JEU 17H", "MER 17H À JEU 17H"],
        ["1h-2h", undefined],
        ["1h-2h LUN", undefined],
        ["1h-2h 3h-4h LUN", undefined],
        ["1h-2h LUN MAR", undefined],
        ["LUN 1h-2h", undefined],
    ])("rpaRegex.weekTimeDaysOverlap.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.weekTimeDaysOverlap.lastIndex = 0;
        const result = rpaRegex.weekTimeDaysOverlap.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["1h-2h", "1h-2h"],
        ["1h-2h LUN", "1h-2h LUN"],
        ["1h-2h 3h-4h LUN", "1h-2h 3h-4h LUN"],
        ["1h-2h LUN MAR", "1h-2h LUN MAR"],
        ["1h-2h LUN. MAR.", "1h-2h LUN. MAR."],
        ["1h-2h 3h-4h LUN MAR", "1h-2h 3h-4h LUN MAR"],
        ["1h-2h LUN À MAR", "1h-2h LUN À MAR"],
        ["1h-2h LUN 3h-4h MAR", "1h-2h LUN"],
        ["8H à 16H30 - MARDI", "8H à 16H30 - MARDI"],
        ["LUN 1h-2h", "LUN 1h-2h"],
        ["MER 17H À JEU 17H", "MER 17H À JEU 17H"],
    ])("rpaRegex.weekTime.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.weekTime.lastIndex = 0;
        const result = rpaRegex.weekTime.exec(value)?.[0];
        expect(result).toBe(expected);
    });
});
    
describe("months", () => {
    test.each([
        ["janvier", "janvier"],
        ["jan", "jan"],
        ["jan.", "jan."],
        ["1 janvier", "janvier"],
        ["1janvier", "janvier"],
        ["jantest", undefined ],
    ])("rpaRegex.months['01'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['01'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["février", "février"],
        ["fevrier", "fevrier"],
        ["fév", "fév"],
        ["fev", "fev"],
        ["fév.", "fév."],
        ["fev.", "fev."],
        ["1 février", "février"],
        ["1février", "février"],
        ["févtest", undefined ],
    ])("rpaRegex.months['02'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['02'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["mars", "mars"],
        ["mar", "mar"],
        ["mar.", "mar."],
        ["mrs.", "mrs"],
        ["mr", "mr"],
        ["1 mars", "mars"],
        ["1mars", "mars"],
        ["marsl", "marsl"],
        ["martest", undefined ],
        ["champ-de-mars", undefined ],
    ])("rpaRegex.months['03'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['03'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["avril", "avril"],
        ["avr", "avr"],
        ["avr.", "avr."],
        ["1 avril", "avril"],
        ["1avril", "avril"],
        ["avil", "avil"],
        ["avrils", "avrils"],
        ["avrtest", undefined ],
    ])("rpaRegex.months['04'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['04'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["mai", "mai"],
        ["1 mai", "mai"],
        ["1mai", "mai"],
        ["maitest", undefined],
    ])("rpaRegex.months['05'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['05'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["juin", "juin"],
        ["1 juin", "juin"],
        ["1juin", "juin"],
        ["juintest", undefined],
    ])("rpaRegex.months['06'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['06'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["juillet", "juillet"],
        ["juil", "juil"],
        ["juil.", "juil."],
        ["1 juillet", "juillet"],
        ["1juillet", "juillet"],
        ["juiltest", undefined ],
    ])("rpaRegex.months['07'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['07'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["août", "août"],
        ["aout", "aout"],
        ["1 août", "août"],
        ["1août", "août"],
        ["aoûttest", undefined ],
    ])("rpaRegex.months['08'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['08'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["septembre", "septembre"],
        ["sept", "sept"],
        ["sept.", "sept."],
        ["1 septembre", "septembre"],
        ["1septembre", "septembre"],
        ["septest", undefined ],
    ])("rpaRegex.months['09'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['09'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["octobre", "octobre"],
        ["oct", "oct"],
        ["oct.", "oct."],
        ["1 octobre", "octobre"],
        ["1octobre", "octobre"],
        ["octtest", undefined ],
    ])("rpaRegex.months['10'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['10'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["novembre", "novembre"],
        ["nov", "nov"],
        ["nov.", "nov."],
        ["1 novembre", "novembre"],
        ["1novembre", "novembre"],
        ["novtest", undefined ],
    ])("rpaRegex.months['11'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['11'].exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["décembre", "décembre"],
        ["decembre", "decembre"],
        ["déc", "déc"],
        ["dec", "dec"],
        ["déc.", "déc."],
        ["dec.", "dec."],
        ["1 décembre", "décembre"],
        ["1décembre", "décembre"],
        ["déctest", undefined ],
    ])("rpaRegex.months['12'].exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.months['12'].exec(value)?.[0];
        expect(result).toBe(expected);
    });
});

describe( "dates", () => {
    test.each([
        ["1 MARS", "1 MARS"],
        ["1ER MARS", "1ER MARS"],
        ["1 MARSL", "1 MARSL"],
        ["1 AVRILAU", "1 AVRIL"],
        ["1 DEC", "1 DEC"],
        ["9NOV", "9NOV"],
        ["15NOV", "15NOV"],
        ["AVRIL 01", undefined],
        ["MAI-JUIN", undefined],
    ])("rpaRegex.dayOfMonthDayFirst.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.dayOfMonthDayFirst.lastIndex = 0;
        const result = rpaRegex.dayOfMonthDayFirst.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["AVRIL 01", "AVRIL 01"],
        ["01 AVRIL AU 01 DEC", undefined],
        ["1 MARS", undefined],
    ])("rpaRegex.dayOfMonthDaySecond.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.dayOfMonthDaySecond.lastIndex = 0;
        const result = rpaRegex.dayOfMonthDaySecond.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["01/01", "01/01"],
        ["12/12", "12/12"],
        ["1/1", undefined],
        ["01/1", undefined],
        ["1/01", undefined],
    ])("rpaRegex.dayOfMonthSlashed.exec('%s')?.[0]", (value, expected) => {
        rpaRegex.dayOfMonthSlashed.lastIndex = 0;
        const result = rpaRegex.dayOfMonthSlashed.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["1 MARS 1 DEC", "1 MARS 1 DEC"],
        ["1 MARS - 1 DEC", "1 MARS - 1 DEC"],
        ["1 MARS A 1 DEC", "1 MARS A 1 DEC"],
        ["1 MARS À 1 DEC", "1 MARS À 1 DEC"],
        ["1 MARS AU 1 DEC", "1 MARS AU 1 DEC"],
        ["1 AVRIL ET 1 DEC", "1 AVRIL ET 1 DEC"], // this is in data
        ["MAI", undefined],
        ["1 MARS TEST 1 DEC", undefined],
        ["MAI-JUIN", undefined],
        ["MARS 01 A DEC 01", undefined],
        ["MARS 1 AU 1 DEC", undefined],
    ])("rpaRegex.daysOfMonthIntervalDayFirst.exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.daysOfMonthIntervalDayFirst.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["MARS 1 DEC 1", "MARS 1 DEC 1"],
        ["MARS 1 - DEC 1", "MARS 1 - DEC 1"],
        ["MARS 1 A DEC 1", "MARS 1 A DEC 1"],
        ["MARS 1 À DEC 1", "MARS 1 À DEC 1"],
        ["MARS 1 AU DEC 1", "MARS 1 AU DEC 1"],
        ["MAI", undefined],
        ["MARS 1 TEST DEC 1", undefined],
        ["MAI-JUIN", undefined],
        ["1 MARS - 1 DEC", undefined],
        ["MARS 1 AU 1 DEC", undefined],
    ])("rpaRegex.daysOfMonthIntervalDaySecond.exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.daysOfMonthIntervalDaySecond.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["MAI JUIN", "MAI JUIN"],
        ["MAI-JUIN", "MAI-JUIN"],
        ["MARS A DEC", "MARS A DEC"],
        ["MARS À DEC", "MARS À DEC"],
        ["MARS AU DEC", "MARS AU DEC"],
        ["1 MARS-DEC 1", "MARS-DEC"], // wrong
        ["MAI", undefined],
        ["MAI TEST JUIN", undefined],
        ["1 MARS - 1 DEC", undefined],
        ["MARS 1 AU 1 DEC", undefined],
        ["MARS 1 AU DEC 1", undefined],
    ])("rpaRegex.daysOfMonthIntervalDayAbsent.exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.daysOfMonthIntervalDayAbsent.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["01/05 01/10", "01/05 01/10"],
        ["01/05-01/10", "01/05-01/10"],
        ["01/05 A 01/10", "01/05 A 01/10"],
        ["01/05 À 01/10", "01/05 À 01/10"],
        ["01/05 AU 01/10", "01/05 AU 01/10"],
        ["MAI", undefined],
        ["01/05 TEST 01/10", undefined],
        ["1 MARS - 1 DEC", undefined]      
    ])("rpaRegex.daysOfMonthIntervalSlashed.exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.daysOfMonthIntervalSlashed.exec(value)?.[0];
        expect(result).toBe(expected);
    });

    test.each([
        ["MAI JUIN", "MAI JUIN"],
        ["MAI-JUIN", "MAI-JUIN"],
        ["1 MARS - 1 DEC", "1 MARS - 1 DEC"],
        ["MARS 1 - DEC 1", "MARS 1 - DEC 1"],
        ["01/05-01/10", "01/05-01/10"],
        ["1 MARS-DEC 1", "MARS-DEC"], // wrong
        ["MAI", undefined],
        ["MARS 1 TEST 1 DEC", undefined],
        ["MARS 1 AU 1 DEC", undefined],
    ])("rpaRegex.daysOfMonthInterval.exec('%s')?.[0]", (value, expected) => {
        const result = rpaRegex.daysOfMonthInterval.exec(value)?.[0];
        expect(result).toBe(expected);
    });
});
