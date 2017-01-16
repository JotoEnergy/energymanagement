var mysql      = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
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

/*
 connection.query('CREATE TABLE payout_log (id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY, email VARCHAR(50) NOT NULL, address VARCHAR(60), amount VARCHAR(30), datum VARCHAR(50), forwarded VARCHAR(50), UNIQUE KEY (id) )', function(err, rows, fields) {
 if (err) throw err;

 console.log(rows);
 });
 */

/*
 //Insert Row
 var timest = Math.floor(Date.now() / 1000);

 connection.query('INSERT INTO test2 (email, validation, two_fa, reg_date) VALUES ("testmail", "123", "no", "'+timest+'")', function(err, rows, fields) {
 if (err) throw err;

 console.log(rows);
 });


 connection.query('UPDATE test2 SET two_fa = "yes" WHERE email = "testmail"', function(err, rows, fields) {
 if (err) throw err;

 console.log(rows);
 });
 */

/*

 connection.query('SELECT * FROM test2', function(err, rows, fields) {
 if (err) throw err;

 console.log(rows);
 });

 */

/*
 connection.query('CREATE TABLE users (id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY, email VARCHAR(50) NOT NULL, validation VARCHAR(60), two_fa VARCHAR(10), reg_date VARCHAR(50), UNIQUE KEY (id, email) )', function(err, rows, fields) {
 if (err) throw err;

 console.log(rows);
 });


 var data = [];
 data['email'] = 'toschdev@gmail.com';

 connection.query('SELECT * FROM users WHERE email =?', [data['email']], function(err, rows, fields) {
 if (err) throw err;


 //console.log(rows.length);
 if(rows.length > 0) {

 console.log('User exists: ');
 console.log(rows);


 } else {
 console.log('User does not exist yet');
 }

 });
 */
/*
 connection.query('UPDATE users SET two_fa = "no" WHERE email = ?', [data['email']], function(err, rows, fields) {
 if (err) throw err;

 //console.log(rows.length);
 if(rows.length > 0) {

 console.log('User exists: ');
 console.log(rows);


 } else {
 console.log('User does not exist yet');
 }

 });
 */
/*
 //Alter Table
 //var sql = 'alter table users change two_fa two_fa varchar(255)';


 //RESET 2FA
 //var sql = 'UPDATE users SET two_fa = "no" WHERE';

 connection.query(sql, function(err, rows, fields) {
 if (err) throw err;

 console.log(rows);

 });
 */
connection.end();
