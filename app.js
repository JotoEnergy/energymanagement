var PythonShell = require('python-shell');


setInterval(function() {
    PythonShell.run('current.py', function (err, data) {
        if (err) throw err;
        console.log(data);
    })
}, 5000);