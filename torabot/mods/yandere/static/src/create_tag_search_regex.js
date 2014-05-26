// https://github.com/moebooru/moebooru/blob/0aa622f2fbdb81a19578c999775ce3bbb2fc49b2/lib/assets/javascripts/moe-legacy/tag_completion.js
define(function(require, exports, module){
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
        if(tag.indexOf("_") != -1)
        {
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
        if(!options.top_results_only)
        {
            var s = "(";
            $.map(letters, function(letter) {
                var escaped_letter = RegExp.escape(letter);
                s += escaped_letter;
                s += '[^`]*';
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

        return new RegExp(regex_string, options.global? "g":"");
    };
});
