const vscode = require('vscode');

/**
 * @param {vscode.CancellationToken} token
 * @returns {vscode.ProviderResult<vscode.TerminalProfile>}
 */
function terminal_profile_provider(token) {
    // TODO: get the current setting for adams_launch_command ...
    return {
        name: 'Adams',
        shellPath: 'cmd.exe'
    }
}

exports.terminal_profile_provider = terminal_profile_provider;
