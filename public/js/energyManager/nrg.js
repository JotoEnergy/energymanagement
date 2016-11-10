var NRG = (function (NRG, $, undefined) {
    "use strict";

    NRG.init = function() {

        NRG.socket = io.connect();
        NRG.socket.on('news', function (data) {
            console.log(data);
            NRG.socket.emit('my other event', { my: 'data' });
        });

        NRG.socket.on('updates', function (data) {
            //console.log(data);

            var dataArray = data.data;
            var amountData = dataArray.length;

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