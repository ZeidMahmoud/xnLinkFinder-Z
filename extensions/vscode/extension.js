const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('xnlinkfinder.findEndpoints', function () {
        vscode.window.showInformationMessage('xnLinkFinder: Finding endpoints...');
        // Call xnLinkFinder CLI or API here
    });
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}
