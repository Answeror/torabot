define(function(require){
    require('seajs-style')
    require('./ut');
    require('./search');

    Cookie = require('cookie');
    if (Cookie.get('intro') != '0') {
        require('./intro');
    }
});
