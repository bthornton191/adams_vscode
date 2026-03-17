const net = require("net");
const path = require("path");
const fs = require("fs");
const { spawn, exec } = require("child_process");
const { getPort, evaluate_exp, execute_cmd } = require("../src/aview.ts.js");
const cwd = path.join(__dirname, "working_directory");
const pidCwd = require("pid-cwd");
const process = require("process");

const log_file = path.join(cwd, "aview.log");

async function mochaGlobalSetup() {
    console.log("Start all tests.");
    await new Promise((resolve, reject) => {
        launchAdamsIfNotRunning(resolve);
    });
    console.log("Global setup complete.");
}

async function mochaGlobalTeardown() {
    console.log("All tests complete.");
    await new Promise((resolve, reject) => {
        killAdamsIfRunningInDir(cwd, resolve);
    });
    console.log("Global teardown complete.");
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
            line.toLowerCase().includes(proc_name.toLowerCase()),
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
            console.log("Command server is running. Restarting Adams View in working directory...");
        }
        startAdamsView(done);
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
    client.connect(getPort(), "localhost", function () {
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
        },
    );
}

/**
 * Start Adams View
 * @param {Function} done - Callback function to be called when Adams View is started
 * @param {number} port - Optional port number for the command server. If not specified, uses default (5002)
 * @param {string} dir - Optional directory to start Adams View in. If not specified, uses default working directory
 */
function startAdamsView(done, port = null, dir = null) {
    const workDir = dir || cwd;
    console.log(`Starting Adams View in ${workDir}${port ? ` on port ${port}` : ""}...`);

    // Create directory if it doesn't exist
    if (!fs.existsSync(workDir)) {
        fs.mkdirSync(workDir, { recursive: true });
    }

    killAdamsIfRunningInDir(workDir, () => {
        console.log("Running aview start command...");
        fs.writeFileSync(
            path.join(workDir, "aviewBS.cmd"),
            'var set var=.mdi.tmp_int int=(eval(run_python_code("import threading")))',
        );
        fs.writeFileSync(path.join(workDir, "aview.cmd"), "command_server start");
        fs.writeFileSync(path.join(workDir, "aviewAS.cmd"), "");

        const spawnOptions = {
            cwd: workDir,
            shell: true,
        };

        // Only set ADAMS_LISTENER_PORT environment variable if port is specified
        if (port) {
            spawnOptions.env = {
                ...process.env,
                ADAMS_LISTENER_PORT: port.toString(),
            };
        }

        spawn(`"${process.env._ADAMS_LAUNCH_COMMAND}"`, ["aview", "ru-s", "i"], spawnOptions);

        // Wait for Adams View to start using polling instead of blocking
        console.log("Waiting for Adams View to start...");
        pollForAdamsViewStart(0, done, 60, 500, workDir);
    });
}

/**
 * Poll for Adams View to start by checking the log file
 * @param {number} attempts - The number of attempts so far
 * @param {Function} done - Callback function to be called when Adams View is started
 * @param {number} maxAttempts - Maximum number of attempts before giving up
 * @param {number} interval - Interval in milliseconds between attempts
 * @param {string} dir - Optional directory where Adams View is running. If not specified, uses default working directory
 */
function pollForAdamsViewStart(attempts, done, maxAttempts = 60, interval = 500, dir = null) {
    const workDir = dir || cwd;
    const logFile = path.join(workDir, "aview.log");

    if (attempts >= maxAttempts) {
        console.error(
            `Adams View failed to start after ${(maxAttempts * interval) / 1000} seconds`,
        );
        done();
        return;
    }

    // Check if the log file exists and contains the expected content
    try {
        if (
            fs.existsSync(logFile) &&
            fs.readFileSync(logFile, "utf8").includes("command_server start")
        ) {
            console.log("Adams View Started!");
            done();
            return;
        }
    } catch (error) {
        console.log(`Error checking log file: ${error.message}`);
    }

    // Schedule the next check
    setTimeout(
        () => pollForAdamsViewStart(attempts + 1, done, maxAttempts, interval, dir),
        interval,
    );
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

        if (dir === null) {
            var logFile = log_file;
        } else {
            var logFile = path.join(dir, "aview.log");
        }

        // Delete the log file if it exists
        console.log("Deleting log file...");
        if (fs.existsSync(logFile)) {
            function deleteLogFile() {
                if (fs.existsSync(logFile)) {
                    try {
                        fs.unlinkSync(logFile);
                        console.log("Log file deleted successfully.");
                    } catch (error) {
                        console.log("Log file is locked. Retrying in 1 second...");
                        setTimeout(deleteLogFile, 1000);
                    }
                }
            }
            deleteLogFile();
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
            line.toLowerCase().includes(proc_name.toLowerCase()),
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
exports.mochaGlobalTeardown = mochaGlobalTeardown;
exports.startAdamsView = startAdamsView;
exports.killAdamsIfRunningInDir = killAdamsIfRunningInDir;
