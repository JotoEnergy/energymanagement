var PythonShell = require('python-shell');
var express = require('express');
var path = require('path');
var mysql      = require('mysql');

function createMysqlConnection() {

    var params={
        host     : 'localhost',
        user     : 'root',
        password : 'joto123',
        database : 'raspi'
    };

    return mysql.createConnection(params);
}


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
    socket.emit('news', { hello: 'world' });
    socket.on('my other event', function (data) {
        console.log(data);
    });


    //Start first GUI Update
    var connection = createMysqlConnection();
    connection.connect();
    connection.query('SELECT * FROM powerSensor' , function(err, rows, fields) {
        if (err) throw err;

        console.log(rows);
        socket.emit('updates', { data: rows });
        connection.end();
    });


    //Update GUI in Intervals
    setInterval(function() {

        var connection = createMysqlConnection();
        connection.connect();
        connection.query('SELECT * FROM powerSensor' , function(err, rows, fields) {
            if (err) throw err;

            console.log(rows);
            socket.emit('updates', { data: rows });
            connection.end();
        });
    }, 5000);


});

console.log('App started.');
console.log('Express Server listening on: http://localhost:'+port);


//Setup listening to Python script /S
setInterval(function() {
    PythonShell.run('current.py', function (err, data) {
        if (err) throw err;
        console.log(data);
    })
}, 5000);