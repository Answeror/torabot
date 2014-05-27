define(function(require, exports, module){
    require('bootstrap-select.css');
    require('bootstrap-select');
    require('./typeahead.jquery');

    var self = {
        init_select: function(){
            $('.mod-select').selectpicker({
                noneResultsText: '无匹配项'
            });
        },
        init_main: function(){
            self.$form = $('form[name="search"]');
            self.$q = self.$form.find('input[name="q"]');

            self.init_select();

            var $mods = self.$form.find('select[name="kind"]');
            self.$form.find('button[name="help"]').click(function(e) {
                e.preventDefault();
                $(location).attr('href', '/help/' + $mods.find('option:selected').val());
            });
            var $search = self.$form.find('button[name="search"]');
            $search.click(function(e) {
                e.preventDefault();
                var $selected = $mods.find('option:selected');
                var kind = $selected.val();
                var text = self.$q.val();
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
            var $advanced = self.$form.find('button[name="advanced"]');
            $advanced.click(function(e) {
                e.preventDefault();
                $(location).attr('href', '/search/advanced/' + $mods.find('option:selected').val());
            });
            var $buttons = self.$form.find('span[name="buttons"]');
            var on_change_mod = function() {
                var $selected = $(this).find('option:selected');
                $advanced.prop('disabled', !$selected.data('has-advanced-search'));
                self.$q.prop('disabled', !$selected.data('has-normal-search'));
                $search.prop('disabled', !$selected.data('has-normal-search'));
                if ($selected.data('has-normal-search')) {
                    self.$q.prop('placeholder', $selected.data('normal-search-prompt'));
                } else {
                    self.$q.prop('placeholder', '请使用高级搜索');
                }
                if (self.previous_mod) {
                    require.async(self.previous_mod, function(m){
                        m.deactivate();
                    });
                }
                var current_mod = self.get_mod_path($selected.val());
                console.log($selected.val());
                console.log(self.options.mods);
                console.log(current_mod);
                if (current_mod) {
                    require.async(current_mod, function(m){
                        m.activate();
                    });
                }
                self.previous_mod = current_mod;
            };
            $mods.ready(on_change_mod).change(on_change_mod);
        },
        get_mod_path: function(selected){
            for (var i = 0; i < self.options.mods.length; ++i) {
                var mod = self.options.mods[i];
                if (selected == mod || selected + '-debug' == mod) return mod;
            }
        },
        previous_mod: null,
        default_options: {
            mods: []
        },
        init: function(options){
            self.options = $.extend({}, self.default_options, options);
            self.init_main();
        }
    };

    module.exports = self;
});
