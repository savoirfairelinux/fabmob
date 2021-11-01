const rpaRegex = require("../rpa_regexes");

describe("regexes", () => {
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
        expect(result).toBe(expected);
    });

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
    ])("days.test('%s')", (value, expected) => {
        const result = rpaRegex.anyDay.test(value);
        expect(result).toBe(expected);
    });

    test.each([
        ["LUN À VEN", true],
        ["LUN A VEN", true],
        ["LUN AU VEN", true],
        ["LUN VEN", false],
        ["1h À 2h", false]
    ])("daysInterval.test('%s')", (value, expected) => {
        const result = rpaRegex.daysInterval.test(value);
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

    test.each([
        ["LUN MAR", "LUN MAR"],
        ["LUN MAR MER", "LUN MAR MER"],
        ["LUN ET MAR", "LUN ET MAR"],
        ["LUN ET MAR ET MER", "LUN ET MAR ET MER"],
        ["LUN MAR ET MER", "LUN MAR ET MER"],
        ["LUN ET MAR MER", "LUN ET MAR MER"],
    ])("rpaRegex.daysEnumeration.exec('%s')[0]", (value, expected) => {
        const result = rpaRegex.daysEnumeration.exec(value)[0];
        expect(result).toBe(expected);
    });
})
