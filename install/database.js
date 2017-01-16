var mysql      = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : 'joto123',
    database : 'energyMonitor'
});

connection.connect();

//Create Table
 connection.query('CREATE TABLE davice (id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), connection VARCHAR(60), typ VARCHAR(20), datum VARCHAR(50), UNIQUE KEY (id) )', function(err, rows, fields) {
 if (err) throw err;

 console.log(rows);
 });

connection.query('CREATE TABLE systemSetup (id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY, kostenProKWH VARCHAR(100), systemKey VARCHAR(60), name VARCHAR(40), datum VARCHAR(50), UNIQUE KEY (id) )', function(err, rows, fields) {
    if (err) throw err;

    console.log(rows);
});

connection.query('CREATE TABLE energyLog (id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY, deviceid VARCHAR(100), volt VARCHAR(60), ampere VARCHAR(60), watt VARCHAR(60), datum VARCHAR(50), UNIQUE KEY (id) )', function(err, rows, fields) {
    if (err) throw err;

    console.log(rows);
});

connection.end();