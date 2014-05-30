define(function(require, exports, module){
    Cookie = require('cookie');
    $('.bulletin').bind('closed.bs.alert', function(){
        Cookie.set('hide_bulletin_id', $('.bulletin *[name="id"]').prop('value'), {path: '/'});
    });
});
