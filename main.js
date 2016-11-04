/* jshint esversion: 6 */

const {app, BrowserWindow, crashReporter} = require('electron');

// Reports server crashes to the designated submitURL (which is unset at the moment)
crashReporter.start({
    productName: 'stitch-flex',
    companyName: 'lukejfernandez',
    submitURL: '',
    autoSubmit: false
});


// Global reference for the mainWindow to bypass garbage collection
let mainWindow = null;

// Called when Electron initialization is complete and instance is ready to create browser windows.
app.on('ready', function() {

  // Creates python child process for running python instructions in app/app.py
  let python_subprocess = require('child_process').spawn('python', ['./app/app.py']);

  // Imports request-promise for request and promise handling
  let request = require('request-promise');
  let mainAddress = 'http://localhost:5000';

  let openWindow = function(){
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

  let startUp = function(){
    request(mainAddress)
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
