var express = require('express');
var path = require('path');
var mysql      = require('mysql');

var _ = require('underscore');


//Initialize Express
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);
//Setup localhost port
var port = 3000;
server.listen(port, "127.0.0.1");

//Folder public contains html, css and javascript files for frontend
app.use(express.static('public'));
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});


io.on('connection', function (socket) {

    socket.emit('check', { hello: 'world' });
    socket.on('established', function (data) {
        console.log('Socket connection successfully established.');
    });



    //socket.emit('data', { data: voltAndAmpere, address: address1 });

    /*
     var ampereAndVoltAddress2 = i2c.readi2c(address2, function(voltAndAmpere) {

     var logAmpereAndVolt = JSON.stringify(voltAndAmpere);
     console.log('Adresse2:');
     console.log(logAmpereAndVolt);


     socket.emit('data', { data: voltAndAmpere, address: address2 });

     });
     */


});

console.log('App started.');
console.log('Express Server listening on: http://localhost:'+port);