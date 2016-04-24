var PythonShell =  require ('python-shell');
var parser = require('json-parser');
var fs = require ('fs');
var jsonfile = require ('jsonfile');



//var content=fs.readFileSync("./values/pubkey.json");
//console.log (JSON.parse(content));
//var file = './values/pubkey.json';

init ();

function init () {
  genPubkey ()
}



function genPubkey () {
  PythonShell.run('./python_scripts/init.py', function (err) {
  if (err) throw err;
  console.log('Public Key Generated');
  });
}

