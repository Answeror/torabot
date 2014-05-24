define(function(require, exports, module){
    require('./xeditable/xeditable');
    require('./xeditable/xeditable.css');

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
    $('.editable-field').popup_text_edit();
});
