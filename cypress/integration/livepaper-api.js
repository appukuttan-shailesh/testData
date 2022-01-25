/// <reference types="cypress" />

describe("LivePaper public API test suite", () => {
    it("Query all published live papers", () => {
        cy.request(
            "GET",
            "https://validation-v2.brainsimulation.eu/livepapers-published/"
        ).then((response) => {
            // check response is 200
            expect(response.status).to.equal(200);

            // check response body is an array of more than 0 elements
            expect(response.body).to.be.a("array");
            cy.wrap(response.body).should("have.length.greaterThan", 0);

            cy.fixture("lp_keys_summary.json").then((lpKeys) => {
                // check each array element (lp object) has all required keys
                cy.wrap(response.body).each((item) => {
                    expect(item).to.have.all.keys(lpKeys);
                });

                // check if each array element key has valid values
                // and if UUID is in expected format
                cy.wrap(response.body).each((item) => {
                    lpKeys.forEach((key) => {
                        if (key === "id") {
                            expect(item["id"]).to.match(
                                /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
                            );
                        } else {
                            expect(item[key]).to.be.ok;
                        }
                    });
                });
            });
        });
    });

    it("Query a specific published live paper using UUID", () => {
        cy.request(
            "GET",
            "https://validation-v2.brainsimulation.eu/livepapers-published/c1573aeb-d139-42a2-a7fc-fd68319e428e"
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

    it("Query a specific published live paper using alias", () => {
        cy.request(
            "GET",
            "https://validation-v2.brainsimulation.eu/livepapers-published/2018-migliore-et-al"
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

    it.only("Query a non-existing live paper", () => {
        cy.request({
            method: "GET",
            url: "https://validation-v2.brainsimulation.eu/livepapers-published/abcde12345",
            failOnStatusCode: false,
        }).then((response) => {
            // check response is 404 (not found)
            expect(response.status).to.equal(404);
            // error message should state that requested live paper was not found
            expect(response.body.detail).to.have.string("not found");
        });
    });
});
