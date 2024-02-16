const net = require("net");

const port = 5002;

function execute_cmd(cmd, log = () => {}, done = () => {}) {
    const client = new net.Socket();
    client.on("error", function (err) {
        log("Error running command '${ cmd }: '" + err.toString());
        done();
    });

    client.connect(port, "localhost", function () {
        // Send the command to the server
        client.write(`cmd ${cmd}`);

        // Receive the server's response
        client.on("data", function (data) {
            if (data.toString() != "cmd: 0") {
                log("Unexpected response from Adams View: " + data.toString());
            } else {
                log(`Command successful: '${cmd}'`);
            }

            // kill client after server's response
            client.destroy();
            done();
        });
    });
}

function evaluate_exp(exp, log = () => {}, done = (data) => {}) {
    const client = new net.Socket();
    client.on("error", function (err) {
        log(`Error evaluating expression '${exp}: '` + err.toString());
    });

    client.connect(port, "localhost", function () {
        // Send the command to the server
        client.write(`query ${exp}`);

        // Receive the server's response
        client.on("data", (desc_response) => {
            let [type_, num] = parseDescription(desc_response.toString());
            client.write("OK");
            client.on("data", (data_response) => {
                let data = parseData(data_response.toString(), type_, num);
                client.destroy();
                done(data);
            });
        });
    });
}

/**
 * Parse the description response from the server
 * @param {String} response - The response from the server
 * @returns {Array} - The type and number of the data
 */
function parseDescription(response) {
    let result = response.split(/[ :]+/);
    let type_ = result[1];
    let num = parseInt(result[2]);

    return [type_, num];
}

function parseData(response, type_, num) {
    function convertType(type_, val) {
        if (type_ === "str" && ["on", "off", "yes", "no"].includes(val.toLowerCase())) {
            // Handle boolean values
            val = val.toLowerCase() === "on" || val.toLowerCase() === "yes";
        } else if (type_ == "int") {
            // Handle integer values
            val = parseInt(val);
        } else if (type_ == "float") {
            // Handle float values
            val = parseFloat(val);
        } else if (type_ == "str") {
            // Handle string values
            val = val.trim();
        }

        return val;
    }

    if (parseInt(num) > 1) {
        var data = response.split(", ").map((val) => convertType(type_, val));
    } else {
        var data = convertType(type_, response);
    }
    return data;
}

exports.execute_cmd = execute_cmd;
exports.evaluate_exp = evaluate_exp;
exports.port = port;
