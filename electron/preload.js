const { contextBridge } = require('electron');

// Expose secure API to renderer process if needed
contextBridge.exposeInMainWorld('electronAPI', {
    getAppVersion: () => '1.2.1',
    getAppName: () => 'My Desktop VTuber'
});
