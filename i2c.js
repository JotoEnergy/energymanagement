var ina219 = require('ina219');

module.exports = {
    readi2c: function (address, callback) {

        ina219.init(address);
        //ina219.enableLogging(true);

        ina219.calibrate32V1A(function () {

            ina219.getBusVoltage_V(function (volts) {

                //console.log("Voltage: " + volts);

                    ina219.getCurrent_mA(function (current){
                        //console.log("Current (mA): " + current );

                        current = (2600 - current) * 2;
                        var voltAndAmpere = {
                            volts: volts,
                            current: current
                        };

                        //console.log(JSON.stringify(voltAndAmpere));

                        return callback(voltAndAmpere);

                    });

            });

        });
    }
};