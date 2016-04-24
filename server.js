var express = require ('express');
var app = express ();
var path = require('path');
var fs = require ('fs');
var config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
var bodyParser = require('body-parser');
var PythonShell = require('python-shell');

app.use (bodyParser.urlencoded({ extended: false }));



//HTML Web Folder Function
app.get ('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/web/index.html'));
});




//GET Public key & Messages
//Values
app.use ('/values', express.static(__dirname + '/values'));


//POST (Receive Message)
app.post ('/receive', function(req, res){
	if (!req.body) return res.sendStatus(400);

    console.log ("Received a message");
    
    //Decrypt and store the new message
    var options = {
    	mode: 'text',
  		criptPath: '.pyt',
      //pythonPath: '/opt/python3/bin/python3',
      args: [req.body.ciphertext, req.body.signature, req.body.iv]
    };
    //PythonShell 
    PythonShell.run('./python_scripts/r.py', options, function (err, results) {
  	if (err) throw err;
  	// results is an array consisting of messages collected during execution
  	console.log('results: %j', results);
});




	res.send ("Message Received ;)");
});


//SEND



app.listen (config.port);
console.log ('Listening on Port '+ config.port);

