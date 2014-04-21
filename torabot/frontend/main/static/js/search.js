$(function(){
    var form = $('form[name="search"]');
    var $mods = form.find('select[name="kind"]');
    form.find('button[name="help"]').click(function(e) {
        e.preventDefault();
        $(location).attr('href', '/help/' + $mods.find('option:selected').val());
    });
    var $search = form.find('button[name="search"]');
    $search.click(function(e) {
        e.preventDefault();
        var kind = $mods.find('option:selected').val();
        var text = form.find('input[name="q"]').val();
        $(location).attr('href', '/search/' + kind + '?' + $.param({q: text}));
    });
    var $advanced = form.find('button[name="advanced"]');
    $advanced.click(function(e) {
        e.preventDefault();
        $(location).attr('href', '/search/advanced/' + $mods.find('option:selected').val());
    });
    var $buttons = form.find('span[name="buttons"]');
    var $q = form.find('input[name="q"]');
    var on_change_mod = function() {
        $advanced.prop('disabled', !$(this).find('option:selected').data('has-advanced-search'));
        $q.prop('disabled', !$(this).find('option:selected').data('has-normal-search'));
        $search.prop('disabled', !$(this).find('option:selected').data('has-normal-search'));
    };
    $mods.ready(on_change_mod).change(on_change_mod);
});
