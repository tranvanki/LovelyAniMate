const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const spawn = require('child_process').spawn;
const os = require('os');
const fs = require('fs');

let mainWindow;
let pythonProcess;

// Function to start the FastAPI server
function startPythonServer() {
    const pythonScriptPath = path.join(__dirname, '..', 'run_server.py');
    const projectRoot = path.join(__dirname, '..');
    
    // Determine Python executable based on OS
    let pythonExe = 'python';
    if (process.platform === 'win32') {
        // On Windows, try to use the virtual environment Python
        const venvPython = path.join(projectRoot, '.venv', 'Scripts', 'python.exe');
        const uvPython = path.join(projectRoot, '.venv', 'bin', 'python.exe');
        
        if (fs.existsSync(venvPython)) {
            pythonExe = venvPython;
        } else if (fs.existsSync(uvPython)) {
            pythonExe = uvPython;
        }
    }

    console.log(`Starting Python server with: ${pythonExe}`);
    
    pythonProcess = spawn(pythonExe, [pythonScriptPath], {
        cwd: projectRoot,
        stdio: 'inherit',
        shell: true
    });

    pythonProcess.on('error', (err) => {
        console.error('Failed to start Python server:', err);
    });

    pythonProcess.on('exit', (code) => {
        console.log(`Python server exited with code ${code}`);
    });

    // Give the server time to start
    return new Promise((resolve) => {
        setTimeout(resolve, 3000);
    });
}

// Function to create the main window
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true
        },
        icon: path.join(__dirname, 'assets', 'icon.png') // Optional: add an app icon
    });

    // Load the FastAPI server
    mainWindow.loadURL('http://localhost:12393');

    // Open DevTools in development (comment out for production)
    // mainWindow.webContents.openDevTools();

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// App event handlers
app.on('ready', async () => {
    console.log('Electron app ready. Starting Python server...');
    await startPythonServer();
    createWindow();
    createMenu();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

app.on('before-quit', () => {
    // Kill the Python process when closing the app
    if (pythonProcess) {
        pythonProcess.kill();
    }
});

// Create application menu
function createMenu() {
    const template = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'Exit',
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'View',
            submenu: [
                {
                    label: 'Reload',
                    accelerator: 'CmdOrCtrl+R',
                    click: () => {
                        mainWindow.reload();
                    }
                },
                {
                    label: 'Toggle DevTools',
                    accelerator: 'CmdOrCtrl+Shift+I',
                    click: () => {
                        mainWindow.webContents.toggleDevTools();
                    }
                }
            ]
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'About',
                    click: () => {
                        console.log('My Desktop VTuber v1.2.1');
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}
