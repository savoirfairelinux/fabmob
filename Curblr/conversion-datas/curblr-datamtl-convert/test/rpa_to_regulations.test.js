const { getActivity, getEffectiveDates, getDaysOfWeek } = require("../rpa_to_regulations");

/*
    uncertain: behaviour that is not certainly right or wrong
    wrong: wrong behaviour that seems not worth fixing
*/

describe("getActivity", () => {
    test.each([
        ["\\P ", "no parking"],
        ["/P ", "no parking"],
        ["STAT. INT. ", "no parking"],
        ["INTERDICTION DE STAT. ", "no parking"],
        ["10h à 11h", "no parking"],
        ["\\A ", "no standing"],
        ["A ", "no standing"],
        [" \\A ", "no standing"],
        ["P ", "parking"],
        ["P PANONCEAU", "parking"],
        ["PANONCEAU ", null],
        ["PANNONCEAU", null],
        ["\\P", undefined],
        ["/P", undefined],
        ["STAT. INT.", undefined],
        [" STAT. INT. ", undefined], // uncertain
        ["INTERDICTION DE STAT.", undefined], // uncertain
        [" INTERDICTION DE STAT. ", undefined], // uncertain
        ["STAT", undefined],
        ["\\A", undefined],
        ["\\AA", undefined],
        ["\\a ", undefined],
        ["A", undefined],
        [" A", undefined],
        ["AA", undefined],
        ["P", undefined],
        [" P", undefined],
        [" PANNONCEAU", undefined], // uncertain
    ])("getActivity('%s')", (description, expected) => {
        const activity = getActivity(description);
        expect(activity).toBe(expected);
    });
});

