define(function(require, exports, module){
    require('./init');
    var self = {
        $watch_form: $('#watch-form'),
        show_name_watch_dialog: function(email_id){
            var $d = $.Deferred();
            var $dialog = $('#name-watch-dialog');
            var submit = function(){
                $.ajax({
                    url: self.options.watch_uri,
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        user_id: self.options.current_user_id,
                        email_id: email_id,
                        query_id: self.options.query_id,
                        name: $dialog.find('[name="name"]').val()
                    })
                }).done(function(){
                    new PNotify({
                        text: '订阅成功',
                        type: 'success',
                        icon: false,
                    });
                    self.switch(email_id, true, true);
                    $dialog.modal('hide');
                }).done($d.resolve).fail(function(xhr){
                    new PNotify({
                        text: JSON.parse(xhr.responseText).message.html,
                        type: 'error',
                        icon: false,
                    });
                }).fail($d.reject);
            };
            $dialog.find('[name="confirm"]').off('click').click(function(e){
                e.preventDefault();
                submit();
            });
            $dialog.find('form').off('submit').submit(function(e){
                e.preventDefault();
                submit();
            });
            $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function(e){
                $d.reject();
            }).modal('show');
            return $d.promise();
        },
        unwatch: function(email_id){
            var $d = $.Deferred();
            $.ajax({
                url: self.options.unwatch_uri,
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    user_id: self.options.current_user_id,
                    email_id: email_id,
                    query_id: self.options.query_id
                })
            }).done(function(){
                new PNotify({
                    text: '退订成功',
                    type: 'success',
                    icon: false,
                });
                self.switch(email_id, false, true);
            }).done($d.resolve).fail(function(xhr){
                new PNotify({
                    text: JSON.parse(xhr.responseText).message.html,
                    type: 'error',
                    icon: false,
                });
            }).fail($d.reject);
            return $d.promise();
        },
        bind: function(){
            self.$watch_form.find('.btn.watch').off('click').click(function(e){
                e.preventDefault();
                self.show_name_watch_dialog(self.options.email_id).done(self.show_unwatch_button);
            });
            self.$watch_form.find('.btn.unwatch').off('click').click(function(e){
                e.preventDefault();
                self.unwatch(self.options.email_id).done(self.show_watch_button);
            });
        },
        show_watch_button: function(){
            self.$watch_form.find('[type="submit"]')
                .removeClass('btn-danger')
                .addClass('btn-primary')
                .removeClass('unwatch')
                .addClass('watch')
                .text('订阅');
            self.$watch_form.find('.dropdown-toggle')
                .removeClass('btn-danger')
                .addClass('btn-primary');
            self.bind();
        },
        show_unwatch_button: function(){
            self.$watch_form.find('[type="submit"]')
                .removeClass('btn-primary')
                .addClass('btn-danger')
                .removeClass('watch')
                .addClass('unwatch')
                .text('退订');
            self.$watch_form.find('.dropdown-toggle')
                .removeClass('btn-primary')
                .addClass('btn-danger');
            self.bind();
        },
        switch: function(email_id, state, skip){
            self.$watch_form.find('.dropdown-menu [name="switch-' + email_id + '"]').bootstrapSwitch('state', state, skip);
        },
        init_switch: function(){
            $('.switch').bootstrapSwitch({
                onSwitchChange: function(e, state){
                    var $this = $(this);
                    var email_id = $this.data('email-id');
                    var $d;
                    if (state) {
                        $d = self.show_name_watch_dialog(email_id);
                    } else {
                        $d = self.unwatch(email_id);
                    }
                    $d.done(function(){
                        if (email_id == self.options.email_id) {
                            if (state) {
                                self.show_unwatch_button();
                            } else {
                                self.show_watch_button();
                            }
                        }
                    }).fail(function(){
                        $this.bootstrapSwitch('state', !state, true);
                    });
                }
            });
            $('.email-switch').click(function(e) {
                e.stopPropagation();
            });
        },
        init: function(options){
            self.options = options;
            self.bind();
            self.init_switch();
        }
    };
    exports.init = self.init;
});
