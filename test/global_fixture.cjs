const net = require("net");
const path = require("path");
const fs = require("fs");
const { spawn, exec } = require("child_process");
const { port, evaluate_exp, execute_cmd } = require("../src/aview.ts.js");
const cwd = path.join(__dirname, "working_directory");
const pidCwd = require("pid-cwd");

const log_file = path.join(cwd, "aview.log");

const adamsLaunchCommand = process.env.ADAMS_LAUNCH_COMMAND;
var proc;

async function mochaGlobalSetup() {
    console.log("Start all tests.");
    await new Promise((resolve, reject) => {
        launchAdamsIfNotRunning(resolve);
    });
    console.log("Global setup complete.");
}

/**
 * Kill all processes with a given name
 * @param {String} proc_name - The name of the process to kill
 * @param {Function} done - Callback function to be called when all processes have been killed
 */
function killAllProcsOfName(proc_name, done = () => {}) {
    exec("tasklist", (err, stdout, stderr) => {
        let lines = stdout.split("\n");
        let matchingLines = lines.filter((line) =>
            line.toLowerCase().includes(proc_name.toLowerCase())
        );

        if (matchingLines.length === 0) {
            console.log("No processes found with the name: " + proc_name);
        } else {
            matchingLines.forEach((line) => {
                let pid = line.split(proc_name)[1].trim().split(" ")[0];
                killProcByPid(pid);
            });
        }
    });
}

/**
 * Kill a process by its PID
 * @param {int} pid - The PID of the process to kill
 */
function killProcByPid(pid) {
    try {
        process.kill(pid, "SIGTERM");
        console.log("Killed process with PID: " + pid);
    } catch (err) {
        console.log("Failed to kill process with PID: " + pid);
    }
}

function launchAdamsIfNotRunning(done = () => {}) {
    checkIfCommandServerRunning((running) => {
        if (running) {
            console.log("Command server is running");
            // getCwdOfRunningCommandServer((cwd_) => {
            //     if (path.resolve(cwd_) == path.resolve(cwd)) {
            //         console.log("Command server is running in the correct directory");
            //         done();
            //     } else {
            //         console.log("Command server is running in the wrong directory");
            //         console.log("Killing the adams view process running the command server...");
            //         execute_cmd(
            //             "stop",
            //             () => {},
            //             () => {}
            //         );
            //         startAdamsView(done);
            //     }
            // });
            console.log("Killing all Adams View processes...");
            killAllProcsOfName("aview.exe", () => {
                startAdamsView(done);
            });
        } else {
            startAdamsView(done);
        }
    });
}

/**
 * Check if the command server is running
 * @param {Function} done - Callback function that takes a boolean as an argument
 * @returns {Boolean} - True if the command server is running, false otherwise
 */
function checkIfCommandServerRunning(done = (running) => {}) {
    const client = new net.Socket();
    client.on("error", function (err) {
        done(false);
    });
    client.connect(port, "localhost", function () {
        done(true);
    });
}

/**
 * Get the current working directory of the command server
 * @param {Function} done - Callback function that takes the current working directory as an argument
 * @returns {String} - The current working directory of the command server
 */
function getCwdOfRunningCommandServer(done = (cwd) => {}) {
    evaluate_exp(
        "getcwd()",
        () => {},
        (result) => {
            done(path.resolve(result));
        }
    );
}

/**
 * Start Adams View
 * @param {Function} done - Callback function to be called when Adams View is started
 */
function startAdamsView(done) {
    console.log("Starting Adams View...");
    killAdamsIfRunningInDir(cwd, () => {
        // Delete the log file if it exists
        console.log("Deleting log file...");
        if (fs.existsSync(log_file)) {
            function deleteLogFile() {
                if (fs.existsSync(log_file)) {
                    try {
                        fs.unlinkSync(log_file);
                        console.log("Log file deleted successfully.");
                    } catch (error) {
                        console.log("Log file is locked. Retrying in 1 second...");
                        setTimeout(deleteLogFile, 1000);
                    }
                }
            }
            deleteLogFile();
        }

        console.log("Running aview start command...");
        fs.writeFileSync(path.join(cwd, "aview.cmd"), "command_server start");
        proc = spawn(`${adamsLaunchCommand}`, ["aview", "ru-s", "i"], { cwd: cwd });

        // Wait for Adams View to start
        console.log("Waiting for Adams View to start...");
        while (
            !fs.existsSync(log_file) ||
            fs.readFileSync(log_file, "utf8").includes("command_server start") == false
        ) {}
        console.log("Adams View Started!");
        done();
    });
}

/**
 * Kill Adams View if it is running in the current working directory
 * @param {str} dir - The directory to check
 * @param {Function} done - Callback function to be called when Adams View is killed
 */
function killAdamsIfRunningInDir(dir, done = () => {}) {
    checkIfAdamsRunningInDir(dir, (pid) => {
        if (pid !== 0) {
            console.log(`There is already a running Adams View process in ${dir}. Killing it...`);
            killProcByPid(pid);
        }
        done();
    });
}

/**
 * Check if Adams View is running in the current working directory
 * @param {String} dir - The directory to check
 * @param {Function} done - Callback function that takes the PID of the running Adams View process as an argument
 */
function checkIfAdamsRunningInDir(dir, done = (pid) => {}) {
    console.log(`Checking if Adams View is running in ${dir}`);
    const proc_name = "aview.exe";
    exec("tasklist", (err, stdout, stderr) => {
        let lines = stdout.split("\n");
        let matchingLines = lines.filter((line) =>
            line.toLowerCase().includes(proc_name.toLowerCase())
        );
        if (matchingLines.length === 0) {
            done(0);
        } else {
            matchingLines.forEach((line) => {
                let pid = parseInt(line.split(proc_name)[1].trim().split(" ")[0]);
                console.log(`- Checking PID: ${pid}...`);
                pidCwd(pid).then((cwd_) => {
                    if (path.resolve(cwd_) == path.resolve(dir)) {
                        console.log(`- Found Adams View process in ${dir} with PID: ${pid}`);
                        done(pid);
                    } else if (matchingLines.indexOf(line) === matchingLines.length - 1) {
                        console.log(`- No Adams View process found in ${dir}`);
                        done(0);
                    }
                });
            });
        }
    });
}

exports.mochaGlobalSetup = mochaGlobalSetup;
mochaGlobalSetup();
