var PythonShell = require('python-shell');

PythonShell.run('current.py', function (err) {
    if (err) throw err;
    console.log('finished');
});