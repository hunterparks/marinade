// ./main.js
const {app, BrowserWindow} = require('electron');
const path = require('path');

let win = null;

app.on('ready', function () {

  // Initialize the window to our specified dimensions
  win = new BrowserWindow({width: 1000, height: 600});

  // Specify entry point
  win.loadURL('http://localhost:4200');

  // Show dev tools
  // Remove this line before distributing
  win.webContents.openDevTools();

  // Remove window once app is closed
  win.on('closed', function () {
    win = null;
  });

});

app.on('activate', () => {
  if (win === null) {
    createWindow();
  }
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

let pyProc = null;
let pyPort = null;

const selectPort = () => {
  pyPort = 4242;
  return pyPort
};

const createPyProc = () => {
  let port = '' + selectPort();
  let script = path.join(__dirname, 'backend', 'src', 'api.py');
  pyProc = require('child_process').spawn('python', [script, port]);
  if (pyProc !== null) {
    console.log('child process success')
  }
};

const exitPyProc = () => {
  pyProc.kill();
  pyProc = null;
  pyPort = null;
};

app.on('ready', createPyProc);
app.on('will-quit', exitPyProc);