describe("getEffectiveDates", () => {
    test.each([
        ["1 MARS AU 1 DEC", [{"from":"03-01","to":"12-01"}]],
        ["1ER MARS 1ER DEC", [{"from":"03-01","to":"12-01"}]],
        ["1ER MARS - 1ER DÉC", [{"from":"03-01","to":"12-01"}]],
        ["1ER MARS - 1ER  DÉC", [{"from":"03-01","to":"12-01"}]],
        ["1ER MARS AU 1ER DECEMBRE", [{"from":"03-01","to":"12-01"}]],
        ["1ER MARS AU 1ER DEC", [{"from":"03-01","to":"12-01"}]],
        ["MARS 01 A DEC. 01", [{"from":"03-01","to":"12-01"}]],
        ["1 MARSL AU 1 DEC", [{"from":"03-01","to":"12-01"}]],
        ["1MARS AU 1 DEC.", [{"from":"03-01","to":"12-01"}]],
        ["15 MRS - 15 NOV.", [{"from":"03-15","to":"11-15"}]],
        ["15 MARS AU 15 NOV", [{"from":"03-15","to":"11-15"}]],
        ["15 MARS À 15 NOV", [{"from":"03-15","to":"11-15"}]],
        ["15 MARS - 15 NOVEMBRE", [{"from":"03-15","to":"11-15"}]],
        ["15 MARS AU 15 NOVEMBRE", [{"from":"03-15","to":"11-15"}]],
        ["1 AVRIL AU 30 SEPT", [{"from":"04-01","to":"09-30"}]],
        ["1 AVRIL AU 15 OCT", [{"from":"05-01","to":"10-15"}]],
        ["1 AVRIL AU 31 OCT", [{"from":"05-01","to":"10-31"}]],
        ["1 AVRIL AU 1 NOVEMBRE", [{"from":"05-01","to":"11-01"}]],
        ["1 AVRIL AU 15 NOV", [{"from":"05-01","to":"11-15"}]],
        ["1 AVRIL AU 15 NOVEMBRE", [{"from":"05-01","to":"11-15"}]],
        ["1 AVRIL AU 30 NOV", [{"from":"04-01","to":"11-30"}]],
        ["1ER AVRIL - 30 NOV", [{"from":"04-01","to":"11-30"}]],
        ["1 AVRILAU 1 DEC", [{"from":"04-01","to":"12-01"}]],
        ["1 AVRIL AU 1 DEC", [{"from":"04-01","to":"12-01"}]],
        ["1 AVIL AU 1 DEC", [{"from":"04-01","to":"12-01"}]],
        ["1 AVRIL ET 1 DEC", [{"from":"04-01","to":"12-01"}]],
        ["1AVRIL AU 1 DEC", [{"from":"04-01","to":"12-01"}]],
        ["1AVRIL AU 1DEC", [{"from":"04-01","to":"12-01"}]],
        ["1ER AVRIL AU 1ER DEC", [{"from":"04-01","to":"12-01"}]],
        ["AVRIL 01 A DEC. 01", [{"from":"04-01","to":"12-01"}]],
        ["1 AVRILS AU 1 DEC", [{"from":"04-01","to":"12-01"}]],
        ["1 AVRIL  AU 1 DEC", [{"from":"04-01","to":"12-01"}]],
        ["15 AVRIL AU 15 OCTOBRE", [{"from":"04-15","to":"10-15"}]],
        ["15 AVRIL AU 1 NOV", [{"from":"05-15","to":"11-01"}]],
        ["15 AVRIL AU 1ER NOV.", [{"from":"04-15","to":"11-01"}]],
        ["15 AVRIL AU 1 NOVEMBRE", [{"from":"04-15","to":"11-01"}]],
        ["15 AVRIL AU 15 NOVEMBRE", [{"from":"04-15","to":"11-15"}]],
        ["15 AVR - 15 NOV", [{"from":"04-15","to":"11-15"}]],
        ["15 AVR AU 15 NOV", [{"from":"04-15","to":"11-15"}]],
        ["15 AVRIL AU 1ER DEC", [{"from":"05-15","to":"12-01"}]],
        ["MAI-JUIN", [{"from":"05-01","to":"06-01"}]],
        ["1MAI AU 1 SEPT", [{"from":"05-01","to":"09-01"}]],
        ["1MAI AU 1OCT", [{"from":"05-01","to":"10-01"}]],
        ["1 MAI AU 1 NOV", [{"from":"06-01","to":"11-01"}]],
        ["15 MAI AU 15 OCT", [{"from":"05-15","to":"10-15"}]],
        ["15 MAI AU 15 SEPT", [{"from":"05-15","to":"09-15"}]],
        ["1 JUIN AU 1 OCT", [{"from":"06-01","to":"10-01"}]],
        ["15 JUIN AU 1ER SEPT.", [{"from":"06-15","to":"09-01"}]],
        ["21 JUIN AU 1 SEPT", [{"from":"06-21","to":"09-01"}]],
        ["30 JUIN AU 30 AOUT", [{"from":"06-30","to":"08-30"}]],
        ["16 JUIL. AU 4 SEPT.", [{"from":"07-16","to":"09-04"}]],
        ["15 AOUT - 28 JUIN", [{"from":"08-15","to":"06-28"}]],
        ["20 AOÛT AU 30 JUIN", [{"from":"08-20","to":"06-30"}]],
        ["1 SEPT. AU 23 JUIN", [{"from":"09-01","to":"06-23"}]],
        ["SEPT A JUIN", [{"from":"09-01","to":"06-30"}]],
        ["SEPT À JUIN", [{"from":"09-01","to":"06-30"}]],
        ["SEPT. A JUIN", [{"from":"09-01","to":"06-30"}]],
        ["SEPT. À JUIN", [{"from":"09-01","to":"06-30"}]],
        ["1 SEPT. AU 30 JUIN", [{"from":"09-01","to":"06-30"}]],
        ["1 SEPT. AU 31 MAI", [{"from":"09-01","to":"05-31"}]],
        ["1ER SEPT AU 31 MAI", [{"from":"09-01","to":"05-31"}]],
        ["1 NOV. AU 31 MARS", [{"from":"11-01","to":"03-31"}]],
        ["1 NOV. AU 1 AVRIL", [{"from":"11-01","to":"04-01"}]],
        ["1 NOVEMBRE AU 15 AVRIL", [{"from":"11-01","to":"04-15"}]],
        ["1 NOV. AU 1 MAI", [{"from":"11-01","to":"05-01"}]],
        ["15 NOV. AU 15 MARS", [{"from":"11-15","to":"03-15"}]],
        ["15 NOV. AU 1 AVRIL", [{"from":"11-15","to":"04-01"}]],
        ["15 NOV - 15 AVR", [{"from":"11-15","to":"04-15"}]],
        ["15NOV - 15AVRIL", [{"from":"11-15","to":"04-15"}]],
        ["16 NOV. AU 14 MARS", [{"from":"11-16","to":"03-14"}]],
        ["30 NOV - 1ER AVRIL", [{"from":"11-30","to":"04-01"}]],
        ["1 DEC. AU 1 MARS", [{"from":"12-01","to":"03-01"}]],
        ["1ER DECEMBRE AU 1ER MARS", [{"from":"12-01","to":"03-01"}]],
        ["1 DEC. AU 1 AVRIL", [{"from":"12-01","to":"04-01"}]]
    ])("getEffectiveDates('%s')", (description, expected) => {
        const effectiveDates = getEffectiveDates(description);
        expect(effectiveDates).toStrictEqual(expected);
    });
});

