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

        var address1 = 0x40;
        var address2 = 0x41;

        var ampereAndVolt1 = i2c.readi2c(address1, function(voltAndAmpere) {

            var logAmpereAndVolt = JSON.stringify(voltAndAmpere);
            console.log('Adresse1:');
            console.log(logAmpereAndVolt);


            socket.emit('data', { data: voltAndAmpere, address: address1 });

            var timest = Math.floor(Date.now() / 1000);
            var volt = voltAndAmpere.volts;
            var current = voltAndAmpere.current / 1000;

            var watt = current * volt;

            var connection = createMysqlConnection();
            connection.connect();
            connection.query('INSERT INTO energyLog (deviceid, volt, ampere, watt, datum) VALUES ("1", ?, ?, ?, ?)', [voltAndAmpere.volts, voltAndAmpere.current, watt, timest], function(err, rows, fields) {
                if (err) throw err;

                connection.end();

            });

        });

        /*
        var ampereAndVoltAddress2 = i2c.readi2c(address2, function(voltAndAmpere) {

            var logAmpereAndVolt = JSON.stringify(voltAndAmpere);
            console.log('Adresse2:');
            console.log(logAmpereAndVolt);


            socket.emit('data', { data: voltAndAmpere, address: address2 });

        });
        */

    }, 1000);

});

console.log('App started.');
console.log('Express Server listening on: http://localhost:'+port);


function createMysqlConnection() {

    var params={
        host     : 'localhost',
        user     : 'root',
        password : 'joto123',
        database : 'energyMonitor'
    };

    return mysql.createConnection(params);
}