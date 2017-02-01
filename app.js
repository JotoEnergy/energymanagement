
var i2c = require('./i2c');


setInterval(function() {

    app();
    
}, 1000);



function app () {



        readDatabaseForDevices(function(devices) {


            for(x=0;x<devices.length;x++) {
                var address = devices[x].connection;
                var deviceId = devices[x].id;
                var deviceName = devices[x].name;

                console.log(deviceName);

                readi2cAndWriteIntoDatabase(address, deviceId);
            }

        });


}



//var address = [ 0x40, 0x41, 0x44, 0x45 ];

function getAddressFromString (address) {

    var useAddress;
    switch(address) {
        case '0x40':
            useAddress = 0x40;
        break;
        case '0x41':
            useAddress = 0x41;
        break;
        case '0x42':
            useAddress = 0x42;
            break;
        case '0x43':
            useAddress = 0x43;
            break;
        case '0x44':
            useAddress = 0x44;
            break;
        case '0x45':
            useAddress = 0x45;
            break;
        default:
            useAddress = 0x40;
        break;
    }

    return useAddress;

}


function readi2cAndWriteIntoDatabase(address, id) {

    var i2cAddress = getAddressFromString(address);

    try {

        var ampereAndVolt1 = i2c.readi2c(i2cAddress, function(voltAndAmpere) {

            if(voltAndAmpere.volts < 1) {
                voltAndAmpere.volts = 0;
            }

            voltAndAmpere.current = voltAndAmpere.current * 4;

            var logAmpereAndVolt = JSON.stringify(voltAndAmpere);

            //console.log('Adresse: '+address);
            console.log(logAmpereAndVolt);
            console.log('------------------------------');

            var timest = Math.floor(Date.now() / 1000);
            var volt = voltAndAmpere.volts;
            var current = voltAndAmpere.current / 1000;

            var watt = current * volt;

            var connection = createMysqlConnection();
            connection.connect();
            connection.query('INSERT INTO energyLog (deviceid, volt, ampere, watt, datum) VALUES (?, ?, ?, ?, ?)', [id, voltAndAmpere.volts, voltAndAmpere.current, watt, timest], function(err, rows, fields) {
                if (err) throw err;

                connection.end();

            });


        });

    } catch(e) {
        //console.log(e);
        console.log(address+' Address not available');
    } finally {
        //console.log('Done');
    }



}

function readDatabaseForDevices (callback) {

    var connection = createMysqlConnection();
    connection.connect();
    connection.query('SELECT * FROM device', function(err, rows, fields) {
        if (err) throw err;

        var devices = rows;
        connection.end();
        return callback(devices);

    });

}

/*
INSERT NEW DEVICE
 INSERT INTO device (name, connection, typ, datum) VALUES ("solarpanel","0x40","quelle","1484767591");

 */

function createMysqlConnection() {

    var params={
        host     : 'localhost',
        user     : 'root',
        password : 'joto123',
        database : 'energyMonitor'
    };

    return mysql.createConnection(params);
}