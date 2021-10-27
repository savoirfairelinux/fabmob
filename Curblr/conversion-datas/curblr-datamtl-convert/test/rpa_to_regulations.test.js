const fs = require('fs');

const { getActivity } = require("../rpa_to_regulations");

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
        [" STAT. INT. ", undefined],
        ["INTERDICTION DE STAT.", undefined],
        [" INTERDICTION DE STAT. ", undefined],
        ["STAT", undefined],
        ["\\A", undefined],
        ["\\AA", undefined],
        ["\\a ", undefined],
        ["A", undefined],
        [" A", undefined],
        ["AA", undefined],
        ["P", undefined],
        [" P", undefined],
        [" PANNONCEAU", undefined],
    ])("getActivity('%s')", (description, expected) => {
        const activity = getActivity(description);
        expect(activity).toBe(expected);
    });
});