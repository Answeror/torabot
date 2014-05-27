define(function(require, exports, module){
    // http://stackoverflow.com/a/5890983/238472
    Object.defineProperty(Object.prototype, "contains", {
        value: function(o) {
            return this.indexOf(o) != -1;
        },
        enumerable: false
    });

    RegExp.escape = function(str) {
        return String(str).replace(/([.*+?^=!:${}()|[\]\/\\])/g, '\\(');
    };

    $.torabot = {};
    $.torabot.cast = function(type, value) {
        return ({
            text: function(x) { return x.toString(); },
            int: parseInt
        })[type](value);
    };

    exports.zip = function(){
        var args = [].slice.call(arguments);
        var shortest = args.length==0 ? [] : args.reduce(function(a,b){
            return a.length<b.length ? a : b
        });

        return shortest.map(function(_,i){
            return args.map(function(array){return array[i]})
        });
    };
});
