define(function(require, exports, module){
    require('seajs-style');
    require('./ut');
    require('./moment');
    require('./pnotify.custom.min');
    require('./switch');
    require('./xeditable');
    require('handlebars');

    var self = {
        default_options: {
            mods: []
        },
        init_mods: function(){
            var $d = $.Deferred();
            var done = [];
            if (self.options.mods.length) {
                $.map(self.options.mods, function(mod){
                    require.async(mod.name, function(m){
                        m.init(mod.options);
                        done.push(mod.name);
                        if (done.length == self.options.mods.length) {
                            self.init_search(done);
                        }
                    });
                });
            }
        },
        init_search: function(mods){
            require('./search').init({mods: mods});
        },
        init: function(options){
            self.options = $.extend({}, self.default_options, options);
            self.init_mods();
        }
    };
    exports.init = self.init;
});
