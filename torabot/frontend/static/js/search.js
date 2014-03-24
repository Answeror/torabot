$(function(){
    var form = $('form[name="search"]');
    form.find('button[name="help"]').click(function(e) {
        e.preventDefault();
    });
    form.find('button[name="search"]').click(function(e) {
        e.preventDefault();
        form.attr('action', '/search').submit();
    });
    form.find('button[name="advanced"]').click(function(e) {
        e.preventDefault();
        form.attr('action', '/search/advanced').submit();
    });
});
