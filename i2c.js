var ina219 = require('ina219');

module.exports = {
    readi2c: function (callback) {

        ina219.init();
        //ina219.enableLogging(true);

        ina219.calibrate32V1A(function () {

            ina219.getBusVoltage_V(function (volts) {

                //console.log("Voltage: " + volts);

                ina219.getCurrent_mA(function (current){
                    //console.log("Current (mA): " + current );

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