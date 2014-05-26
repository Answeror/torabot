define(function(require, exports, module){
    /*
     * Contents matches (t*g*m -> tagme) are lower priority than other results.  Within
     * each search type (recent and main), sort them to the bottom.
     */
    module.exports = function(tag, results)
    {
      var re = require('./create_tag_search_regex')(tag, { top_results_only: true, global: false });
      var top_results = [];
      var bottom_results = [];

      $.map(results, function(tag) {
        if(re.test(tag))
          top_results.push(tag);
        else
          bottom_results.push(tag);
      });
      return top_results.concat(bottom_results);
    }
});
