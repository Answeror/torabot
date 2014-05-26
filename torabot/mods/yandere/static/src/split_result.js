define(function(require, exports, module){
    module.exports = function(results){
/* Strip the "1`" tag type prefix off of each result. */
  var final_results = [];
  var final_aliases = [];
  $.map(results, function(tag) {
    var m = tag.match(/(\d+)`([^`]*)`(([^ ]*)`)? /);
    if(!m)
    {
      ReportError("Unparsable cached tag: '" + tag + "'", null, null, null, null);
      throw "Unparsable cached tag: '" + tag + "'";
    }

    var tag = m[2];
    var aliases = m[4];
    if(m[4])
      aliases = aliases.split("`");
    else
      aliases = [];

    if(final_results.indexOf(tag) == -1)
    {
      final_results.push(tag);
      final_aliases.push(aliases);
    }
  });
        return [final_results, final_aliases];
    };
});
