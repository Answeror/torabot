define(function(require, exports, module){
    // http://stackoverflow.com/a/5890983/238472
    Object.defineProperty(Object.prototype, "contains", {
        value: function(o) {
            return this.indexOf(o) != -1;
        },
        enumerable: false
    });
});
