const path = require('path');
const fs = require('fs');
const { spawn, exec, } = require('child_process');

var proc;
const cwd = path.join(__dirname, 'working_directory');
async function mochaGlobalSetup() {
    
    // TODO: FIgure out why this isn't running
    console.log('Start all tests.');

    const adamsLaunchCommand = process.env.ADAMS_LAUNCH_COMMAND;
    
    fs.writeFileSync(path.join(cwd, 'aview.cmd'), 'command_server start');
    
    // var isDone = false;
    // killProcess('aview.exe', () => {
    //     isDone = true;
    // });


    // console.log('Waiting for Adams View to die...');
    // while (!isDone) { }
    
    // Delete the log file if it exists
    let log_file = path.join(cwd, 'aview.log');
    if (fs.existsSync(log_file)) {
        fs.unlinkSync(log_file);
    }

    proc = spawn(
        `${adamsLaunchCommand}`,
        ["aview", "ru-s", "i"],
        { cwd: cwd }
    );

    proc.stdout.on('data', function (data) {
        console.log('stdout: ' + data);
    });

    proc.stderr.on('data', function (data) {
        console.log('stderr: ' + data);
    });

    proc.on('exit', function (code) {
        console.log('child process exited with code ' + code);
    });

    // Wait for Adams View to start
    console.log('Waiting for Adams View to start...');
    while (!fs.existsSync(log_file) || fs.readFileSync(log_file, 'utf8').includes("command_server start") == false) { }
    console.log('Adams View Started');

};


function mochaGlobalTeardown(done) {
        // Kill Adams View
        const cleanup = () => {
            return new Promise((resolve, reject) => {
                killProcess('aview.exe', () => {
                    console.log('All tests done');
                    resolve();
                });
            });
        };

        cleanup().then(() => {
            done();
        });
    };

function killProcess(query, done) {
    let cmd = `tasklist`;
    exec(cmd, (err, stdout, stderr) => {
        let lines = stdout.split('\n');
        let matchingLines = lines.filter(line => line.toLowerCase().includes(query.toLowerCase()));

        if (matchingLines.length === 0) {
            console.log('No processes found with the name: ' + query);
        } else {
            matchingLines.forEach(line => {
                let pid = line.split(query)[1].trim().split(' ')[0];
                try {
                    process.kill(pid, 'SIGTERM');
                    console.log('Killed process with PID: ' + pid);
                } catch (err) {
                    console.log('Failed to kill process with PID: ' + pid);
                }
            });
        }
    });
};


exports.mochaGlobalSetup = mochaGlobalSetup;
exports.mochaGlobalTeardown = mochaGlobalTeardown;

mochaGlobalSetup();
