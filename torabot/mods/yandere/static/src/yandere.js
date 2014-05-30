define(function(require, exports, module){
    var self = {
        create_tag_search_regex: require('./create_tag_search_regex'),
        retrieve_tag_search: require('./retrieve_tag_search'),
        reorder_search_results: require('./reorder_search_results'),
        split_result: require('./split_result'),
        complete_tag: function(tag){
            var re = self.create_tag_search_regex(tag, {global: true});
            var main_results = self.retrieve_tag_search(re, self.options.source, {max_results: 100});
            main_results = self.reorder_search_results(tag, main_results);
            var results = main_results;
            self.bubble_rating_tags(results, tag);
            results = results.slice(0, self.options.max_results != null? self.options.max_results:10);
            return self.split_result(results);
        },
        bubble_rating_tags: function(results, tag){
            /* Hack: if the search is one of the ratings shortcuts, put that at the top, even though
             * it's not a real tag. */
            if ("sqe".indexOf(tag) != -1) results.unshift("0`" + tag + "` ");
        },
        match: function(q, cb){
            var tag = q.split(' ').slice(-1)[0];
            if (tag) {
                var ret = self.complete_tag(tag);
                cb($.map(require('main/ut').zip(ret[0], ret[1]), function(args){
                    return {
                        value: args[0],
                        alias: args[1].map(function(x){
                            return {value: x};
                        })
                    };
                }));
            }
        },
        default_options: {
            completion_cache_timeout: 600,
            source: ''
        },
        init: function(options){
            self.options = $.extend({}, self.default_options, options);
            self.completion = require('main/completion').make({
                source: self.match
            });
        },
        activated: function(){
            return self.completion.activated();
        },
        activate: function(){
            if (self.activated()) return;
            var timekey = 'yandere_completion_options_time';
            var datakey = 'yandere_completion_options';
            var last_time = $.localStorage(timekey);
            var last_data = $.localStorage(datakey);
            if (last_data && last_time && self.now() - last_time < 1000 * self.options.completion_cache_timeout) {
                self.options.source = last_data.result.data;
                self.activate_();
            } else {
                if (last_data) {
                    self.options.source = last_data.result.data;
                    self.activate_();
                }
                $.ajax({
                    url: self.options.completion_options_uri,
                    type: 'get'
                }).done(function(data){
                    self.options.source = data.result.data;
                    self.activate_();
                    $.localStorage(datakey, data);
                    $.localStorage(timekey, self.now());
                });
            }
        },
        now: function(){
            return (new Date()).getTime();
        },
        activate_: function(){
            return self.completion.activate();
        },
        deactivate: function(){
            return self.completion.deactivate();
        }
    };
    module.exports = {
        init: self.init,
        activate: self.activate,
        deactivate: self.deactivate
    };
});
