define(function(require, exports, module){
    $(function() {
        $.torabot = {};
        $.torabot.cast = function(type, value) {
            return ({
                text: function(x) { return x.toString(); },
                int: parseInt
            })[type](value);
        };
    });
    $(function() {
        $.fn.popup_text_edit = function(options) {
            $(this).editable($.extend({}, {
                type: 'text',
                mode: 'popup',
                url: function(params) {
                    var d = $.Deferred();
                    var $this = $(this);
                    if ($this.data('args')) {
                        var data = $this.data('args');
                    } else {
                        var data = {};
                    }
                    if ($this.data('field')) {
                        var field = $this.data('field');
                    } else {
                        var field = 'value';
                    }
                    data[field] = $.torabot.cast($this.data('kind'), params.value);
                    $.ajax({
                        url: $this.data('uri'),
                        type: 'post',
                        dataType: 'json',
                        contentType: 'application/json',
                        data: JSON.stringify(data)
                    }).done(d.resolve).fail(d.reject);
                    return d;
                },
                error: function(xhr) {
                    new PNotify({
                        text: JSON.parse(xhr.responseText).message.html,
                        type: 'error',
                        icon: false,
                        buttons: {
                            closer: true,
                            sticker: false
                        }
                    });
                }
            }, options || {}));
        }
    });
    $(function(){
        var form = $('form[name="search"]');
        var $q = form.find('input[name="q"]');
        var $mods = form.find('select[name="kind"]');
        form.find('button[name="help"]').click(function(e) {
            e.preventDefault();
            $(location).attr('href', '/help/' + $mods.find('option:selected').val());
        });
        var $search = form.find('button[name="search"]');
        $search.click(function(e) {
            e.preventDefault();
            var $selected = $mods.find('option:selected');
            var kind = $selected.val();
            var text = $q.val();
            if (!text && !$selected.data('allow-empty-query')) {
                new PNotify({
                    text: '查询不能为空',
                    type: 'error',
                    icon: false
                });
                return;
            }
            $(location).attr('href', '/search/' + kind + '?' + $.param({q: text}));
        });
        var $advanced = form.find('button[name="advanced"]');
        $advanced.click(function(e) {
            e.preventDefault();
            $(location).attr('href', '/search/advanced/' + $mods.find('option:selected').val());
        });
        var $buttons = form.find('span[name="buttons"]');
        var on_change_mod = function() {
            var $selected = $(this).find('option:selected');
            $advanced.prop('disabled', !$selected.data('has-advanced-search'));
            $q.prop('disabled', !$selected.data('has-normal-search'));
            $search.prop('disabled', !$selected.data('has-normal-search'));
            if ($selected.data('has-normal-search')) {
                $q.prop('placeholder', $selected.data('normal-search-prompt'));
            } else {
                $q.prop('placeholder', '请使用高级搜索');
            }
        };
        $mods.ready(on_change_mod).change(on_change_mod);
    });
});
