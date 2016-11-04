/* jshint esversion: 6 */

const {app, BrowserWindow, crashReporter} = require('electron');

// Report crashes to our server.
crashReporter.start({
    productName: 'stitch-flex',
    companyName: 'lukejfernandez',
    submitURL: '',
    autoSubmit: false
});


// Global reference for the mainWindow to bypass garbage collection
var mainWindow = null;

// This method will be called when Electron has done everything
// initialization and ready for creating browser windows.
app.on('ready', function() {

  var python_subprocess = require('child_process').spawn('python', ['./app/app.py']);

  var rq = require('request-promise');
  var mainAddr = 'http://localhost:5000';

  var openWindow = function(){
    // Create the browser window.
    mainWindow = new BrowserWindow({width: 800, height: 600});
    // and load the index.html of the app.
    // mainWindow.loadURL('file://' + __dirname + '/index.html');
    mainWindow.loadURL('http://localhost:5000');
    // Open the devtools.
    // mainWindow.webContents.openDevTools();
    // Emitted when the window is closed.
    mainWindow.on('closed', function() {
      // Dereferences the mainWindow object. Replace with stack, if multiwindow
      mainWindow = null;
      // Kills subprocess opened up to pass Python to Electron
      python_subprocess.kill('SIGINT');
    });
  };

// Ensures quit on window close, even for OSX
app.on('window-all-closed', function() {
  //if (process.platform != 'darwin') {
    app.quit();
  //}
});

  var startUp = function(){
    rq(mainAddr)
      .then(function(htmlString){
        console.log('Server initialized and started.');
        openWindow();
      })
      .catch(function(err){
        console.log('Waiting for server to start...');
        startUp();
      });
  };

  startUp();
});
