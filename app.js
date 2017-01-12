var express = require('express');
var path = require('path');
var mysql      = require('mysql');
var i2c = require('./i2c');
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

//var address = [ 0x40, 0x41, 0x44, 0x45 ];

io.on('connection', function (socket) {

    socket.emit('check', { hello: 'world' });
    socket.on('established', function (data) {
        console.log('Socket connection successfully established.');
    });

    setInterval(function() {

        var ampereAndVolt = i2c.readi2c(0x40, function(voltAndAmpere) {

            var logAmpereAndVolt = JSON.stringify(voltAndAmpere);
            console.log(logAmpereAndVolt);


            socket.emit('data', { data: voltAndAmpere });

        });
    }, 1000);

});

console.log('App started.');
console.log('Express Server listening on: http://localhost:'+port);


function createMysqlConnection() {

    var params={
        host     : 'localhost',
        user     : 'root',
        password : 'joto123',
        database : 'raspi'
    };

    return mysql.createConnection(params);
}