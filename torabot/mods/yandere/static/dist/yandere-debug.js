define("torabot/yandere/0.1.0/yandere-debug", [ "./create_tag_search_regex-debug", "./retrieve_tag_search-debug", "./reorder_search_results-debug", "./split_result-debug", "main/ut-debug", "main/search-debug", "main/handlebars-v1.3.0-debug" ], function(require, exports, module) {
    var self = {
        create_tag_search_regex: require("./create_tag_search_regex-debug"),
        retrieve_tag_search: require("./retrieve_tag_search-debug"),
        reorder_search_results: require("./reorder_search_results-debug"),
        split_result: require("./split_result-debug"),
        complete_tag: function(tag) {
            var re = self.create_tag_search_regex(tag, {
                global: true
            });
            var main_results = self.retrieve_tag_search(re, self.options.source, {
                max_results: 100
            });
            main_results = self.reorder_search_results(tag, main_results);
            var results = main_results;
            self.bubble_rating_tags(results, tag);
            results = results.slice(0, self.options.max_results != null ? self.options.max_results : 10);
            return self.split_result(results);
        },
        bubble_rating_tags: function(results, tag) {
            /* Hack: if the search is one of the ratings shortcuts, put that at the top, even though
             * it's not a real tag. */
            if ("sqe".indexOf(tag) != -1) results.unshift("0`" + tag + "` ");
        },
        match: function(q, cb) {
            var tag = q.split(" ").slice(-1)[0];
            if (tag) {
                var ret = self.complete_tag(tag);
                cb($.map(require("main/ut-debug").zip(ret[0], ret[1]), function(args) {
                    return {
                        value: args[0],
                        alias: args[1].map(function(x) {
                            return {
                                value: x
                            };
                        })
                    };
                }));
            }
        },
        init: function(options) {
            self.options = options;
        },
        activate: function() {
            var last_query = null;
            var update_query = function(suggestion, options) {
                options = $.extend({
                    query: null,
                    set: function(value) {
                        return require("main/search-debug").$q.val(value);
                    }
                }, options);
                var query = options.query;
                if (!query) {
                    last_query = query = require("main/search-debug").$q.typeahead("val");
                }
                var tags = query.split(" ").slice(0, -1);
                tags.push(suggestion.value);
                return options.set(tags.join(" "));
            };
            require("main/search-debug").$q.typeahead({
                hint: true,
                highlight: true,
                minLength: 1
            }, {
                name: "yandere",
                displayKey: "value",
                source: self.match,
                templates: {
                    suggestion: require("main/handlebars-v1.3.0-debug").compile([ "<p class=completion-item>", "<strong class=ellipsis>{{value}}</strong>", "{{#if alias}}<br>{{#each alias}}<span class='ellipsis label label-default'>{{value}}</span> {{/each}}{{/if}}", "</p>" ].join(""))
                }
            }).on("typeahead:cursorchanged", function(e, suggestion, dataset) {
                update_query(suggestion);
                e.preventDefault();
            }).on("typeahead:selected", function(e, suggestion, dataset) {
                var $this = $(this);
                update_query(suggestion, {
                    query: last_query,
                    set: function(value) {
                        return $this.typeahead("val", value);
                    }
                });
                e.preventDefault();
            });
        },
        deactivate: function() {
            require("main/search-debug").$q.typeahead("destroy");
        }
    };
    module.exports = {
        init: self.init,
        activate: self.activate,
        deactivate: self.deactivate
    };
});

