const assert = require('assert');
const path = require('path');
const fs = require('fs');
const vscode = require('vscode');
const os = require('os');
const { spawn, exec,  } = require('child_process');
const { run_selection } = require('../src/run_selection.ts.js');


output_channel = vscode.window.createOutputChannel('MSC Adams Testing');


suite('Extension Test Suite', () => {

    let proc;
    const cwd = path.join(vscode.workspace.workspaceFolders[0].uri.fsPath, 'working_directory');

    suiteSetup(() => {
        vscode.window.showInformationMessage('Start all tests.');
        
        const adamsLaunchCommand = process.env.ADAMS_LAUNCH_COMMAND;
        let log_file = path.join(cwd, 'aview.log');

        // Delete the log file if it exists
        if (fs.existsSync(log_file)) {
            fs.unlinkSync(log_file);
        }

        while (fs.existsSync(log_file)) {
            console.log('Waiting for log file to be deleted...');
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
        while (!fs.existsSync(log_file) || fs.readFileSync(log_file, 'utf8').includes("command_server start") == false) {}
        console.log('Adams View Started');

    });
        
    suiteTeardown( (done) => {
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
        
    });


    test('run_selection, python, not entire file', async () => {
        const tempFilePath = path.join(os.tmpdir(), 'run_selection_not_entire_file.py');
        const tempFileContent = "print('this should be shown')\nprint('this should not be shown')";
        fs.writeFileSync(tempFilePath, tempFileContent);
    
        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {
                //  Select the first line
                editor.selection = new vscode.Selection(0, 0, 1, 0);
    
                // Run the msc_adams.runSelection command
                await run_selection(output_channel, false)()
        
                // Give the command some time to finish
                await new Promise(resolve => setTimeout(resolve, 1000));
                const logFilePath = path.join(
                    vscode.workspace.workspaceFolders[0].uri.fsPath,
                    'working_directory',
                    'aview.log'
                );
                const logFileContent = fs.readFileSync(logFilePath, 'utf8');
                const lastLine = logFileContent.trim().split('\n').pop();
                assert.strictEqual(lastLine, "! this should be shown");
            });
        });
    });


    test('run_selection, python, entire file', async () => {
        const tempFilePath = path.join(os.tmpdir(), 'run_selection_entire_file.py');
        const tempFileContent = "print('this should be shown')\nprint('this should ALSO be shown')";
        fs.writeFileSync(tempFilePath, tempFileContent);
    
        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {
                
                // Select the first character of the first line
                editor.selection = new vscode.Selection(0, 0, 0, 1);

                // Run the msc_adams.runSelection command
                await run_selection(output_channel, true)();
        
                // Give the command some time to finish
                await new Promise(resolve => setTimeout(resolve, 1000));
                const logFilePath = path.join(
                    vscode.workspace.workspaceFolders[0].uri.fsPath,
                    'working_directory',
                    'aview.log');
                const logFileContent = fs.readFileSync(logFilePath, 'utf8');
                const lastTwoLines = logFileContent.trim().split(/\r?\n/).slice(-2);
                const expectedLines = ["! this should be shown", "! this should ALSO be shown"];
                assert.deepStrictEqual(lastTwoLines, expectedLines);
            });
        });
    });


    test('run_selection, cmd, not entire file', async () => {
        const tempFilePath = path.join(os.tmpdir(), 'run_selection_not_entire_file.cmd');
        const tempFileContent = "var set var=.mdi.tmpstr str=(eval(str_print('this should be shown')))\n" +
                                "var set var=.mdi.tmpstr str=(eval(str_print('this should not be shown')))";
        fs.writeFileSync(tempFilePath, tempFileContent);

        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {

                //  Select the first line
                editor.selection = new vscode.Selection(0, 0, 1, 0);

                // Run the msc_adams.runSelection command
                await run_selection(output_channel, false)()

                // Give the command some time to finish
                await new Promise(resolve => setTimeout(resolve, 1000));
                const logFilePath = path.join(
                    vscode.workspace.workspaceFolders[0].uri.fsPath,
                    'working_directory',
                    'aview.log'
                );
                const logFileContent = fs.readFileSync(logFilePath, 'utf8');
                const lastLine = logFileContent.trim().split('\n').pop();
                assert.strictEqual(lastLine, "! this should be shown");
            });
        });
    });


    test('run_selection, cmd, entire file', async () => {
        
        // create a file in the user's temp directory
        const tempFilePath = path.join(os.tmpdir(), 'run_selection_entire_file.cmd');
        const tempFileContent = "var set var=.mdi.tmpstr str=(eval(str_print('this should be shown')))\n" +
                                "var set var=.mdi.tmpstr str=(eval(str_print('this should ALSO be shown')))";
        fs.writeFileSync(tempFilePath, tempFileContent);

        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {

                // Select the first character of the first line
                editor.selection = new vscode.Selection(0, 0, 0, 1);

                // Run the msc_adams.runSelection command
                await run_selection(output_channel, true)();

                // Give the command some time to finish
                await new Promise(resolve => setTimeout(resolve, 1000));
                const logFilePath = path.join(
                    vscode.workspace.workspaceFolders[0].uri.fsPath,
                    'working_directory',
                    'aview.log');
                const logFileContent = fs.readFileSync(logFilePath, 'utf8');
                const lastTwoLines = logFileContent.trim().split(/\r?\n/).slice(-2);
                const expectedLines = ["! this should be shown", "! this should ALSO be shown"];
                assert.deepStrictEqual(lastTwoLines, expectedLines);
            });
        });
    });


});


const killProcess = (query, done) => {
    let cmd = `tasklist`; 
    exec(cmd, (err, stdout, stderr) => {

        let proc_exists = (stdout.toLowerCase().indexOf(query.toLowerCase()) > -1);
        if (!proc_exists) {
            console.log('Adams View is not running')
            done()
        }
        else {
            // Get the process id
            let pid = stdout.split(query)[1].trim().split(' ')[0];
            process.kill(pid, 'SIGTERM');
            console.log('Adams View Killed');
            done()
        }
    });
}
