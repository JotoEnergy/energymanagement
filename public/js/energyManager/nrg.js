var NRG = (function (NRG, $, undefined) {
    "use strict";

    NRG.init = function() {

        NRG.socket = io.connect();
        NRG.socket.on('check', function (data) {
            //console.log(data);
            console.log('Socket connected');
            NRG.socket.emit('established');
        });

        NRG.socket.on('updates', function (data) {
            //console.log(data);

            var dataArray = data.data;
            var amountData = dataArray.length;

            NRG.inputData = dataArray;
            NRG.powerData = {
                "datum": [],
                "power": []
            } ;

            $.each(NRG.inputData, function(key, value) {
               NRG.powerData.power.push(value.power);
                NRG.powerData.datum.push(value.datum);
            });

            //Just short hack
            NRG.powerData.power.slice(0,6);

            var lastItem = dataArray[amountData-1];
            var power = lastItem.power;
            var inputPower = 0;
            var outputPower = 0;
            if(lastItem.power < 0) {
                outputPower = lastItem.power * -1;
            } else {
                inputPower = lastItem.power;
            }
            //console.log(value.power)
            $("#total_incoming_power").html(inputPower + 'W');
            $("#total_devices").html('1');
            $("#power_output").html(outputPower + 'W');

        });

    };


    return NRG;
}(NRG || {}, jQuery));


$(document).ready(function() {

    NRG.init();

});