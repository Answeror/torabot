define(function(require, exports, module){
    require('seajs-style');
    require('./ut');
    require('./moment');
    require('./pnotify.custom.min');
    require('./switch');
    require('./xeditable');
    require('./search');

    var self = {
        default_options: {
            mods: []
        },
        init_mods: function(){
            if (self.options.mods.length) {
                $.map(self.options.mods, function(mod){
                    require.async(mod.name, function(m){
                        m.init(mod.options);
                    });
                });
            }
        },
        init: function(options){
            self.options = $.extend({}, self.default_options, options);
            self.init_mods();
        }
    };
    exports.init = self.init;
});
