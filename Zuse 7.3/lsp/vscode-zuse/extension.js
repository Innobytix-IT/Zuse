// FILE: extension.js
// VS Code Extension für Zuse Language Support
// Startet den Zuse Language Server als Child-Process.

const vscode = require('vscode');
const { LanguageClient, TransportKind } = require('vscode-languageclient/node');
const path = require('path');

let client;

function activate(context) {
    const config = vscode.workspace.getConfiguration('zuse');
    const pythonPath = config.get('server.python', 'python');

    // Server-Pfad ermitteln
    let serverPath = config.get('server.path', '');
    if (!serverPath) {
        // Versuche den Server relativ zur Extension zu finden
        serverPath = path.join(__dirname, '..', 'zuse_server.py');
    }

    const serverOptions = {
        command: pythonPath,
        args: [serverPath],
        transport: TransportKind.stdio,
    };

    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'zuse' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.zuse'),
        },
    };

    client = new LanguageClient(
        'zuseLanguageServer',
        'Zuse Language Server',
        serverOptions,
        clientOptions
    );

    client.start();
    console.log('Zuse Language Server gestartet');
}

function deactivate() {
    if (client) {
        return client.stop();
    }
}

module.exports = { activate, deactivate };