// https://github.com/moebooru/moebooru/blob/0aa622f2fbdb81a19578c999775ce3bbb2fc49b2/lib/assets/javascripts/moe-legacy/tag_completion.js
define("torabot/yandere/0.1.0/create_tag_search_regex-debug", [], function(require, exports, module) {
    module.exports = function(tag, options) {
        /* Split the tag by character. */
        var letters = tag.split("");
        /*
         * We can do a few search methods:
         *
         * 1: Ordinary prefix search.
         * 2: Name search. "aaa_bbb" -> "aaa*_bbb*|bbb*_aaa*".
         * 3: Contents search; "tgm" -> "t*g*m*" -> "tagme".  The first character is still always
         * matched exactly.
         *
         * Avoid running multiple expressions.  Instead, combine these into a single one, then run
         * each part on the results to determine which type of result it is.  Always show prefix and
         * name results before contents results.
         */
        var regex_parts = [];
        /* Allow basic word prefix matches.  "tag" matches at the beginning of any word
         * in a tag, eg. both "tagme" and "dont_tagme". */
        /* Add the regex for ordinary prefix matches. */
        var s = "(([^`]*_)?";
        $.map(letters, function(letter) {
            var escaped_letter = RegExp.escape(letter);
            s += escaped_letter;
        });
        s += ")";
        regex_parts.push(s);
        /* Allow "fir_las" to match both "first_last" and "last_first". */
        if (tag.indexOf("_") != -1) {
            var first = tag.split("_", 1)[0];
            var last = tag.slice(first.length + 1);
            first = RegExp.escape(first);
            last = RegExp.escape(last);
            var s = "(";
            s += "(" + first + "[^`]*_" + last + ")";
            s += "|";
            s += "(" + last + "[^`]*_" + first + ")";
            s += ")";
            regex_parts.push(s);
        }
        /* Allow "tgm" to match "tagme".  If top_results_only is set, we only want primary results,
         * so omit this match. */
        if (!options.top_results_only) {
            var s = "(";
            $.map(letters, function(letter) {
                var escaped_letter = RegExp.escape(letter);
                s += escaped_letter;
                s += "[^`]*";
            });
            s += ")";
            regex_parts.push(s);
        }
        /* The space is included in the result, so the result tags can be matched with the
         * same regexes, for in reorder_search_results.
         *
         * (\d)+  match the alias ID                      1`
         * [^ ]*: start at the beginning of any alias     1`foo`bar`
         * ... match ...
         * [^`]*` all matches are prefix matches          1`foo`bar`tagme`
         * [^ ]*  match any remaining aliases             1`foo`bar`tagme`tag_me`
         */
        var regex_string = regex_parts.join("|");
        regex_string = "(\\d+)[^ ]*`(" + regex_string + ")[^`]*`[^ ]* ";
        return new RegExp(regex_string, options.global ? "g" : "");
    };
});

define("torabot/yandere/0.1.0/retrieve_tag_search-debug", [], function(require, exports, module) {
    module.exports = function(re, source, options) {
        var results = [];
        var max_results = 10;
        if (options.max_results != null) max_results = options.max_results;
        while (results.length < max_results) {
            var m = re.exec(source);
            if (!m) break;
            var tag = m[0];
            /* Ignore this tag.  We need a better way to blackhole tags. */
            if (tag.indexOf(":deletethistag:") != -1) continue;
            if (results.indexOf(tag) == -1) results.push(tag);
        }
        return results;
    };
});

define("torabot/yandere/0.1.0/reorder_search_results-debug", [ "torabot/yandere/0.1.0/create_tag_search_regex-debug" ], function(require, exports, module) {
    /*
     * Contents matches (t*g*m -> tagme) are lower priority than other results.  Within
     * each search type (recent and main), sort them to the bottom.
     */
    module.exports = function(tag, results) {
        var re = require("torabot/yandere/0.1.0/create_tag_search_regex-debug")(tag, {
            top_results_only: true,
            global: false
        });
        var top_results = [];
        var bottom_results = [];
        $.map(results, function(tag) {
            if (re.test(tag)) top_results.push(tag); else bottom_results.push(tag);
        });
        return top_results.concat(bottom_results);
    };
});

define("torabot/yandere/0.1.0/split_result-debug", [], function(require, exports, module) {
    module.exports = function(results) {
        /* Strip the "1`" tag type prefix off of each result. */
        var final_results = [];
        var final_aliases = [];
        $.map(results, function(tag) {
            var m = tag.match(/(\d+)`([^`]*)`(([^ ]*)`)? /);
            if (!m) {
                ReportError("Unparsable cached tag: '" + tag + "'", null, null, null, null);
                throw "Unparsable cached tag: '" + tag + "'";
            }
            var tag = m[2];
            var aliases = m[4];
            if (m[4]) aliases = aliases.split("`"); else aliases = [];
            if (final_results.indexOf(tag) == -1) {
                final_results.push(tag);
                final_aliases.push(aliases);
            }
        });
        return [ final_results, final_aliases ];
    };
});