describe("getDaysOfWeek", () => {
    test.each([
        ["LUNDI", {"days": ["mo"]}],
        ["LUN.", {"days": ["mo"]}],
        ["LUN", {"days": ["mo"]}],
        ["MARDI", {"days": ["tu"]}],
        ["MAR.", {"days": ["tu"]}],
        ["MAR", {"days": ["tu"]}],
        ["MERCREDI", {"days": ["we"]}],
        ["MER.", {"days": ["we"]}],
        ["MER", {"days": ["we"]}],
        ["JEUDI", {"days": ["th"]}],
        ["JEU.", {"days": ["th"]}],
        ["JEU", {"days": ["th"]}],
        ["VENDREDI", {"days": ["fr"]}],
        ["VEN.", {"days": ["fr"]}],
        ["VEN", {"days": ["fr"]}],
        ["VEMDREDI", {"days": ["fr"]}], // typo in data
        ["SAMEDI", {"days": ["sa"]}],
        ["SAM.", {"days": ["sa"]}],
        ["SAM", {"days": ["sa"]}],
        ["DIMANCHE", {"days": ["su"]}],
        ["DIM.", {"days": ["su"]}],
        ["DIM", {"days": ["su"]}],
        ["LUN VEN", {"days": ["mo", "fr"]}],
        ["LUN A VEN", {"days": ["mo","tu","we","th","fr"]}],
        ["LUN À VEN", {"days": ["mo","tu","we","th","fr"]}],
        ["LUN AU VEN", {"days": ["mo","tu","we","th","fr"]}],
        ["LUN ET VEN", {"days": ["mo", "fr"]}],
        ["VEN LUN", {"days": ["fr", "mo"]}],
        ["LUN VEN MAR", {"days": ["mo", "fr", "tu"]}],
        //["LUN VEN MAR MER", {"days": ["mo", "fr", "tu", "we"]}]
        // ["LUN B VEN", {"days": ["mo","tu","we","th","fr"]}],
        ["LUN ET LUN", {"days": ["mo", "mo"]}], // uncertain
        ["LUN AU VENA", {"days": ["mo","tu","we","th","fr"]}], // uncertain
        ["LUNA AU VENA", {"days": ["mo"]}], // wrong
        ["SAM A LUN", undefined], // uncertain
        ["1 DEC. AU 1 AVRIL", undefined],
        //["P 60 MIN 09H-18H LUN. MAR. MER. SAM. 09H-21H JEU. VEN.", undefined]
        // "\\P 08h-09h MER. 1 MARS AU 1 DEC."
    ])("getDaysOfWeek('%s')", (description, expected) => {
        const daysOfWeek = getDaysOfWeek(description);
        expect(daysOfWeek).toStrictEqual(expected);
    });
});
