define(function(require, exports, module){
    require('bootstrap-select.css');
    require('bootstrap-select');
    require('./typeahead.jquery');

    var self = {
        init_select: function(){
            $('.mod-select').selectpicker({
                noneResultsText: '无匹配项'
            });
            self.$mod_select_wrap.animate({'margin-left': '0'});
        },
        init_main: function(){
            self.$form = $('form[name="search"]');
            self.$q = self.$form.find('input[name="q"]');
            self.$query_wrap = self.$form.find('.query-wrap');
            self.$mods = self.$form.find('select[name="kind"]');
            self.$mod_select_wrap = self.$form.find('.mod-select-wrap');

            self.init_select();

            self.$form.find('button[name="help"]').click(function(e) {
                e.preventDefault();
                $(location).attr('href', '/help/' + self.$mods.find('option:selected').val());
            });
            var $search = self.$form.find('button[name="search"]');
            $search.click(function(e) {
                e.preventDefault();
                var kind = self.$selected().val();
                var text = self.$q.val();
                if (!text && !self.$selected().data('allow-empty-query')) {
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
                $(location).attr('href', '/search/advanced/' + self.$selected().val());
            });
            var $buttons = self.$form.find('span[name="buttons"]');
            var on_change_mod = function() {
                var $selected = $(this).find('option:selected');
                $advanced.prop('disabled', !$selected.data('has-advanced-search'));
                var $d = $.Deferred();
                if ($selected.data('has-normal-search')) {
                    self.$q
                        .prop('placeholder', $selected.data('normal-search-prompt'))
                        .prop('disabled', false)
                        .animate({'margin-left': '0'}, {
                            done: function(){
                                self.$query_wrap.css('overflow', 'inherit');
                                $d.resolve();
                            }
                        });
                    $search.prop('disabled', false).show();
                } else {
                    self.$query_wrap.css('overflow', 'hidden');
                    self.$q
                        .prop('placeholder', '请使用高级搜索')
                        .prop('disabled', true)
                        .animate({'margin-left': '-194px'}, {
                            done: $d.resolve
                        });
                    $search.prop('disabled', true).hide();
                }
                self.deactivate_previous_mod();
                $d.done(self.activate_current_mod);
            };
            self.$mods.ready(on_change_mod).change(on_change_mod);
        },
        $selected: function(){
            return self.$mods.find('option:selected');
        },
        activate_current_mod: function(){
            var current_mod = self.get_mod_path(self.$selected().val());
            if (current_mod) {
                require.async(current_mod, function(m){
                    m.activate();
                });
            }
            self.previous_mod = current_mod;
        },
        deactivate_previous_mod: function() {
            if (self.previous_mod) {
                require.async(self.previous_mod, function(m){
                    m.deactivate();
                });
            }
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
