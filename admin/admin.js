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
app.use(express.static());
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});


io.on('connection', function (socket) {

    socket.emit('check', { hello: 'world' });
    socket.on('established', function (data) {
        console.log('Socket connection successfully established.');



    });

    setInterval(function() {

        getDatabaseEntries(function(data) {

            socket.emit('databaseEntries', data);

        });


    }, 1000);

});


function getDatabaseEntries (callback) {

    var amountOfINAs = 4;
    var ONE_HOUR = 3600;
    var ONE_MINUTE = 60;

    var takeDataBaseEntries = amountOfINAs * ONE_MINUTE;

    var connection = createMysqlConnection();
    connection.connect();
    connection.query('SELECT * FROM energyLog LIMIT '+takeDataBaseEntries+'', function(err, rows, fields) {
        if (err) throw err;

        return callback(rows);

        connection.end();

    });


}



console.log('App started.');
console.log('Express Server listening on: http://localhost:'+port);