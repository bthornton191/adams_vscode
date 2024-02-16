const { evaluate_exp } = require("../src/aview.ts.js");

function waitForAdamsConnection(done = () => {}) {
    evaluate_exp(
        "db_exists('.mdi')",
        (msg) => {
            if (msg.includes("ECONNREFUSED") || msg.includes("ECONNRESET")) {
                console.log("Connection refused. Retrying in 5 second...");
                setTimeout(waitForAdamsConnection, 5000, done);
            }
        },
        done
    );
}
exports.waitForAdamsConnection = waitForAdamsConnection;
