const express = require("express");
const upload = require('express-fileupload');
const spawn = require('child_process').spawn;

const app = express();
app.use(express.static("public"));

app.use(upload())
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

app.post('/', function(req,res){
  if(req.files){
    console.log(req.files);
    var file = req.files.file;
    var filename = file.name;
    file.mv("./upload/" + filename, function(err){
      if(err){
        res.send(err);
      } else {
        const process = spawn('python', ['./tamilScript.py', filename]);
        process.stdout.on('data', data=>{
            console.log(data.toString());
          res.sendFile(__dirname + "/output.html");
        })
        process.stderr.on('data', data=> {
            console.error(data.toString());
        })
      }
    })
  }
})

app.listen(3000, '0.0.0.0',function(){
  console.log("Server listening on port 3000");
})
