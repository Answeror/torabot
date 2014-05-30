define(function(require, exports, module){
    var self = {
        activated: false,
        default_options: {},
        init: function(options){
            self.options = $.extend({}, self.default_options, options);
        },
        activate: function(){
            if (self.activated) return;
        }
    };
    module.exports = {
        init: self.init,
        activate: self.activate,
        deactivate: self.deactivate
    };
});
