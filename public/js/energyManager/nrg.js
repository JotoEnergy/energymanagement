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

            $.each(dataArray, function(key, value) {

                console.log(value.power)

            });

        });

    };


    return NRG;
}(NRG || {}, jQuery));


$(document).ready(function() {

    NRG.init();

});