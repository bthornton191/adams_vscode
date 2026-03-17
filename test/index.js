const path = require("path");
const Mocha = require("mocha");
const { glob } = require("glob");
const { mochaGlobalSetup, mochaGlobalTeardown } = require("./global_fixture.cjs");

async function run() {
    await mochaGlobalSetup();

    const mocha = new Mocha({
        timeout: 300000,
        fullTrace: true,
    });

    const testsRoot = __dirname;
    const files = await glob("**/*.test.js", { cwd: testsRoot });
    files.forEach((f) => mocha.addFile(path.resolve(testsRoot, f)));

    return new Promise((resolve, reject) => {
        mocha.run(async (failures) => {
            await mochaGlobalTeardown();
            if (failures > 0) {
                reject(new Error(`${failures} test(s) failed.`));
            } else {
                resolve();
            }
        });
    });
}

exports.run = run;
