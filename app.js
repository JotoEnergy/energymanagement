var PythonShell = require('python-shell');
var express = require('express');


var app = express();
app.use(express.static('public'));


app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.listen(3000);

setInterval(function() {
    PythonShell.run('current.py', function (err, data) {
        if (err) throw err;
        console.log(data);
    })
}, 5000);