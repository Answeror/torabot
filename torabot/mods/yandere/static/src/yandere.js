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
            var ret = self.complete_tag(q);
            cb($.map(ret[0], function(r){ return {value: r}; }));
        },
        init: function(options){
            self.options = options;
            require('main/search').$q.typeahead({
                hint: true,
                highlight: true,
                minLength: 1
            }, {
                name: 'yandere',
                displayKey: 'value',
                source: self.match
            });
        }
    };
    exports.init = self.init;
});
