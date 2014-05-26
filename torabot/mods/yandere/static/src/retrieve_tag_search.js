define(function(require, exports, module){
    module.exports = function(re, source, options){
      var results = [];

      var max_results = 10;
      if(options.max_results != null)
        max_results = options.max_results;

      while(results.length < max_results)
      {
        var m = re.exec(source);
        if(!m)
          break;

        var tag = m[0];
        /* Ignore this tag.  We need a better way to blackhole tags. */
        if(tag.indexOf(":deletethistag:") != -1)
          continue;
        if(results.indexOf(tag) == -1)
          results.push(tag);
      }
      return results;
    };
});
