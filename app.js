var express = require('express');
var path = require('path');
var mysql      = require('mysql');
var i2c = require('./i2c');

var app = express();

var server = require('http').Server(app);
var io = require('socket.io')(server);

var port = 3000;
server.listen(port, "127.0.0.1");

app.use(express.static('public'));
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});



io.on('connection', function (socket) {

    socket.emit('check', { hello: 'world' });
    socket.on('established', function (data) {
        console.log('Socket connection successfully established.');
    });

    setInterval(function() {

        var address = 0x41;
        var ampereAndVolt = i2c.readi2c(address, function(voltAndAmpere) {

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