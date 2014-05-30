define(function(require, exports, module){
    var self = {
        activated: function(){
            return self.completion.activated();
        },
        activate: function(){
            return self.completion.activate();
        },
        deactivate: function(){
            return self.completion.deactivate();
        },
        match: function(q, cb){
            var query = q.split(' ').slice(-1)[0];
            return self.fetch(query).done(function(data){
                return cb($.map(data.result, function(post){
                    return {value: post.name};
                }));
            });
        },
        fetch: function(query){
            return $.ajax({
                url: self.make_json_uri(query),
                type: 'get'
            });
        },
        make_json_uri: function(query){
            return self.options.call_url + '?' + $.param({
                arg: JSON.stringify({
                    'type': 'completion',
                    'query': query + '*'
                })
            });
        },
        default_options: {},
        init: function(options){
            self.options = $.extend({}, self.default_options, options);
            self.completion = require('main/completion').make({
                source: self.match
            });
        }
    };
    module.exports = {
        init: self.init,
        activate: self.activate,
        deactivate: self.deactivate
    };
});
