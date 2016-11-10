var PythonShell = require('python-shell');



PythonShell.run('current.py', function (err, data) {
    if (err) throw err;
    console.log(data);
});