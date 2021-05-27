var express = require('express'),
    port = process.env.PORT || 3000,
    app = express();
    path = require('path');
    cookieParser = require('cookie-parser');
    logger = require('morgan');

// var cors = require('cors');
// const port = normalizePort(process.env.PORT || '3000');


var app = express();

app.set('port', port);
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
// app.use(cors());
app.use(express.static(path.join(__dirname, 'app')));

app.listen(port);
// module.exports = app;
