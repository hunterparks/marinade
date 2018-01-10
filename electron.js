// ./main.js
const { app, BrowserWindow } = require('electron');

let win = null;

function createDefaultWindow() {
  // Initialize the window to our specified dimensions
  win = new BrowserWindow({ width: 1000, height: 600 });
  // Show dev tools
  // Remove this line before distributing
  win.webContents.openDevTools();
  // Remove window once app is closed
  win.on('closed', function () {
    win = null;
  });
  let urlSource = process.argv[2];
  // Specify entry point
  if (urlSource === 'dynamic') {
    win.loadURL('http://localhost:4200');
  } else {
    win.loadURL(`file://${__dirname}/dist/index.html`);
  }
  return win;
}

app.on('ready', function() {
  createDefaultWindow();
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (win === null) {
    createWindow();
  }
})
