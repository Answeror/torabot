define("torabot/yandere/0.1.0/main-debug", [ "./create_tag_search_regex-debug", "./retrieve_tag_search-debug", "./reorder_search_results-debug" ], function(require, exports, module) {
    var self = {
        create_tag_search_regex: require("./create_tag_search_regex-debug"),
        retrieve_tag_search: require("./retrieve_tag_search-debug"),
        reorder_search_results: require("./reorder_search_results-debug"),
        complete_tag: function(tag) {
            var re = self.create_tag_search_regex(tag, {
                gloabl: true
            });
            var main_results = self.retrieve_tag_search(re, self.options.source, {
                max_results: 100
            });
            main_results = self.reorder_search_results(tag, main_results);
            var results = main_results;
            self.bubble_rating_tags(results, tag);
            console.log(results);
        },
        bubble_rating_tags: function(results, tag) {
            /* Hack: if the search is one of the ratings shortcuts, put that at the top, even though
             * it's not a real tag. */
            if ("sqe".indexOf(tag) != -1) results.unshift("0`" + tag + "` ");
        },
        init: function(options) {
            self.options = options;
            self.complete_tag("tou");
        }
    };
    exports.init = self.init;
});

// https://github.com/moebooru/moebooru/blob/0aa622f2fbdb81a19578c999775ce3bbb2fc49b2/lib/assets/javascripts/moe-legacy/tag_completion.js
define("torabot/yandere/0.1.0/create_tag_search_regex-debug", [], function(require, exports, module) {
    modules.exports = function(tag, options) {
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
        letters.each(function(letter) {
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
            letters.each(function(letter) {
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
        results.each(function(tag) {
            if (re.test(tag)) top_results.push(tag); else bottom_results.push(tag);
        });
        return top_results.concat(bottom_results);
    };
});
