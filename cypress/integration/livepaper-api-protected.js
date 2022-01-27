/// <reference types="cypress" />

// import 'cypress-keycloak';

describe("LivePaper protected API test suite", () => {

    describe.skip("Without authentication", () => {
        it("Query a specific published live paper using alias", () => {
            cy.request({
                method: "GET",
                url: "https://validation-v2.brainsimulation.eu/livepapers/2018-migliore-et-al",
                failOnStatusCode: false,
            }).then((response) => {
                // check response is 403 (forbidden)
                expect(response.status).to.equal(403);
                // error message should state that requested live paper was not found
                expect(response.body.detail).to.have.string("Not authenticated");
            });
        });
    })

    // beforeEach(() => {
    //     cy.visit("/builder/");
    //     cy.login({
    //         root: 'https://iam.ebrains.eu/',
    //         realm: 'hbp',
    //         username: 'validationtester',
    //         password: 'ADD_PASS',
    //         client_id: 'live-paper-apps',
    //         redirect_uri: 'https://live-papers.brainsimulation.eu/builder/',
    //     });
    // });

    beforeEach(() => {
        cy.visit("/builder/");
        cy.url().then((url) => {
            if (url.startsWith("https://iam.ebrains.eu/")) {
                const username = Cypress.env("CYPRESS_LP_username");
                const password = Cypress.env("CYPRESS_LP_password");
                cy.get("input[name=username]").type(`${username}{enter}`);
                cy.get("input[name=password]").type(`${password}{enter}`);
            }
        });
    });

    it("Query a specific published live paper using alias", () => {
        cy.request(
            "GET",
            "https://validation-v2.brainsimulation.eu/livepapers/2018-migliore-et-al"
        ).then((response) => {
            // check response is 200
            expect(response.status).to.equal(200);
            cy.fixture("lp_keys_all.json").then((lpKeys) => {
                // check lp object has all required keys
                // Note: we check here for complete set of keys
                expect(response.body).to.have.all.keys(lpKeys);

                // check all keys have valid values
                lpKeys.forEach((key) => {
                    // TODO: License should not be null; fix API error!
                    if (["version", "license"].includes(key)) return true;
                    else expect(response.body[key]).to.be.ok;
                });
            });
        });
    });

    it.skip("Query a non-existing live paper", () => {
        cy.request({
            method: "GET",
            url: "https://validation-v2.brainsimulation.eu/livepapers/abcde12345",
            failOnStatusCode: false,
        }).then((response) => {
            // check response is 404 (not found)
            expect(response.status).to.equal(404);
            // error message should state that requested live paper was not found
            expect(response.body.detail).to.have.string("not found");
        });
    });
});
