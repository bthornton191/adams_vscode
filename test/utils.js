const { evaluate_exp } = require("../src/aview.ts.js");
const path = require("path");
const fs = require("fs");

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

/**
 * Parents
 * @param {path.ParsedPath} p
 * @param {int} n
 * @returns {path.ParsedPath}
 */
function get_parents(p, n) {
    let result = p;
    for (let i = 0; i < n; i++) {
        result = path.parse(result.dir);
    }
    return result;
}

/**
 * Get the latest installed version of Adams and the latest installed 2023 version of Adams
 * and return the two paths in a list.
 * @returns {path.ParsedPath[]}
 */
function getLatestAdamsVersions() {
    // Get the path to the adams installations
    const adams_path = path.format(get_parents(path.parse(process.env.ADAMS_LAUNCH_COMMAND), 2));

    // Get the list of all directories that match the pattern \d+_\d+(_\d+)?
    const adams_versions = fs.readdirSync(adams_path).filter((f) => f.match(/\d+_\d+(_\d+)?/));
    const latest = adams_versions.sort().reverse()[0];
    const latest_2023 = adams_versions
        .filter((v) => v.includes("2023"))
        .sort()
        .reverse()[0];

    if (process.platform === "win32") {
        return [
            path.join(adams_path, latest, "common", "mdi.bat"),
            path.join(adams_path, latest_2023, "common", "mdi.bat"),
        ];
    } else {
        return [path.join(adams_path, latest, "mdi"), path.join(adams_path, latest_2023, "mdi")];
    }
}

exports.waitForAdamsConnection = waitForAdamsConnection;
exports.get_parents = get_parents;
exports.getLatestAdamsVersions = getLatestAdamsVersions;
