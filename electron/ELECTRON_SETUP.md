# Electron Desktop Application Setup

This guide explains how to build and run My Desktop VTuber as an Electron desktop application.

## Prerequisites

- Node.js 16+ (download from https://nodejs.org/)
- npm or yarn
- Python 3.10+ with all dependencies installed (via `uv sync`)

## Installation Steps

### 1. Install Electron Dependencies

```bash
cd electron
npm install
```

This installs:
- `electron` - The framework for building desktop apps
- `electron-builder` - For packaging and building installers

### 2. Run in Development Mode

```bash
npm start
```

Or with verbose logging:
```bash
npm run dev
```

This will:
1. Start the FastAPI backend (Python server on port 12393)
2. Launch the Electron window
3. Load the web interface

### 3. Build Executable/Installer

#### For Windows (NSIS installer + portable):
```bash
npm run build-win
```

#### For macOS (DMG + ZIP):
```bash
npm run build-mac
```

#### For Linux (AppImage + DEB):
```bash
npm run build-linux
```

The built files will be in the `dist/` folder.

## How It Works

### Main Process (Electron)
- `main.js` - Electron main process that:
  - Spawns the Python FastAPI server as a child process
  - Creates the BrowserWindow
  - Handles app lifecycle events
  - Manages the application menu

### Preload Script
- `preload.js` - Secure bridge between Electron and renderer process
  - Exposes only safe APIs to the web frontend
  - Implements context isolation for security

### Python Backend
- The FastAPI server runs as a subprocess
- Electron connects to it via `http://localhost:12393`
- When the Electron app closes, it automatically kills the Python process

## Configuration

### Change Server Port
Edit `main.js` line `mainWindow.loadURL()` to use a different port:
```javascript
mainWindow.loadURL('http://localhost:YOUR_PORT');
```

Also update `conf.yaml` port setting.

### Add App Icon
1. Create a PNG image (512x512 recommended)
2. Place it in `electron/assets/icon.png`
3. It will be used in the taskbar and window title

### Customize Menu
Edit the `createMenu()` function in `main.js` to add/remove menu items.

## Distribution

### Windows:
- NSIS installer (recommended for end users)
- Portable EXE (no installation needed)

### macOS:
- DMG installer
- ZIP for direct app distribution

### Linux:
- AppImage (run without installation)
- DEB package (for Debian/Ubuntu)

## Troubleshooting

### Python server fails to start
- Ensure Python is in PATH or virtual environment is activated
- Check that port 12393 is not in use
- Review console output in DevTools (Ctrl+Shift+I)

### "Cannot find python executable"
- The main.js tries to find Python in the .venv folder
- Ensure you've run `uv sync` to create the virtual environment
- Or modify the pythonExe path in main.js

### App won't start on Linux
- Install required dependencies: `sudo apt-get install libgtk-3-0 libxss1`
- Run with: `electron .`

### Build fails
- Delete `node_modules` and `dist` folders
- Run `npm install` again
- Try `npm run build`

## Performance Notes

- First launch takes longer (Python server startup)
- Subsequent launches are faster (cached resources)
- Keep Python dependencies minimal for faster startup
- Consider using `--no-sandbox` flag if running in restricted environments

## Next Steps

1. Test in development mode with `npm start`
2. Once working, build installers with `npm run build`
3. Distribute the installers to users
4. Users can run the app without needing Python installed on their system
