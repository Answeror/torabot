$(function(){
    var form = $('form[name="search"]');
    var $mods = form.find('select[name="torabot_query_kind"]');
    form.find('button[name="help"]').click(function(e) {
        e.preventDefault();
        $(location).attr('href', '/help/' + $mods.find('option:selected').val());
    });
    form.find('button[name="search"]').click(function(e) {
        e.preventDefault();
        form.attr('action', '/search').submit();
    });
    var $advanced = form.find('button[name="advanced"]');
    $advanced.click(function(e) {
        e.preventDefault();
        form.attr('action', '/search/advanced').submit();
    });
    var $buttons = form.find('span[name="buttons"]');
    var on_change_mod = function() {
        if ($(this).find('option:selected').data('has-advanced-search')) {
            $buttons.append($advanced);
        } else {
            $advanced.remove();
        }
    };
    $mods.ready(on_change_mod).change(on_change_mod);
});
