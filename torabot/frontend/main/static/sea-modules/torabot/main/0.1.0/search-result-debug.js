define("torabot/main/0.1.0/search-result-debug", [ "./init-debug", "seajs/seajs-style/1.0.2/seajs-style-debug", "./ut-debug", "./bulletin-debug", "arale/cookie/1.0.2/cookie-debug", "./completion-debug", "./search-debug", "silviomoreto-bootstrap-select-0e1b27a/bootstrap-select-debug", "./typeahead.jquery-debug", "./handlebars-v1.3.0-debug", "./moment-debug", "./moment/moment-debug", "./moment/lang/zh-cn-debug", "./pnotify.custom.min-debug", "./switch-debug", "./bootstrap-switch/bootstrap-switch-debug", "./xeditable-debug", "./xeditable/xeditable-debug", "./xeditable/xeditable-debug.css", "./jquery.storage-debug" ], function(require, exports, module) {
    require("./init-debug");
    var self = {
        $watch_form: $("#watch-form"),
        show_name_watch_dialog: function(email_id) {
            var $d = $.Deferred();
            var $dialog = $("#name-watch-dialog");
            var submit = function() {
                $.ajax({
                    url: self.options.watch_uri,
                    type: "post",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        user_id: self.options.current_user_id,
                        email_id: email_id,
                        query_id: self.options.query_id,
                        name: $dialog.find('[name="name"]').val()
                    })
                }).done(function() {
                    new PNotify({
                        text: "订阅成功",
                        type: "success",
                        icon: false
                    });
                    self.switch(email_id, true, true);
                    $dialog.modal("hide");
                }).done($d.resolve).fail(function(xhr) {
                    new PNotify({
                        text: JSON.parse(xhr.responseText).message.html,
                        type: "error",
                        icon: false
                    });
                }).fail($d.reject);
            };
            $dialog.find('[name="confirm"]').off("click").click(function(e) {
                e.preventDefault();
                submit();
            });
            $dialog.find("form").off("submit").submit(function(e) {
                e.preventDefault();
                submit();
            });
            $dialog.off("hidden.bs.modal").on("hidden.bs.modal", function(e) {
                $d.reject();
            }).modal("show");
            return $d.promise();
        },
        unwatch: function(email_id) {
            var $d = $.Deferred();
            $.ajax({
                url: self.options.unwatch_uri,
                type: "post",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    user_id: self.options.current_user_id,
                    email_id: email_id,
                    query_id: self.options.query_id
                })
            }).done(function() {
                new PNotify({
                    text: "退订成功",
                    type: "success",
                    icon: false
                });
                self.switch(email_id, false, true);
            }).done($d.resolve).fail(function(xhr) {
                new PNotify({
                    text: JSON.parse(xhr.responseText).message.html,
                    type: "error",
                    icon: false
                });
            }).fail($d.reject);
            return $d.promise();
        },
        bind: function() {
            self.$watch_form.find(".btn.watch").off("click").click(function(e) {
                e.preventDefault();
                self.show_name_watch_dialog(self.options.email_id).done(self.show_unwatch_button);
            });
            self.$watch_form.find(".btn.unwatch").off("click").click(function(e) {
                e.preventDefault();
                self.unwatch(self.options.email_id).done(self.show_watch_button);
            });
        },
        show_watch_button: function() {
            self.$watch_form.find('[type="submit"]').removeClass("btn-danger").addClass("btn-primary").removeClass("unwatch").addClass("watch").text("订阅");
            self.$watch_form.find(".dropdown-toggle").removeClass("btn-danger").addClass("btn-primary");
            self.bind();
        },
        show_unwatch_button: function() {
            self.$watch_form.find('[type="submit"]').removeClass("btn-primary").addClass("btn-danger").removeClass("watch").addClass("unwatch").text("退订");
            self.$watch_form.find(".dropdown-toggle").removeClass("btn-primary").addClass("btn-danger");
            self.bind();
        },
        "switch": function(email_id, state, skip) {
            self.$watch_form.find('.dropdown-menu [name="switch-' + email_id + '"]').bootstrapSwitch("state", state, skip);
        },
        init_switch: function() {
            $(".switch").bootstrapSwitch({
                onSwitchChange: function(e, state) {
                    var $this = $(this);
                    var email_id = $this.data("email-id");
                    var $d;
                    if (state) {
                        $d = self.show_name_watch_dialog(email_id);
                    } else {
                        $d = self.unwatch(email_id);
                    }
                    $d.done(function() {
                        if (email_id == self.options.email_id) {
                            if (state) {
                                self.show_unwatch_button();
                            } else {
                                self.show_watch_button();
                            }
                        }
                    }).fail(function() {
                        $this.bootstrapSwitch("state", !state, true);
                    });
                }
            });
            $(".email-switch").click(function(e) {
                e.stopPropagation();
            });
        },
        init: function(options) {
            self.options = options;
            self.bind();
            self.init_switch();
        }
    };
    exports.init = self.init;
});

define("torabot/main/0.1.0/init-debug", [ "seajs/seajs-style/1.0.2/seajs-style-debug", "torabot/main/0.1.0/ut-debug", "torabot/main/0.1.0/bulletin-debug", "arale/cookie/1.0.2/cookie-debug", "torabot/main/0.1.0/completion-debug", "torabot/main/0.1.0/search-debug", "silviomoreto-bootstrap-select-0e1b27a/bootstrap-select-debug", "torabot/main/0.1.0/typeahead.jquery-debug", "torabot/main/0.1.0/handlebars-v1.3.0-debug", "torabot/main/0.1.0/moment-debug", "torabot/main/0.1.0/moment/moment-debug", "torabot/main/0.1.0/moment/lang/zh-cn-debug", "torabot/main/0.1.0/pnotify.custom.min-debug", "torabot/main/0.1.0/switch-debug", "torabot/main/0.1.0/bootstrap-switch/bootstrap-switch-debug", "torabot/main/0.1.0/xeditable-debug", "torabot/main/0.1.0/xeditable/xeditable-debug", "torabot/main/0.1.0/jquery.storage-debug" ], function(require, exports, module) {
    require("seajs/seajs-style/1.0.2/seajs-style-debug");
    require("torabot/main/0.1.0/ut-debug");
    require("torabot/main/0.1.0/bulletin-debug");
    require("torabot/main/0.1.0/completion-debug");
    require("torabot/main/0.1.0/moment-debug");
    require("torabot/main/0.1.0/pnotify.custom.min-debug");
    require("torabot/main/0.1.0/switch-debug");
    require("torabot/main/0.1.0/xeditable-debug");
    require("torabot/main/0.1.0/jquery.storage-debug");
    require("torabot/main/0.1.0/handlebars-v1.3.0-debug");
    var self = {
        default_options: {
            mods: []
        },
        init_mods: function() {
            var $d = $.Deferred();
            var done = [];
            if (self.options.mods.length) {
                $.map(self.options.mods, function(mod) {
                    require.async(mod.name, function(m) {
                        m.init(mod.options);
                        done.push(mod.name);
                        if (done.length == self.options.mods.length) {
                            self.init_search(done);
                        }
                    });
                });
            }
        },
        init_search: function(mods) {
            require("torabot/main/0.1.0/search-debug").init({
                mods: mods
            });
        },
        init: function(options) {
            self.options = $.extend({}, self.default_options, options);
            self.init_mods();
        }
    };
    exports.init = self.init;
});

(function() {
    /**
 * The Sea.js plugin for embedding style text in JavaScript code
 */
    var RE_NON_WORD = /\W/g;
    var doc = document;
    var head = document.getElementsByTagName("head")[0] || document.documentElement;
    var styleNode;
    seajs.importStyle = function(cssText, id) {
        if (id) {
            // Convert id to valid string
            id = id.replace(RE_NON_WORD, "-");
            // Don't add multiple times
            if (doc.getElementById(id)) return;
        }
        var element;
        // Don't share styleNode when id is spectied
        if (!styleNode || id) {
            element = doc.createElement("style");
            id && (element.id = id);
            // Adds to DOM first to avoid the css hack invalid
            head.appendChild(element);
        } else {
            element = styleNode;
        }
        // IE
        if (element.styleSheet) {
            // http://support.microsoft.com/kb/262161
            if (doc.getElementsByTagName("style").length > 31) {
                throw new Error("Exceed the maximal count of style tags in IE");
            }
            element.styleSheet.cssText += cssText;
        } else {
            element.appendChild(doc.createTextNode(cssText));
        }
        if (!id) {
            styleNode = element;
        }
    };
    define("seajs/seajs-style/1.0.2/seajs-style-debug", [], {});
})();

define("torabot/main/0.1.0/ut-debug", [], function(require, exports, module) {
    // http://stackoverflow.com/a/5890983/238472
    Object.defineProperty(Object.prototype, "contains", {
        value: function(o) {
            return this.indexOf(o) != -1;
        },
        enumerable: false
    });
    RegExp.escape = function(str) {
        return String(str).replace(/([.*+?^=!:${}()|[\]\/\\])/g, "\\(");
    };
    $.torabot = {};
    $.torabot.cast = function(type, value) {
        return {
            text: function(x) {
                return x.toString();
            },
            "int": parseInt
        }[type](value);
    };
    exports.zip = function() {
        var args = [].slice.call(arguments);
        var shortest = args.length == 0 ? [] : args.reduce(function(a, b) {
            return a.length < b.length ? a : b;
        });
        return shortest.map(function(_, i) {
            return args.map(function(array) {
                return array[i];
            });
        });
    };
});

define("torabot/main/0.1.0/bulletin-debug", [ "arale/cookie/1.0.2/cookie-debug" ], function(require, exports, module) {
    Cookie = require("arale/cookie/1.0.2/cookie-debug");
    $(".bulletin").bind("closed.bs.alert", function() {
        Cookie.set("hide_bulletin_id", $('.bulletin *[name="id"]').prop("value"), {
            path: "/"
        });
    });
});

define("arale/cookie/1.0.2/cookie-debug", [], function(require, exports) {
    // Cookie
    // -------------
    // Thanks to:
    //  - http://www.nczonline.net/blog/2009/05/05/http-cookies-explained/
    //  - http://developer.yahoo.com/yui/3/cookie/
    var Cookie = exports;
    var decode = decodeURIComponent;
    var encode = encodeURIComponent;
    /**
     * Returns the cookie value for the given name.
     *
     * @param {String} name The name of the cookie to retrieve.
     *
     * @param {Function|Object} options (Optional) An object containing one or
     *     more cookie options: raw (true/false) and converter (a function).
     *     The converter function is run on the value before returning it. The
     *     function is not used if the cookie doesn't exist. The function can be
     *     passed instead of the options object for conveniently. When raw is
     *     set to true, the cookie value is not URI decoded.
     *
     * @return {*} If no converter is specified, returns a string or undefined
     *     if the cookie doesn't exist. If the converter is specified, returns
     *     the value returned from the converter.
     */
    Cookie.get = function(name, options) {
        validateCookieName(name);
        if (typeof options === "function") {
            options = {
                converter: options
            };
        } else {
            options = options || {};
        }
        var cookies = parseCookieString(document.cookie, !options["raw"]);
        return (options.converter || same)(cookies[name]);
    };
    /**
     * Sets a cookie with a given name and value.
     *
     * @param {string} name The name of the cookie to set.
     *
     * @param {*} value The value to set for the cookie.
     *
     * @param {Object} options (Optional) An object containing one or more
     *     cookie options: path (a string), domain (a string),
     *     expires (number or a Date object), secure (true/false),
     *     and raw (true/false). Setting raw to true indicates that the cookie
     *     should not be URI encoded before being set.
     *
     * @return {string} The created cookie string.
     */
    Cookie.set = function(name, value, options) {
        validateCookieName(name);
        options = options || {};
        var expires = options["expires"];
        var domain = options["domain"];
        var path = options["path"];
        if (!options["raw"]) {
            value = encode(String(value));
        }
        var text = name + "=" + value;
        // expires
        var date = expires;
        if (typeof date === "number") {
            date = new Date();
            date.setDate(date.getDate() + expires);
        }
        if (date instanceof Date) {
            text += "; expires=" + date.toUTCString();
        }
        // domain
        if (isNonEmptyString(domain)) {
            text += "; domain=" + domain;
        }
        // path
        if (isNonEmptyString(path)) {
            text += "; path=" + path;
        }
        // secure
        if (options["secure"]) {
            text += "; secure";
        }
        document.cookie = text;
        return text;
    };
    /**
     * Removes a cookie from the machine by setting its expiration date to
     * sometime in the past.
     *
     * @param {string} name The name of the cookie to remove.
     *
     * @param {Object} options (Optional) An object containing one or more
     *     cookie options: path (a string), domain (a string),
     *     and secure (true/false). The expires option will be overwritten
     *     by the method.
     *
     * @return {string} The created cookie string.
     */
    Cookie.remove = function(name, options) {
        options = options || {};
        options["expires"] = new Date(0);
        return this.set(name, "", options);
    };
    function parseCookieString(text, shouldDecode) {
        var cookies = {};
        if (isString(text) && text.length > 0) {
            var decodeValue = shouldDecode ? decode : same;
            var cookieParts = text.split(/;\s/g);
            var cookieName;
            var cookieValue;
            var cookieNameValue;
            for (var i = 0, len = cookieParts.length; i < len; i++) {
                // Check for normally-formatted cookie (name-value)
                cookieNameValue = cookieParts[i].match(/([^=]+)=/i);
                if (cookieNameValue instanceof Array) {
                    try {
                        cookieName = decode(cookieNameValue[1]);
                        cookieValue = decodeValue(cookieParts[i].substring(cookieNameValue[1].length + 1));
                    } catch (ex) {}
                } else {
                    // Means the cookie does not have an "=", so treat it as
                    // a boolean flag
                    cookieName = decode(cookieParts[i]);
                    cookieValue = "";
                }
                if (cookieName) {
                    cookies[cookieName] = cookieValue;
                }
            }
        }
        return cookies;
    }
    // Helpers
    function isString(o) {
        return typeof o === "string";
    }
    function isNonEmptyString(s) {
        return isString(s) && s !== "";
    }
    function validateCookieName(name) {
        if (!isNonEmptyString(name)) {
            throw new TypeError("Cookie name must be a non-empty string");
        }
    }
    function same(s) {
        return s;
    }
});

define("torabot/main/0.1.0/completion-debug", [ "torabot/main/0.1.0/search-debug", "silviomoreto-bootstrap-select-0e1b27a/bootstrap-select-debug", "torabot/main/0.1.0/typeahead.jquery-debug", "torabot/main/0.1.0/handlebars-v1.3.0-debug" ], function(require, exports, module) {
    exports.make = function(options) {
        options = $.extend({
            source: null
        }, options);
        var self = {
            _activated: false,
            activated: function() {
                return self._activated;
            },
            activate: function() {
                if (self._activated) return;
                var last_query = null;
                var update_query = function(suggestion, options) {
                    options = $.extend({
                        query: null,
                        set: function(value) {
                            return require("torabot/main/0.1.0/search-debug").$q.val(value);
                        }
                    }, options);
                    var query = options.query;
                    if (!query) {
                        last_query = query = require("torabot/main/0.1.0/search-debug").$q.typeahead("val");
                    }
                    var tags = query.split(" ").slice(0, -1);
                    tags.push(suggestion.value);
                    return options.set(tags.join(" "));
                };
                require("torabot/main/0.1.0/search-debug").$q.typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1
                }, {
                    name: "completion",
                    displayKey: "value",
                    source: options.source,
                    templates: {
                        suggestion: require("torabot/main/0.1.0/handlebars-v1.3.0-debug").compile([ "<p class=completion-item>", "<strong class=ellipsis>{{value}}</strong>", "{{#if alias}}<br>{{#each alias}}<span class='ellipsis label label-default'>{{value}}</span> {{/each}}{{/if}}", "</p>" ].join(""))
                    }
                }).on("typeahead:cursorchanged", function(e, suggestion, dataset) {
                    update_query(suggestion);
                    e.preventDefault();
                }).on("typeahead:selected", function(e, suggestion, dataset) {
                    var $this = $(this);
                    update_query(suggestion, {
                        query: last_query,
                        set: function(value) {
                            return $this.typeahead("val", value);
                        }
                    });
                    e.preventDefault();
                });
                self._activated = true;
            },
            deactivate: function() {
                if (!self._activated) return;
                require("torabot/main/0.1.0/search-debug").$q.typeahead("destroy");
                self._activated = false;
            }
        };
        return self;
    };
});

define("torabot/main/0.1.0/search-debug", [ "silviomoreto-bootstrap-select-0e1b27a/bootstrap-select-debug", "torabot/main/0.1.0/typeahead.jquery-debug" ], function(require, exports, module) {
    require("silviomoreto-bootstrap-select-0e1b27a/bootstrap-select-debug.css");
    require("silviomoreto-bootstrap-select-0e1b27a/bootstrap-select-debug");
    require("torabot/main/0.1.0/typeahead.jquery-debug");
    var self = {
        init_select: function() {
            $(".mod-select").selectpicker({
                noneResultsText: "无匹配项"
            });
        },
        init_main: function() {
            self.$form = $('form[name="search"]');
            self.$q = self.$form.find('input[name="q"]');
            self.$query_wrap = self.$form.find(".query-wrap");
            self.$mods = self.$form.find('select[name="kind"]');
            self.init_select();
            self.$form.find('button[name="help"]').click(function(e) {
                e.preventDefault();
                $(location).attr("href", "/help/" + self.$mods.find("option:selected").val());
            });
            var $search = self.$form.find('button[name="search"]');
            $search.click(function(e) {
                e.preventDefault();
                var kind = self.$selected().val();
                var text = self.$q.val();
                if (!text && !self.$selected().data("allow-empty-query")) {
                    new PNotify({
                        text: "查询不能为空",
                        type: "error",
                        icon: false
                    });
                    return;
                }
                $(location).attr("href", "/search/" + kind + "?" + $.param({
                    q: text
                }));
            });
            var $advanced = self.$form.find('button[name="advanced"]');
            $advanced.click(function(e) {
                e.preventDefault();
                $(location).attr("href", "/search/advanced/" + self.$selected().val());
            });
            var $buttons = self.$form.find('span[name="buttons"]');
            var on_change_mod = function() {
                var $selected = $(this).find("option:selected");
                $advanced.prop("disabled", !$selected.data("has-advanced-search"));
                var $d = $.Deferred();
                if ($selected.data("has-normal-search")) {
                    self.$q.prop("placeholder", $selected.data("normal-search-prompt")).prop("disabled", false).animate({
                        "margin-left": "0"
                    }, {
                        done: function() {
                            self.$query_wrap.css("overflow", "inherit");
                            $d.resolve();
                        }
                    });
                    $search.prop("disabled", false).show();
                } else {
                    self.$query_wrap.css("overflow", "hidden");
                    self.$q.prop("placeholder", "请使用高级搜索").prop("disabled", true).animate({
                        "margin-left": "-194px"
                    }, {
                        done: $d.resolve
                    });
                    $search.prop("disabled", true).hide();
                }
                self.deactivate_previous_mod();
                $d.done(self.activate_current_mod);
            };
            self.$mods.ready(on_change_mod).change(on_change_mod);
        },
        $selected: function() {
            return self.$mods.find("option:selected");
        },
        activate_current_mod: function() {
            var current_mod = self.get_mod_path(self.$selected().val());
            if (current_mod) {
                require.async(current_mod, function(m) {
                    m.activate();
                });
            }
            self.previous_mod = current_mod;
        },
        deactivate_previous_mod: function() {
            if (self.previous_mod) {
                require.async(self.previous_mod, function(m) {
                    m.deactivate();
                });
            }
        },
        get_mod_path: function(selected) {
            for (var i = 0; i < self.options.mods.length; ++i) {
                var mod = self.options.mods[i];
                if (selected == mod || selected + "-debug" == mod) return mod;
            }
        },
        previous_mod: null,
        default_options: {
            mods: []
        },
        init: function(options) {
            self.options = $.extend({}, self.default_options, options);
            self.init_main();
        }
    };
    module.exports = self;
});

define("silviomoreto-bootstrap-select-0e1b27a/bootstrap-select-debug.css", [], function() {
    seajs.importStyle(".bootstrap-select.btn-group:not(.input-group-btn),.bootstrap-select.btn-group[class*=span]{float:none;display:inline-block;margin-bottom:10px;margin-left:0}.form-search .bootstrap-select.btn-group,.form-inline .bootstrap-select.btn-group,.form-horizontal .bootstrap-select.btn-group{margin-bottom:0}.bootstrap-select.form-control{margin-bottom:0;padding:0;border:0}.bootstrap-select.btn-group.pull-right,.bootstrap-select.btn-group[class*=span].pull-right,.row-fluid .bootstrap-select.btn-group[class*=span].pull-right{float:right}.input-append .bootstrap-select.btn-group{margin-left:-1px}.input-prepend .bootstrap-select.btn-group{margin-right:-1px}.bootstrap-select:not([class*=span]):not([class*=col-]):not([class*=form-control]):not(.input-group-btn){width:220px}.bootstrap-select{width:220px\\0}.bootstrap-select.form-control:not([class*=span]){width:100%}.bootstrap-select>.btn{width:100%;padding-right:25px}.error .bootstrap-select .btn{border:1px solid #b94a48}.bootstrap-select.show-menu-arrow.open>.btn{z-index:2051}.bootstrap-select .btn:focus{outline:thin dotted #333!important;outline:5px auto -webkit-focus-ring-color!important;outline-offset:-2px}.bootstrap-select.btn-group .btn .filter-option{display:inline-block;overflow:hidden;width:100%;float:left;text-align:left}.bootstrap-select.btn-group .btn .caret{position:absolute;top:50%;right:12px;margin-top:-2px;vertical-align:middle}.bootstrap-select.btn-group>.disabled,.bootstrap-select.btn-group .dropdown-menu li.disabled>a{cursor:not-allowed}.bootstrap-select.btn-group>.disabled:focus{outline:0!important}.bootstrap-select.btn-group[class*=span] .btn{width:100%}.bootstrap-select.btn-group .dropdown-menu{min-width:100%;z-index:2000;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box}.bootstrap-select.btn-group .dropdown-menu.inner{position:static;border:0;padding:0;margin:0;-webkit-border-radius:0;-moz-border-radius:0;border-radius:0;-webkit-box-shadow:none;-moz-box-shadow:none;box-shadow:none}.bootstrap-select.btn-group .dropdown-menu dt{display:block;padding:3px 20px;cursor:default}.bootstrap-select.btn-group .div-contain{overflow:hidden}.bootstrap-select.btn-group .dropdown-menu li{position:relative}.bootstrap-select.btn-group .dropdown-menu li>a.opt{position:relative;padding-left:35px}.bootstrap-select.btn-group .dropdown-menu li>a{cursor:pointer}.bootstrap-select.btn-group .dropdown-menu li>dt small{font-weight:400}.bootstrap-select.btn-group.show-tick .dropdown-menu li.selected a i.check-mark{position:absolute;display:inline-block;right:15px;margin-top:2.5px}.bootstrap-select.btn-group .dropdown-menu li a i.check-mark{display:none}.bootstrap-select.btn-group.show-tick .dropdown-menu li a span.text{margin-right:34px}.bootstrap-select.btn-group .dropdown-menu li small{padding-left:.5em}.bootstrap-select.btn-group .dropdown-menu li:not(.disabled)>a:hover small,.bootstrap-select.btn-group .dropdown-menu li:not(.disabled)>a:focus small,.bootstrap-select.btn-group .dropdown-menu li.active:not(.disabled)>a small{color:#64b1d8;color:rgba(255,255,255,.4)}.bootstrap-select.btn-group .dropdown-menu li>dt small{font-weight:400}.bootstrap-select.show-menu-arrow .dropdown-toggle:before{content:'';display:inline-block;border-left:7px solid transparent;border-right:7px solid transparent;border-bottom:7px solid #CCC;border-bottom-color:rgba(0,0,0,.2);position:absolute;bottom:-4px;left:9px;display:none}.bootstrap-select.show-menu-arrow .dropdown-toggle:after{content:'';display:inline-block;border-left:6px solid transparent;border-right:6px solid transparent;border-bottom:6px solid #fff;position:absolute;bottom:-4px;left:10px;display:none}.bootstrap-select.show-menu-arrow.dropup .dropdown-toggle:before{bottom:auto;top:-3px;border-top:7px solid #ccc;border-bottom:0;border-top-color:rgba(0,0,0,.2)}.bootstrap-select.show-menu-arrow.dropup .dropdown-toggle:after{bottom:auto;top:-3px;border-top:6px solid #fff;border-bottom:0}.bootstrap-select.show-menu-arrow.pull-right .dropdown-toggle:before{right:12px;left:auto}.bootstrap-select.show-menu-arrow.pull-right .dropdown-toggle:after{right:13px;left:auto}.bootstrap-select.show-menu-arrow.open>.dropdown-toggle:before,.bootstrap-select.show-menu-arrow.open>.dropdown-toggle:after{display:block}.bootstrap-select.btn-group .no-results{padding:3px;background:#f5f5f5;margin:0 5px}.bootstrap-select.btn-group .dropdown-menu .notify{position:absolute;bottom:5px;width:96%;margin:0 2%;min-height:26px;padding:3px 5px;background:#f5f5f5;border:1px solid #e3e3e3;box-shadow:inset 0 1px 1px rgba(0,0,0,.05);pointer-events:none;opacity:.9;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box}.mobile-device{position:absolute;top:0;left:0;display:block!important;width:100%;height:100%!important;opacity:0}.bootstrap-select.fit-width{width:auto!important}.bootstrap-select.btn-group.fit-width .btn .filter-option{position:static}.bootstrap-select.btn-group.fit-width .btn .caret{position:static;top:auto;margin-top:-1px}.control-group.error .bootstrap-select .dropdown-toggle{border-color:#b94a48}.bootstrap-select-searchbox,.bootstrap-select .bs-actionsbox{padding:4px 8px}.bootstrap-select .bs-actionsbox{float:left;width:100%;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box}.bootstrap-select-searchbox+.bs-actionsbox{padding:0 8px 4px}.bootstrap-select-searchbox input{margin-bottom:0}.bootstrap-select .bs-actionsbox .btn-group button{width:50%}");
});

/*!
 * bootstrap-select v1.5.4
 * http://silviomoreto.github.io/bootstrap-select/
 *
 * Copyright 2013 bootstrap-select
 * Licensed under the MIT license
 */
!function($) {
    "use strict";
    $.expr[":"].icontains = function(obj, index, meta) {
        return $(obj).text().toUpperCase().indexOf(meta[3].toUpperCase()) >= 0;
    };
    var Selectpicker = function(element, options, e) {
        if (e) {
            e.stopPropagation();
            e.preventDefault();
        }
        this.$element = $(element);
        this.$newElement = null;
        this.$button = null;
        this.$menu = null;
        this.$lis = null;
        //Merge defaults, options and data-attributes to make our options
        this.options = $.extend({}, $.fn.selectpicker.defaults, this.$element.data(), typeof options == "object" && options);
        //If we have no title yet, check the attribute 'title' (this is missed by jq as its not a data-attribute
        if (this.options.title === null) {
            this.options.title = this.$element.attr("title");
        }
        //Expose public methods
        this.val = Selectpicker.prototype.val;
        this.render = Selectpicker.prototype.render;
        this.refresh = Selectpicker.prototype.refresh;
        this.setStyle = Selectpicker.prototype.setStyle;
        this.selectAll = Selectpicker.prototype.selectAll;
        this.deselectAll = Selectpicker.prototype.deselectAll;
        this.init();
    };
    Selectpicker.prototype = {
        constructor: Selectpicker,
        init: function() {
            var that = this, id = this.$element.attr("id");
            this.$element.hide();
            this.multiple = this.$element.prop("multiple");
            this.autofocus = this.$element.prop("autofocus");
            this.$newElement = this.createView();
            this.$element.after(this.$newElement);
            this.$menu = this.$newElement.find("> .dropdown-menu");
            this.$button = this.$newElement.find("> button");
            this.$searchbox = this.$newElement.find("input");
            if (id !== undefined) {
                this.$button.attr("data-id", id);
                $('label[for="' + id + '"]').click(function(e) {
                    e.preventDefault();
                    that.$button.focus();
                });
            }
            this.checkDisabled();
            this.clickListener();
            if (this.options.liveSearch) this.liveSearchListener();
            this.render();
            this.liHeight();
            this.setStyle();
            this.setWidth();
            if (this.options.container) this.selectPosition();
            this.$menu.data("this", this);
            this.$newElement.data("this", this);
        },
        createDropdown: function() {
            //If we are multiple, then add the show-tick class by default
            var multiple = this.multiple ? " show-tick" : "";
            var inputGroup = this.$element.parent().hasClass("input-group") ? " input-group-btn" : "";
            var autofocus = this.autofocus ? " autofocus" : "";
            var header = this.options.header ? '<div class="popover-title"><button type="button" class="close" aria-hidden="true">&times;</button>' + this.options.header + "</div>" : "";
            var searchbox = this.options.liveSearch ? '<div class="bootstrap-select-searchbox"><input type="text" class="input-block-level form-control" /></div>' : "";
            var actionsbox = this.options.actionsBox ? '<div class="bs-actionsbox">' + '<div class="btn-group btn-block">' + '<button class="actions-btn bs-select-all btn btn-sm btn-default">' + "Select All" + "</button>" + '<button class="actions-btn bs-deselect-all btn btn-sm btn-default">' + "Deselect All" + "</button>" + "</div>" + "</div>" : "";
            var drop = '<div class="btn-group bootstrap-select' + multiple + inputGroup + '">' + '<button type="button" class="btn dropdown-toggle selectpicker" data-toggle="dropdown"' + autofocus + ">" + '<span class="filter-option pull-left"></span>&nbsp;' + '<span class="caret"></span>' + "</button>" + '<div class="dropdown-menu open">' + header + searchbox + actionsbox + '<ul class="dropdown-menu inner selectpicker" role="menu">' + "</ul>" + "</div>" + "</div>";
            return $(drop);
        },
        createView: function() {
            var $drop = this.createDropdown();
            var $li = this.createLi();
            $drop.find("ul").append($li);
            return $drop;
        },
        reloadLi: function() {
            //Remove all children.
            this.destroyLi();
            //Re build
            var $li = this.createLi();
            this.$menu.find("ul").append($li);
        },
        destroyLi: function() {
            this.$menu.find("li").remove();
        },
        createLi: function() {
            var that = this, _liA = [], _liHtml = "";
            this.$element.find("option").each(function() {
                var $this = $(this);
                //Get the class and text for the option
                var optionClass = $this.attr("class") || "";
                var inline = $this.attr("style") || "";
                var text = $this.data("content") ? $this.data("content") : $this.html();
                var subtext = $this.data("subtext") !== undefined ? '<small class="muted text-muted">' + $this.data("subtext") + "</small>" : "";
                var icon = $this.data("icon") !== undefined ? '<i class="' + that.options.iconBase + " " + $this.data("icon") + '"></i> ' : "";
                if (icon !== "" && ($this.is(":disabled") || $this.parent().is(":disabled"))) {
                    icon = "<span>" + icon + "</span>";
                }
                if (!$this.data("content")) {
                    //Prepend any icon and append any subtext to the main text.
                    text = icon + '<span class="text">' + text + subtext + "</span>";
                }
                if (that.options.hideDisabled && ($this.is(":disabled") || $this.parent().is(":disabled"))) {
                    _liA.push('<a style="min-height: 0; padding: 0"></a>');
                } else if ($this.parent().is("optgroup") && $this.data("divider") !== true) {
                    if ($this.index() === 0) {
                        //Get the opt group label
                        var label = $this.parent().attr("label");
                        var labelSubtext = $this.parent().data("subtext") !== undefined ? '<small class="muted text-muted">' + $this.parent().data("subtext") + "</small>" : "";
                        var labelIcon = $this.parent().data("icon") ? '<i class="' + $this.parent().data("icon") + '"></i> ' : "";
                        label = labelIcon + '<span class="text">' + label + labelSubtext + "</span>";
                        if ($this[0].index !== 0) {
                            _liA.push('<div class="div-contain"><div class="divider"></div></div>' + "<dt>" + label + "</dt>" + that.createA(text, "opt " + optionClass, inline));
                        } else {
                            _liA.push("<dt>" + label + "</dt>" + that.createA(text, "opt " + optionClass, inline));
                        }
                    } else {
                        _liA.push(that.createA(text, "opt " + optionClass, inline));
                    }
                } else if ($this.data("divider") === true) {
                    _liA.push('<div class="div-contain"><div class="divider"></div></div>');
                } else if ($(this).data("hidden") === true) {
                    _liA.push("<a></a>");
                } else {
                    _liA.push(that.createA(text, optionClass, inline));
                }
            });
            $.each(_liA, function(i, item) {
                var hide = item === "<a></a>" ? 'class="hide is-hidden"' : "";
                _liHtml += '<li rel="' + i + '"' + hide + ">" + item + "</li>";
            });
            //If we are not multiple, and we dont have a selected item, and we dont have a title, select the first element so something is set in the button
            if (!this.multiple && this.$element.find("option:selected").length === 0 && !this.options.title) {
                this.$element.find("option").eq(0).prop("selected", true).attr("selected", "selected");
            }
            return $(_liHtml);
        },
        createA: function(text, classes, inline) {
            return '<a tabindex="0" class="' + classes + '" style="' + inline + '">' + text + '<i class="' + this.options.iconBase + " " + this.options.tickIcon + ' icon-ok check-mark"></i>' + "</a>";
        },
        render: function(updateLi) {
            var that = this;
            //Update the LI to match the SELECT
            if (updateLi !== false) {
                this.$element.find("option").each(function(index) {
                    that.setDisabled(index, $(this).is(":disabled") || $(this).parent().is(":disabled"));
                    that.setSelected(index, $(this).is(":selected"));
                });
            }
            this.tabIndex();
            var selectedItems = this.$element.find("option:selected").map(function() {
                var $this = $(this);
                var icon = $this.data("icon") && that.options.showIcon ? '<i class="' + that.options.iconBase + " " + $this.data("icon") + '"></i> ' : "";
                var subtext;
                if (that.options.showSubtext && $this.attr("data-subtext") && !that.multiple) {
                    subtext = ' <small class="muted text-muted">' + $this.data("subtext") + "</small>";
                } else {
                    subtext = "";
                }
                if ($this.data("content") && that.options.showContent) {
                    return $this.data("content");
                } else if ($this.attr("title") !== undefined) {
                    return $this.attr("title");
                } else {
                    return icon + $this.html() + subtext;
                }
            }).toArray();
            //Fixes issue in IE10 occurring when no default option is selected and at least one option is disabled
            //Convert all the values into a comma delimited string
            var title = !this.multiple ? selectedItems[0] : selectedItems.join(this.options.multipleSeparator);
            //If this is multi select, and the selectText type is count, the show 1 of 2 selected etc..
            if (this.multiple && this.options.selectedTextFormat.indexOf("count") > -1) {
                var max = this.options.selectedTextFormat.split(">");
                var notDisabled = this.options.hideDisabled ? ":not([disabled])" : "";
                if (max.length > 1 && selectedItems.length > max[1] || max.length == 1 && selectedItems.length >= 2) {
                    title = this.options.countSelectedText.replace("{0}", selectedItems.length).replace("{1}", this.$element.find('option:not([data-divider="true"]):not([data-hidden="true"])' + notDisabled).length);
                }
            }
            this.options.title = this.$element.attr("title");
            //If we dont have a title, then use the default, or if nothing is set at all, use the not selected text
            if (!title) {
                title = this.options.title !== undefined ? this.options.title : this.options.noneSelectedText;
            }
            this.$button.attr("title", $.trim(title));
            this.$newElement.find(".filter-option").html(title);
        },
        setStyle: function(style, status) {
            if (this.$element.attr("class")) {
                this.$newElement.addClass(this.$element.attr("class").replace(/selectpicker|mobile-device/gi, ""));
            }
            var buttonClass = style ? style : this.options.style;
            if (status == "add") {
                this.$button.addClass(buttonClass);
            } else if (status == "remove") {
                this.$button.removeClass(buttonClass);
            } else {
                this.$button.removeClass(this.options.style);
                this.$button.addClass(buttonClass);
            }
        },
        liHeight: function() {
            if (this.options.size === false) return;
            var $selectClone = this.$menu.parent().clone().find("> .dropdown-toggle").prop("autofocus", false).end().appendTo("body"), $menuClone = $selectClone.addClass("open").find("> .dropdown-menu"), liHeight = $menuClone.find("li > a").outerHeight(), headerHeight = this.options.header ? $menuClone.find(".popover-title").outerHeight() : 0, searchHeight = this.options.liveSearch ? $menuClone.find(".bootstrap-select-searchbox").outerHeight() : 0, actionsHeight = this.options.actionsBox ? $menuClone.find(".bs-actionsbox").outerHeight() : 0;
            $selectClone.remove();
            this.$newElement.data("liHeight", liHeight).data("headerHeight", headerHeight).data("searchHeight", searchHeight).data("actionsHeight", actionsHeight);
        },
        setSize: function() {
            var that = this, menu = this.$menu, menuInner = menu.find(".inner"), selectHeight = this.$newElement.outerHeight(), liHeight = this.$newElement.data("liHeight"), headerHeight = this.$newElement.data("headerHeight"), searchHeight = this.$newElement.data("searchHeight"), actionsHeight = this.$newElement.data("actionsHeight"), divHeight = menu.find("li .divider").outerHeight(true), menuPadding = parseInt(menu.css("padding-top")) + parseInt(menu.css("padding-bottom")) + parseInt(menu.css("border-top-width")) + parseInt(menu.css("border-bottom-width")), notDisabled = this.options.hideDisabled ? ":not(.disabled)" : "", $window = $(window), menuExtras = menuPadding + parseInt(menu.css("margin-top")) + parseInt(menu.css("margin-bottom")) + 2, menuHeight, selectOffsetTop, selectOffsetBot, posVert = function() {
                selectOffsetTop = that.$newElement.offset().top - $window.scrollTop();
                selectOffsetBot = $window.height() - selectOffsetTop - selectHeight;
            };
            posVert();
            if (this.options.header) menu.css("padding-top", 0);
            if (this.options.size == "auto") {
                var getSize = function() {
                    var minHeight, lisVis = that.$lis.not(".hide");
                    posVert();
                    menuHeight = selectOffsetBot - menuExtras;
                    if (that.options.dropupAuto) {
                        that.$newElement.toggleClass("dropup", selectOffsetTop > selectOffsetBot && menuHeight - menuExtras < menu.height());
                    }
                    if (that.$newElement.hasClass("dropup")) {
                        menuHeight = selectOffsetTop - menuExtras;
                    }
                    if (lisVis.length + lisVis.find("dt").length > 3) {
                        minHeight = liHeight * 3 + menuExtras - 2;
                    } else {
                        minHeight = 0;
                    }
                    menu.css({
                        "max-height": menuHeight + "px",
                        overflow: "hidden",
                        "min-height": minHeight + headerHeight + searchHeight + actionsHeight + "px"
                    });
                    menuInner.css({
                        "max-height": menuHeight - headerHeight - searchHeight - actionsHeight - menuPadding + "px",
                        "overflow-y": "auto",
                        "min-height": Math.max(minHeight - menuPadding, 0) + "px"
                    });
                };
                getSize();
                this.$searchbox.off("input.getSize propertychange.getSize").on("input.getSize propertychange.getSize", getSize);
                $(window).off("resize.getSize").on("resize.getSize", getSize);
                $(window).off("scroll.getSize").on("scroll.getSize", getSize);
            } else if (this.options.size && this.options.size != "auto" && menu.find("li" + notDisabled).length > this.options.size) {
                var optIndex = menu.find("li" + notDisabled + " > *").filter(":not(.div-contain)").slice(0, this.options.size).last().parent().index();
                var divLength = menu.find("li").slice(0, optIndex + 1).find(".div-contain").length;
                menuHeight = liHeight * this.options.size + divLength * divHeight + menuPadding;
                if (that.options.dropupAuto) {
                    this.$newElement.toggleClass("dropup", selectOffsetTop > selectOffsetBot && menuHeight < menu.height());
                }
                menu.css({
                    "max-height": menuHeight + headerHeight + searchHeight + actionsHeight + "px",
                    overflow: "hidden"
                });
                menuInner.css({
                    "max-height": menuHeight - menuPadding + "px",
                    "overflow-y": "auto"
                });
            }
        },
        setWidth: function() {
            if (this.options.width == "auto") {
                this.$menu.css("min-width", "0");
                // Get correct width if element hidden
                var selectClone = this.$newElement.clone().appendTo("body");
                var ulWidth = selectClone.find("> .dropdown-menu").css("width");
                var btnWidth = selectClone.css("width", "auto").find("> button").css("width");
                selectClone.remove();
                // Set width to whatever's larger, button title or longest option
                this.$newElement.css("width", Math.max(parseInt(ulWidth), parseInt(btnWidth)) + "px");
            } else if (this.options.width == "fit") {
                // Remove inline min-width so width can be changed from 'auto'
                this.$menu.css("min-width", "");
                this.$newElement.css("width", "").addClass("fit-width");
            } else if (this.options.width) {
                // Remove inline min-width so width can be changed from 'auto'
                this.$menu.css("min-width", "");
                this.$newElement.css("width", this.options.width);
            } else {
                // Remove inline min-width/width so width can be changed
                this.$menu.css("min-width", "");
                this.$newElement.css("width", "");
            }
            // Remove fit-width class if width is changed programmatically
            if (this.$newElement.hasClass("fit-width") && this.options.width !== "fit") {
                this.$newElement.removeClass("fit-width");
            }
        },
        selectPosition: function() {
            var that = this, drop = "<div />", $drop = $(drop), pos, actualHeight, getPlacement = function($element) {
                $drop.addClass($element.attr("class").replace(/form-control/gi, "")).toggleClass("dropup", $element.hasClass("dropup"));
                pos = $element.offset();
                actualHeight = $element.hasClass("dropup") ? 0 : $element[0].offsetHeight;
                $drop.css({
                    top: pos.top + actualHeight,
                    left: pos.left,
                    width: $element[0].offsetWidth,
                    position: "absolute"
                });
            };
            this.$newElement.on("click", function() {
                if (that.isDisabled()) {
                    return;
                }
                getPlacement($(this));
                $drop.appendTo(that.options.container);
                $drop.toggleClass("open", !$(this).hasClass("open"));
                $drop.append(that.$menu);
            });
            $(window).resize(function() {
                getPlacement(that.$newElement);
            });
            $(window).on("scroll", function() {
                getPlacement(that.$newElement);
            });
            $("html").on("click", function(e) {
                if ($(e.target).closest(that.$newElement).length < 1) {
                    $drop.removeClass("open");
                }
            });
        },
        mobile: function() {
            this.$element.addClass("mobile-device").appendTo(this.$newElement);
            if (this.options.container) this.$menu.hide();
        },
        refresh: function() {
            this.$lis = null;
            this.reloadLi();
            this.render();
            this.setWidth();
            this.setStyle();
            this.checkDisabled();
            this.liHeight();
        },
        update: function() {
            this.reloadLi();
            this.setWidth();
            this.setStyle();
            this.checkDisabled();
            this.liHeight();
        },
        setSelected: function(index, selected) {
            if (this.$lis == null) this.$lis = this.$menu.find("li");
            $(this.$lis[index]).toggleClass("selected", selected);
        },
        setDisabled: function(index, disabled) {
            if (this.$lis == null) this.$lis = this.$menu.find("li");
            if (disabled) {
                $(this.$lis[index]).addClass("disabled").find("a").attr("href", "#").attr("tabindex", -1);
            } else {
                $(this.$lis[index]).removeClass("disabled").find("a").removeAttr("href").attr("tabindex", 0);
            }
        },
        isDisabled: function() {
            return this.$element.is(":disabled");
        },
        checkDisabled: function() {
            var that = this;
            if (this.isDisabled()) {
                this.$button.addClass("disabled").attr("tabindex", -1);
            } else {
                if (this.$button.hasClass("disabled")) {
                    this.$button.removeClass("disabled");
                }
                if (this.$button.attr("tabindex") == -1) {
                    if (!this.$element.data("tabindex")) this.$button.removeAttr("tabindex");
                }
            }
            this.$button.click(function() {
                return !that.isDisabled();
            });
        },
        tabIndex: function() {
            if (this.$element.is("[tabindex]")) {
                this.$element.data("tabindex", this.$element.attr("tabindex"));
                this.$button.attr("tabindex", this.$element.data("tabindex"));
            }
        },
        clickListener: function() {
            var that = this;
            $("body").on("touchstart.dropdown", ".dropdown-menu", function(e) {
                e.stopPropagation();
            });
            this.$newElement.on("click", function() {
                that.setSize();
                if (!that.options.liveSearch && !that.multiple) {
                    setTimeout(function() {
                        that.$menu.find(".selected a").focus();
                    }, 10);
                }
            });
            this.$menu.on("click", "li a", function(e) {
                var clickedIndex = $(this).parent().index(), prevValue = that.$element.val(), prevIndex = that.$element.prop("selectedIndex");
                //Dont close on multi choice menu
                if (that.multiple) {
                    e.stopPropagation();
                }
                e.preventDefault();
                //Dont run if we have been disabled
                if (!that.isDisabled() && !$(this).parent().hasClass("disabled")) {
                    var $options = that.$element.find("option"), $option = $options.eq(clickedIndex), state = $option.prop("selected"), $optgroup = $option.parent("optgroup"), maxOptions = that.options.maxOptions, maxOptionsGrp = $optgroup.data("maxOptions") || false;
                    //Deselect all others if not multi select box
                    if (!that.multiple) {
                        $options.prop("selected", false);
                        $option.prop("selected", true);
                        that.$menu.find(".selected").removeClass("selected");
                        that.setSelected(clickedIndex, true);
                    } else {
                        $option.prop("selected", !state);
                        that.setSelected(clickedIndex, !state);
                        if (maxOptions !== false || maxOptionsGrp !== false) {
                            var maxReached = maxOptions < $options.filter(":selected").length, maxReachedGrp = maxOptionsGrp < $optgroup.find("option:selected").length, maxOptionsArr = that.options.maxOptionsText, maxTxt = maxOptionsArr[0].replace("{n}", maxOptions), maxTxtGrp = maxOptionsArr[1].replace("{n}", maxOptionsGrp), $notify = $('<div class="notify"></div>');
                            if (maxOptions && maxReached || maxOptionsGrp && maxReachedGrp) {
                                // If {var} is set in array, replace it
                                if (maxOptionsArr[2]) {
                                    maxTxt = maxTxt.replace("{var}", maxOptionsArr[2][maxOptions > 1 ? 0 : 1]);
                                    maxTxtGrp = maxTxtGrp.replace("{var}", maxOptionsArr[2][maxOptionsGrp > 1 ? 0 : 1]);
                                }
                                $option.prop("selected", false);
                                that.$menu.append($notify);
                                if (maxOptions && maxReached) {
                                    $notify.append($("<div>" + maxTxt + "</div>"));
                                    that.$element.trigger("maxReached.bs.select");
                                }
                                if (maxOptionsGrp && maxReachedGrp) {
                                    $notify.append($("<div>" + maxTxtGrp + "</div>"));
                                    that.$element.trigger("maxReachedGrp.bs.select");
                                }
                                setTimeout(function() {
                                    that.setSelected(clickedIndex, false);
                                }, 10);
                                $notify.delay(750).fadeOut(300, function() {
                                    $(this).remove();
                                });
                            }
                        }
                    }
                    if (!that.multiple) {
                        that.$button.focus();
                    } else if (that.options.liveSearch) {
                        that.$searchbox.focus();
                    }
                    // Trigger select 'change'
                    if (prevValue != that.$element.val() && that.multiple || prevIndex != that.$element.prop("selectedIndex") && !that.multiple) {
                        that.$element.change();
                    }
                }
            });
            this.$menu.on("click", "li.disabled a, li dt, li .div-contain, .popover-title, .popover-title :not(.close)", function(e) {
                if (e.target == this) {
                    e.preventDefault();
                    e.stopPropagation();
                    if (!that.options.liveSearch) {
                        that.$button.focus();
                    } else {
                        that.$searchbox.focus();
                    }
                }
            });
            this.$menu.on("click", ".popover-title .close", function() {
                that.$button.focus();
            });
            this.$searchbox.on("click", function(e) {
                e.stopPropagation();
            });
            this.$menu.on("click", ".actions-btn", function(e) {
                if (that.options.liveSearch) {
                    that.$searchbox.focus();
                } else {
                    that.$button.focus();
                }
                e.preventDefault();
                e.stopPropagation();
                if ($(this).is(".bs-select-all")) {
                    that.selectAll();
                } else {
                    that.deselectAll();
                }
                that.$element.change();
            });
            this.$element.change(function() {
                that.render(false);
            });
        },
        liveSearchListener: function() {
            var that = this, no_results = $('<li class="no-results"></li>');
            this.$newElement.on("click.dropdown.data-api", function() {
                that.$menu.find(".active").removeClass("active");
                if (!!that.$searchbox.val()) {
                    that.$searchbox.val("");
                    that.$lis.not(".is-hidden").removeClass("hide");
                    if (!!no_results.parent().length) no_results.remove();
                }
                if (!that.multiple) that.$menu.find(".selected").addClass("active");
                setTimeout(function() {
                    that.$searchbox.focus();
                }, 10);
            });
            this.$searchbox.on("input propertychange", function() {
                if (that.$searchbox.val()) {
                    that.$lis.not(".is-hidden").removeClass("hide").find("a").not(":icontains(" + that.$searchbox.val() + ")").parent().addClass("hide");
                    if (!that.$menu.find("li").filter(":visible:not(.no-results)").length) {
                        if (!!no_results.parent().length) no_results.remove();
                        no_results.html(that.options.noneResultsText + ' "' + that.$searchbox.val() + '"').show();
                        that.$menu.find("li").last().after(no_results);
                    } else if (!!no_results.parent().length) {
                        no_results.remove();
                    }
                } else {
                    that.$lis.not(".is-hidden").removeClass("hide");
                    if (!!no_results.parent().length) no_results.remove();
                }
                that.$menu.find("li.active").removeClass("active");
                that.$menu.find("li").filter(":visible:not(.divider)").eq(0).addClass("active").find("a").focus();
                $(this).focus();
            });
            this.$menu.on("mouseenter", "a", function(e) {
                that.$menu.find(".active").removeClass("active");
                $(e.currentTarget).parent().not(".disabled").addClass("active");
            });
            this.$menu.on("mouseleave", "a", function() {
                that.$menu.find(".active").removeClass("active");
            });
        },
        val: function(value) {
            if (value !== undefined) {
                this.$element.val(value);
                this.$element.change();
                return this.$element;
            } else {
                return this.$element.val();
            }
        },
        selectAll: function() {
            if (this.$lis == null) this.$lis = this.$menu.find("li");
            this.$element.find("option:enabled").prop("selected", true);
            $(this.$lis).filter(":not(.disabled)").addClass("selected");
            this.render(false);
        },
        deselectAll: function() {
            if (this.$lis == null) this.$lis = this.$menu.find("li");
            this.$element.find("option:enabled").prop("selected", false);
            $(this.$lis).filter(":not(.disabled)").removeClass("selected");
            this.render(false);
        },
        keydown: function(e) {
            var $this, $items, $parent, index, next, first, last, prev, nextPrev, that, prevIndex, isActive, keyCodeMap = {
                32: " ",
                48: "0",
                49: "1",
                50: "2",
                51: "3",
                52: "4",
                53: "5",
                54: "6",
                55: "7",
                56: "8",
                57: "9",
                59: ";",
                65: "a",
                66: "b",
                67: "c",
                68: "d",
                69: "e",
                70: "f",
                71: "g",
                72: "h",
                73: "i",
                74: "j",
                75: "k",
                76: "l",
                77: "m",
                78: "n",
                79: "o",
                80: "p",
                81: "q",
                82: "r",
                83: "s",
                84: "t",
                85: "u",
                86: "v",
                87: "w",
                88: "x",
                89: "y",
                90: "z",
                96: "0",
                97: "1",
                98: "2",
                99: "3",
                100: "4",
                101: "5",
                102: "6",
                103: "7",
                104: "8",
                105: "9"
            };
            $this = $(this);
            $parent = $this.parent();
            if ($this.is("input")) $parent = $this.parent().parent();
            that = $parent.data("this");
            if (that.options.liveSearch) $parent = $this.parent().parent();
            if (that.options.container) $parent = that.$menu;
            $items = $("[role=menu] li:not(.divider) a", $parent);
            isActive = that.$menu.parent().hasClass("open");
            if (!isActive && /([0-9]|[A-z])/.test(String.fromCharCode(e.keyCode))) {
                if (!that.options.container) {
                    that.setSize();
                    that.$menu.parent().addClass("open");
                    isActive = that.$menu.parent().hasClass("open");
                } else {
                    that.$newElement.trigger("click");
                }
                that.$searchbox.focus();
            }
            if (that.options.liveSearch) {
                if (/(^9$|27)/.test(e.keyCode) && isActive && that.$menu.find(".active").length === 0) {
                    e.preventDefault();
                    that.$menu.parent().removeClass("open");
                    that.$button.focus();
                }
                $items = $("[role=menu] li:not(.divider):visible", $parent);
                if (!$this.val() && !/(38|40)/.test(e.keyCode)) {
                    if ($items.filter(".active").length === 0) {
                        $items = that.$newElement.find("li").filter(":icontains(" + keyCodeMap[e.keyCode] + ")");
                    }
                }
            }
            if (!$items.length) return;
            if (/(38|40)/.test(e.keyCode)) {
                index = $items.index($items.filter(":focus"));
                first = $items.parent(":not(.disabled):visible").first().index();
                last = $items.parent(":not(.disabled):visible").last().index();
                next = $items.eq(index).parent().nextAll(":not(.disabled):visible").eq(0).index();
                prev = $items.eq(index).parent().prevAll(":not(.disabled):visible").eq(0).index();
                nextPrev = $items.eq(next).parent().prevAll(":not(.disabled):visible").eq(0).index();
                if (that.options.liveSearch) {
                    $items.each(function(i) {
                        if ($(this).is(":not(.disabled)")) {
                            $(this).data("index", i);
                        }
                    });
                    index = $items.index($items.filter(".active"));
                    first = $items.filter(":not(.disabled):visible").first().data("index");
                    last = $items.filter(":not(.disabled):visible").last().data("index");
                    next = $items.eq(index).nextAll(":not(.disabled):visible").eq(0).data("index");
                    prev = $items.eq(index).prevAll(":not(.disabled):visible").eq(0).data("index");
                    nextPrev = $items.eq(next).prevAll(":not(.disabled):visible").eq(0).data("index");
                }
                prevIndex = $this.data("prevIndex");
                if (e.keyCode == 38) {
                    if (that.options.liveSearch) index -= 1;
                    if (index != nextPrev && index > prev) index = prev;
                    if (index < first) index = first;
                    if (index == prevIndex) index = last;
                }
                if (e.keyCode == 40) {
                    if (that.options.liveSearch) index += 1;
                    if (index == -1) index = 0;
                    if (index != nextPrev && index < next) index = next;
                    if (index > last) index = last;
                    if (index == prevIndex) index = first;
                }
                $this.data("prevIndex", index);
                if (!that.options.liveSearch) {
                    $items.eq(index).focus();
                } else {
                    e.preventDefault();
                    if (!$this.is(".dropdown-toggle")) {
                        $items.removeClass("active");
                        $items.eq(index).addClass("active").find("a").focus();
                        $this.focus();
                    }
                }
            } else if (!$this.is("input")) {
                var keyIndex = [], count, prevKey;
                $items.each(function() {
                    if ($(this).parent().is(":not(.disabled)")) {
                        if ($.trim($(this).text().toLowerCase()).substring(0, 1) == keyCodeMap[e.keyCode]) {
                            keyIndex.push($(this).parent().index());
                        }
                    }
                });
                count = $(document).data("keycount");
                count++;
                $(document).data("keycount", count);
                prevKey = $.trim($(":focus").text().toLowerCase()).substring(0, 1);
                if (prevKey != keyCodeMap[e.keyCode]) {
                    count = 1;
                    $(document).data("keycount", count);
                } else if (count >= keyIndex.length) {
                    $(document).data("keycount", 0);
                    if (count > keyIndex.length) count = 1;
                }
                $items.eq(keyIndex[count - 1]).focus();
            }
            // Select focused option if "Enter", "Spacebar", "Tab" are pressed inside the menu.
            if (/(13|32|^9$)/.test(e.keyCode) && isActive) {
                if (!/(32)/.test(e.keyCode)) e.preventDefault();
                if (!that.options.liveSearch) {
                    $(":focus").click();
                } else if (!/(32)/.test(e.keyCode)) {
                    that.$menu.find(".active a").click();
                    $this.focus();
                }
                $(document).data("keycount", 0);
            }
            if (/(^9$|27)/.test(e.keyCode) && isActive && (that.multiple || that.options.liveSearch) || /(27)/.test(e.keyCode) && !isActive) {
                that.$menu.parent().removeClass("open");
                that.$button.focus();
            }
        },
        hide: function() {
            this.$newElement.hide();
        },
        show: function() {
            this.$newElement.show();
        },
        destroy: function() {
            this.$newElement.remove();
            this.$element.remove();
        }
    };
    $.fn.selectpicker = function(option, event) {
        //get the args of the outer function..
        var args = arguments;
        var value;
        var chain = this.each(function() {
            if ($(this).is("select")) {
                var $this = $(this), data = $this.data("selectpicker"), options = typeof option == "object" && option;
                if (!data) {
                    $this.data("selectpicker", data = new Selectpicker(this, options, event));
                } else if (options) {
                    for (var i in options) {
                        data.options[i] = options[i];
                    }
                }
                if (typeof option == "string") {
                    //Copy the value of option, as once we shift the arguments
                    //it also shifts the value of option.
                    var property = option;
                    if (data[property] instanceof Function) {
                        [].shift.apply(args);
                        value = data[property].apply(data, args);
                    } else {
                        value = data.options[property];
                    }
                }
            }
        });
        if (value !== undefined) {
            return value;
        } else {
            return chain;
        }
    };
    $.fn.selectpicker.defaults = {
        style: "btn-default",
        size: "auto",
        title: null,
        selectedTextFormat: "values",
        noneSelectedText: "Nothing selected",
        noneResultsText: "No results match",
        countSelectedText: "{0} of {1} selected",
        maxOptionsText: [ "Limit reached ({n} {var} max)", "Group limit reached ({n} {var} max)", [ "items", "item" ] ],
        width: false,
        container: false,
        hideDisabled: false,
        showSubtext: false,
        showIcon: true,
        showContent: true,
        dropupAuto: true,
        header: false,
        liveSearch: false,
        actionsBox: false,
        multipleSeparator: ", ",
        iconBase: "glyphicon",
        tickIcon: "glyphicon-ok",
        maxOptions: false
    };
    $(document).data("keycount", 0).on("keydown", ".bootstrap-select [data-toggle=dropdown], .bootstrap-select [role=menu], .bootstrap-select-searchbox input", Selectpicker.prototype.keydown).on("focusin.modal", ".bootstrap-select [data-toggle=dropdown], .bootstrap-select [role=menu], .bootstrap-select-searchbox input", function(e) {
        e.stopPropagation();
    });
}(window.jQuery);

define("torabot/main/0.1.0/typeahead.jquery-debug", [], function(require, exports, module) {
    /*!
 * typeahead.js 0.10.2
 * https://github.com/twitter/typeahead.js
 * Copyright 2013-2014 Twitter, Inc. and other contributors; Licensed MIT
 */
    (function($) {
        var _ = {
            isMsie: function() {
                return /(msie|trident)/i.test(navigator.userAgent) ? navigator.userAgent.match(/(msie |rv:)(\d+(.\d+)?)/i)[2] : false;
            },
            isBlankString: function(str) {
                return !str || /^\s*$/.test(str);
            },
            escapeRegExChars: function(str) {
                return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
            },
            isString: function(obj) {
                return typeof obj === "string";
            },
            isNumber: function(obj) {
                return typeof obj === "number";
            },
            isArray: $.isArray,
            isFunction: $.isFunction,
            isObject: $.isPlainObject,
            isUndefined: function(obj) {
                return typeof obj === "undefined";
            },
            bind: $.proxy,
            each: function(collection, cb) {
                $.each(collection, reverseArgs);
                function reverseArgs(index, value) {
                    return cb(value, index);
                }
            },
            map: $.map,
            filter: $.grep,
            every: function(obj, test) {
                var result = true;
                if (!obj) {
                    return result;
                }
                $.each(obj, function(key, val) {
                    if (!(result = test.call(null, val, key, obj))) {
                        return false;
                    }
                });
                return !!result;
            },
            some: function(obj, test) {
                var result = false;
                if (!obj) {
                    return result;
                }
                $.each(obj, function(key, val) {
                    if (result = test.call(null, val, key, obj)) {
                        return false;
                    }
                });
                return !!result;
            },
            mixin: $.extend,
            getUniqueId: function() {
                var counter = 0;
                return function() {
                    return counter++;
                };
            }(),
            templatify: function templatify(obj) {
                return $.isFunction(obj) ? obj : template;
                function template() {
                    return String(obj);
                }
            },
            defer: function(fn) {
                setTimeout(fn, 0);
            },
            debounce: function(func, wait, immediate) {
                var timeout, result;
                return function() {
                    var context = this, args = arguments, later, callNow;
                    later = function() {
                        timeout = null;
                        if (!immediate) {
                            result = func.apply(context, args);
                        }
                    };
                    callNow = immediate && !timeout;
                    clearTimeout(timeout);
                    timeout = setTimeout(later, wait);
                    if (callNow) {
                        result = func.apply(context, args);
                    }
                    return result;
                };
            },
            throttle: function(func, wait) {
                var context, args, timeout, result, previous, later;
                previous = 0;
                later = function() {
                    previous = new Date();
                    timeout = null;
                    result = func.apply(context, args);
                };
                return function() {
                    var now = new Date(), remaining = wait - (now - previous);
                    context = this;
                    args = arguments;
                    if (remaining <= 0) {
                        clearTimeout(timeout);
                        timeout = null;
                        previous = now;
                        result = func.apply(context, args);
                    } else if (!timeout) {
                        timeout = setTimeout(later, remaining);
                    }
                    return result;
                };
            },
            noop: function() {}
        };
        var html = {
            wrapper: '<span class="twitter-typeahead"></span>',
            dropdown: '<span class="tt-dropdown-menu"></span>',
            dataset: '<div class="tt-dataset-%CLASS%"></div>',
            suggestions: '<span class="tt-suggestions"></span>',
            suggestion: '<div class="tt-suggestion"></div>'
        };
        var css = {
            wrapper: {
                position: "relative",
                display: "inline-block"
            },
            hint: {
                position: "absolute",
                top: "0",
                left: "0",
                borderColor: "transparent",
                boxShadow: "none"
            },
            input: {
                position: "relative",
                verticalAlign: "top",
                backgroundColor: "transparent"
            },
            inputWithNoHint: {
                position: "relative",
                verticalAlign: "top"
            },
            dropdown: {
                position: "absolute",
                top: "100%",
                left: "0",
                zIndex: "100",
                display: "none"
            },
            suggestions: {
                display: "block"
            },
            suggestion: {
                whiteSpace: "nowrap",
                cursor: "pointer"
            },
            suggestionChild: {
                whiteSpace: "normal"
            },
            ltr: {
                left: "0",
                right: "auto"
            },
            rtl: {
                left: "auto",
                right: " 0"
            }
        };
        if (_.isMsie()) {
            _.mixin(css.input, {
                backgroundImage: "url(data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)"
            });
        }
        if (_.isMsie() && _.isMsie() <= 7) {
            _.mixin(css.input, {
                marginTop: "-1px"
            });
        }
        var EventBus = function() {
            var namespace = "typeahead:";
            function EventBus(o) {
                if (!o || !o.el) {
                    $.error("EventBus initialized without el");
                }
                this.$el = $(o.el);
            }
            _.mixin(EventBus.prototype, {
                trigger: function(type) {
                    var args = [].slice.call(arguments, 1);
                    this.$el.trigger(namespace + type, args);
                }
            });
            return EventBus;
        }();
        var EventEmitter = function() {
            var splitter = /\s+/, nextTick = getNextTick();
            return {
                onSync: onSync,
                onAsync: onAsync,
                off: off,
                trigger: trigger
            };
            function on(method, types, cb, context) {
                var type;
                if (!cb) {
                    return this;
                }
                types = types.split(splitter);
                cb = context ? bindContext(cb, context) : cb;
                this._callbacks = this._callbacks || {};
                while (type = types.shift()) {
                    this._callbacks[type] = this._callbacks[type] || {
                        sync: [],
                        async: []
                    };
                    this._callbacks[type][method].push(cb);
                }
                return this;
            }
            function onAsync(types, cb, context) {
                return on.call(this, "async", types, cb, context);
            }
            function onSync(types, cb, context) {
                return on.call(this, "sync", types, cb, context);
            }
            function off(types) {
                var type;
                if (!this._callbacks) {
                    return this;
                }
                types = types.split(splitter);
                while (type = types.shift()) {
                    delete this._callbacks[type];
                }
                return this;
            }
            function trigger(types) {
                var type, callbacks, args, syncFlush, asyncFlush;
                if (!this._callbacks) {
                    return this;
                }
                types = types.split(splitter);
                args = [].slice.call(arguments, 1);
                while ((type = types.shift()) && (callbacks = this._callbacks[type])) {
                    syncFlush = getFlush(callbacks.sync, this, [ type ].concat(args));
                    asyncFlush = getFlush(callbacks.async, this, [ type ].concat(args));
                    syncFlush() && nextTick(asyncFlush);
                }
                return this;
            }
            function getFlush(callbacks, context, args) {
                return flush;
                function flush() {
                    var cancelled;
                    for (var i = 0; !cancelled && i < callbacks.length; i += 1) {
                        cancelled = callbacks[i].apply(context, args) === false;
                    }
                    return !cancelled;
                }
            }
            function getNextTick() {
                var nextTickFn;
                if (window.setImmediate) {
                    nextTickFn = function nextTickSetImmediate(fn) {
                        setImmediate(function() {
                            fn();
                        });
                    };
                } else {
                    nextTickFn = function nextTickSetTimeout(fn) {
                        setTimeout(function() {
                            fn();
                        }, 0);
                    };
                }
                return nextTickFn;
            }
            function bindContext(fn, context) {
                return fn.bind ? fn.bind(context) : function() {
                    fn.apply(context, [].slice.call(arguments, 0));
                };
            }
        }();
        var highlight = function(doc) {
            var defaults = {
                node: null,
                pattern: null,
                tagName: "strong",
                className: null,
                wordsOnly: false,
                caseSensitive: false
            };
            return function hightlight(o) {
                var regex;
                o = _.mixin({}, defaults, o);
                if (!o.node || !o.pattern) {
                    return;
                }
                o.pattern = _.isArray(o.pattern) ? o.pattern : [ o.pattern ];
                regex = getRegex(o.pattern, o.caseSensitive, o.wordsOnly);
                traverse(o.node, hightlightTextNode);
                function hightlightTextNode(textNode) {
                    var match, patternNode;
                    if (match = regex.exec(textNode.data)) {
                        wrapperNode = doc.createElement(o.tagName);
                        o.className && (wrapperNode.className = o.className);
                        patternNode = textNode.splitText(match.index);
                        patternNode.splitText(match[0].length);
                        wrapperNode.appendChild(patternNode.cloneNode(true));
                        textNode.parentNode.replaceChild(wrapperNode, patternNode);
                    }
                    return !!match;
                }
                function traverse(el, hightlightTextNode) {
                    var childNode, TEXT_NODE_TYPE = 3;
                    for (var i = 0; i < el.childNodes.length; i++) {
                        childNode = el.childNodes[i];
                        if (childNode.nodeType === TEXT_NODE_TYPE) {
                            i += hightlightTextNode(childNode) ? 1 : 0;
                        } else {
                            traverse(childNode, hightlightTextNode);
                        }
                    }
                }
            };
            function getRegex(patterns, caseSensitive, wordsOnly) {
                var escapedPatterns = [], regexStr;
                for (var i = 0; i < patterns.length; i++) {
                    escapedPatterns.push(_.escapeRegExChars(patterns[i]));
                }
                regexStr = wordsOnly ? "\\b(" + escapedPatterns.join("|") + ")\\b" : "(" + escapedPatterns.join("|") + ")";
                return caseSensitive ? new RegExp(regexStr) : new RegExp(regexStr, "i");
            }
        }(window.document);
        var Input = function() {
            var specialKeyCodeMap;
            specialKeyCodeMap = {
                9: "tab",
                27: "esc",
                37: "left",
                39: "right",
                13: "enter",
                38: "up",
                40: "down"
            };
            function Input(o) {
                var that = this, onBlur, onFocus, onKeydown, onInput;
                o = o || {};
                if (!o.input) {
                    $.error("input is missing");
                }
                onBlur = _.bind(this._onBlur, this);
                onFocus = _.bind(this._onFocus, this);
                onKeydown = _.bind(this._onKeydown, this);
                onInput = _.bind(this._onInput, this);
                this.$hint = $(o.hint);
                this.$input = $(o.input).on("blur.tt", onBlur).on("focus.tt", onFocus).on("keydown.tt", onKeydown);
                if (this.$hint.length === 0) {
                    this.setHint = this.getHint = this.clearHint = this.clearHintIfInvalid = _.noop;
                }
                if (!_.isMsie()) {
                    this.$input.on("input.tt", onInput);
                } else {
                    this.$input.on("keydown.tt keypress.tt cut.tt paste.tt", function($e) {
                        if (specialKeyCodeMap[$e.which || $e.keyCode]) {
                            return;
                        }
                        _.defer(_.bind(that._onInput, that, $e));
                    });
                }
                this.query = this.$input.val();
                this.$overflowHelper = buildOverflowHelper(this.$input);
            }
            Input.normalizeQuery = function(str) {
                return (str || "").replace(/^\s*/g, "").replace(/\s{2,}/g, " ");
            };
            _.mixin(Input.prototype, EventEmitter, {
                _onBlur: function onBlur() {
                    this.resetInputValue();
                    this.trigger("blurred");
                },
                _onFocus: function onFocus() {
                    this.trigger("focused");
                },
                _onKeydown: function onKeydown($e) {
                    var keyName = specialKeyCodeMap[$e.which || $e.keyCode];
                    this._managePreventDefault(keyName, $e);
                    if (keyName && this._shouldTrigger(keyName, $e)) {
                        this.trigger(keyName + "Keyed", $e);
                    }
                },
                _onInput: function onInput() {
                    this._checkInputValue();
                },
                _managePreventDefault: function managePreventDefault(keyName, $e) {
                    var preventDefault, hintValue, inputValue;
                    switch (keyName) {
                      case "tab":
                        hintValue = this.getHint();
                        inputValue = this.getInputValue();
                        preventDefault = hintValue && hintValue !== inputValue && !withModifier($e);
                        break;

                      case "up":
                      case "down":
                        preventDefault = !withModifier($e);
                        break;

                      default:
                        preventDefault = false;
                    }
                    preventDefault && $e.preventDefault();
                },
                _shouldTrigger: function shouldTrigger(keyName, $e) {
                    var trigger;
                    switch (keyName) {
                      case "tab":
                        trigger = !withModifier($e);
                        break;

                      default:
                        trigger = true;
                    }
                    return trigger;
                },
                _checkInputValue: function checkInputValue() {
                    var inputValue, areEquivalent, hasDifferentWhitespace;
                    inputValue = this.getInputValue();
                    areEquivalent = areQueriesEquivalent(inputValue, this.query);
                    hasDifferentWhitespace = areEquivalent ? this.query.length !== inputValue.length : false;
                    if (!areEquivalent) {
                        this.trigger("queryChanged", this.query = inputValue);
                    } else if (hasDifferentWhitespace) {
                        this.trigger("whitespaceChanged", this.query);
                    }
                },
                focus: function focus() {
                    this.$input.focus();
                },
                blur: function blur() {
                    this.$input.blur();
                },
                getQuery: function getQuery() {
                    return this.query;
                },
                setQuery: function setQuery(query) {
                    this.query = query;
                },
                getInputValue: function getInputValue() {
                    return this.$input.val();
                },
                setInputValue: function setInputValue(value, silent) {
                    this.$input.val(value);
                    silent ? this.clearHint() : this._checkInputValue();
                },
                resetInputValue: function resetInputValue() {
                    this.setInputValue(this.query, true);
                },
                getHint: function getHint() {
                    return this.$hint.val();
                },
                setHint: function setHint(value) {
                    this.$hint.val(value);
                },
                clearHint: function clearHint() {
                    this.setHint("");
                },
                clearHintIfInvalid: function clearHintIfInvalid() {
                    var val, hint, valIsPrefixOfHint, isValid;
                    val = this.getInputValue();
                    hint = this.getHint();
                    valIsPrefixOfHint = val !== hint && hint.indexOf(val) === 0;
                    isValid = val !== "" && valIsPrefixOfHint && !this.hasOverflow();
                    !isValid && this.clearHint();
                },
                getLanguageDirection: function getLanguageDirection() {
                    return (this.$input.css("direction") || "ltr").toLowerCase();
                },
                hasOverflow: function hasOverflow() {
                    var constraint = this.$input.width() - 2;
                    this.$overflowHelper.text(this.getInputValue());
                    return this.$overflowHelper.width() >= constraint;
                },
                isCursorAtEnd: function() {
                    var valueLength, selectionStart, range;
                    valueLength = this.$input.val().length;
                    selectionStart = this.$input[0].selectionStart;
                    if (_.isNumber(selectionStart)) {
                        return selectionStart === valueLength;
                    } else if (document.selection) {
                        range = document.selection.createRange();
                        range.moveStart("character", -valueLength);
                        return valueLength === range.text.length;
                    }
                    return true;
                },
                destroy: function destroy() {
                    this.$hint.off(".tt");
                    this.$input.off(".tt");
                    this.$hint = this.$input = this.$overflowHelper = null;
                }
            });
            return Input;
            function buildOverflowHelper($input) {
                return $('<pre aria-hidden="true"></pre>').css({
                    position: "absolute",
                    visibility: "hidden",
                    whiteSpace: "pre",
                    fontFamily: $input.css("font-family"),
                    fontSize: $input.css("font-size"),
                    fontStyle: $input.css("font-style"),
                    fontVariant: $input.css("font-variant"),
                    fontWeight: $input.css("font-weight"),
                    wordSpacing: $input.css("word-spacing"),
                    letterSpacing: $input.css("letter-spacing"),
                    textIndent: $input.css("text-indent"),
                    textRendering: $input.css("text-rendering"),
                    textTransform: $input.css("text-transform")
                }).insertAfter($input);
            }
            function areQueriesEquivalent(a, b) {
                return Input.normalizeQuery(a) === Input.normalizeQuery(b);
            }
            function withModifier($e) {
                return $e.altKey || $e.ctrlKey || $e.metaKey || $e.shiftKey;
            }
        }();
        var Dataset = function() {
            var datasetKey = "ttDataset", valueKey = "ttValue", datumKey = "ttDatum";
            function Dataset(o) {
                o = o || {};
                o.templates = o.templates || {};
                if (!o.source) {
                    $.error("missing source");
                }
                if (o.name && !isValidName(o.name)) {
                    $.error("invalid dataset name: " + o.name);
                }
                this.query = null;
                this.highlight = !!o.highlight;
                this.name = o.name || _.getUniqueId();
                this.source = o.source;
                this.displayFn = getDisplayFn(o.display || o.displayKey);
                this.templates = getTemplates(o.templates, this.displayFn);
                this.$el = $(html.dataset.replace("%CLASS%", this.name));
            }
            Dataset.extractDatasetName = function extractDatasetName(el) {
                return $(el).data(datasetKey);
            };
            Dataset.extractValue = function extractDatum(el) {
                return $(el).data(valueKey);
            };
            Dataset.extractDatum = function extractDatum(el) {
                return $(el).data(datumKey);
            };
            _.mixin(Dataset.prototype, EventEmitter, {
                _render: function render(query, suggestions) {
                    if (!this.$el) {
                        return;
                    }
                    var that = this, hasSuggestions;
                    this.$el.empty();
                    hasSuggestions = suggestions && suggestions.length;
                    if (!hasSuggestions && this.templates.empty) {
                        this.$el.html(getEmptyHtml()).prepend(that.templates.header ? getHeaderHtml() : null).append(that.templates.footer ? getFooterHtml() : null);
                    } else if (hasSuggestions) {
                        this.$el.html(getSuggestionsHtml()).prepend(that.templates.header ? getHeaderHtml() : null).append(that.templates.footer ? getFooterHtml() : null);
                    }
                    this.trigger("rendered");
                    function getEmptyHtml() {
                        return that.templates.empty({
                            query: query,
                            isEmpty: true
                        });
                    }
                    function getSuggestionsHtml() {
                        var $suggestions, nodes;
                        $suggestions = $(html.suggestions).css(css.suggestions);
                        nodes = _.map(suggestions, getSuggestionNode);
                        $suggestions.append.apply($suggestions, nodes);
                        that.highlight && highlight({
                            node: $suggestions[0],
                            pattern: query
                        });
                        return $suggestions;
                        function getSuggestionNode(suggestion) {
                            var $el;
                            $el = $(html.suggestion).append(that.templates.suggestion(suggestion)).data(datasetKey, that.name).data(valueKey, that.displayFn(suggestion)).data(datumKey, suggestion);
                            $el.children().each(function() {
                                $(this).css(css.suggestionChild);
                            });
                            return $el;
                        }
                    }
                    function getHeaderHtml() {
                        return that.templates.header({
                            query: query,
                            isEmpty: !hasSuggestions
                        });
                    }
                    function getFooterHtml() {
                        return that.templates.footer({
                            query: query,
                            isEmpty: !hasSuggestions
                        });
                    }
                },
                getRoot: function getRoot() {
                    return this.$el;
                },
                update: function update(query) {
                    var that = this;
                    this.query = query;
                    this.canceled = false;
                    this.source(query, render);
                    function render(suggestions) {
                        if (!that.canceled && query === that.query) {
                            that._render(query, suggestions);
                        }
                    }
                },
                cancel: function cancel() {
                    this.canceled = true;
                },
                clear: function clear() {
                    this.cancel();
                    this.$el.empty();
                    this.trigger("rendered");
                },
                isEmpty: function isEmpty() {
                    return this.$el.is(":empty");
                },
                destroy: function destroy() {
                    this.$el = null;
                }
            });
            return Dataset;
            function getDisplayFn(display) {
                display = display || "value";
                return _.isFunction(display) ? display : displayFn;
                function displayFn(obj) {
                    return obj[display];
                }
            }
            function getTemplates(templates, displayFn) {
                return {
                    empty: templates.empty && _.templatify(templates.empty),
                    header: templates.header && _.templatify(templates.header),
                    footer: templates.footer && _.templatify(templates.footer),
                    suggestion: templates.suggestion || suggestionTemplate
                };
                function suggestionTemplate(context) {
                    return "<p>" + displayFn(context) + "</p>";
                }
            }
            function isValidName(str) {
                return /^[_a-zA-Z0-9-]+$/.test(str);
            }
        }();
        var Dropdown = function() {
            function Dropdown(o) {
                var that = this, onSuggestionClick, onSuggestionMouseEnter, onSuggestionMouseLeave;
                o = o || {};
                if (!o.menu) {
                    $.error("menu is required");
                }
                this.isOpen = false;
                this.isEmpty = true;
                this.datasets = _.map(o.datasets, initializeDataset);
                onSuggestionClick = _.bind(this._onSuggestionClick, this);
                onSuggestionMouseEnter = _.bind(this._onSuggestionMouseEnter, this);
                onSuggestionMouseLeave = _.bind(this._onSuggestionMouseLeave, this);
                this.$menu = $(o.menu).on("click.tt", ".tt-suggestion", onSuggestionClick).on("mouseenter.tt", ".tt-suggestion", onSuggestionMouseEnter).on("mouseleave.tt", ".tt-suggestion", onSuggestionMouseLeave);
                _.each(this.datasets, function(dataset) {
                    that.$menu.append(dataset.getRoot());
                    dataset.onSync("rendered", that._onRendered, that);
                });
            }
            _.mixin(Dropdown.prototype, EventEmitter, {
                _onSuggestionClick: function onSuggestionClick($e) {
                    this.trigger("suggestionClicked", $($e.currentTarget));
                },
                _onSuggestionMouseEnter: function onSuggestionMouseEnter($e) {
                    this._removeCursor();
                    this._setCursor($($e.currentTarget), true);
                },
                _onSuggestionMouseLeave: function onSuggestionMouseLeave() {
                    this._removeCursor();
                },
                _onRendered: function onRendered() {
                    this.isEmpty = _.every(this.datasets, isDatasetEmpty);
                    this.isEmpty ? this._hide() : this.isOpen && this._show();
                    this.trigger("datasetRendered");
                    function isDatasetEmpty(dataset) {
                        return dataset.isEmpty();
                    }
                },
                _hide: function() {
                    this.$menu.hide();
                },
                _show: function() {
                    this.$menu.css("display", "block");
                },
                _getSuggestions: function getSuggestions() {
                    return this.$menu.find(".tt-suggestion");
                },
                _getCursor: function getCursor() {
                    return this.$menu.find(".tt-cursor").first();
                },
                _setCursor: function setCursor($el, silent) {
                    $el.first().addClass("tt-cursor");
                    !silent && this.trigger("cursorMoved");
                },
                _removeCursor: function removeCursor() {
                    this._getCursor().removeClass("tt-cursor");
                },
                _moveCursor: function moveCursor(increment) {
                    var $suggestions, $oldCursor, newCursorIndex, $newCursor;
                    if (!this.isOpen) {
                        return;
                    }
                    $oldCursor = this._getCursor();
                    $suggestions = this._getSuggestions();
                    this._removeCursor();
                    newCursorIndex = $suggestions.index($oldCursor) + increment;
                    newCursorIndex = (newCursorIndex + 1) % ($suggestions.length + 1) - 1;
                    if (newCursorIndex === -1) {
                        this.trigger("cursorRemoved");
                        return;
                    } else if (newCursorIndex < -1) {
                        newCursorIndex = $suggestions.length - 1;
                    }
                    this._setCursor($newCursor = $suggestions.eq(newCursorIndex));
                    this._ensureVisible($newCursor);
                },
                _ensureVisible: function ensureVisible($el) {
                    var elTop, elBottom, menuScrollTop, menuHeight;
                    elTop = $el.position().top;
                    elBottom = elTop + $el.outerHeight(true);
                    menuScrollTop = this.$menu.scrollTop();
                    menuHeight = this.$menu.height() + parseInt(this.$menu.css("paddingTop"), 10) + parseInt(this.$menu.css("paddingBottom"), 10);
                    if (elTop < 0) {
                        this.$menu.scrollTop(menuScrollTop + elTop);
                    } else if (menuHeight < elBottom) {
                        this.$menu.scrollTop(menuScrollTop + (elBottom - menuHeight));
                    }
                },
                close: function close() {
                    if (this.isOpen) {
                        this.isOpen = false;
                        this._removeCursor();
                        this._hide();
                        this.trigger("closed");
                    }
                },
                open: function open() {
                    if (!this.isOpen) {
                        this.isOpen = true;
                        !this.isEmpty && this._show();
                        this.trigger("opened");
                    }
                },
                setLanguageDirection: function setLanguageDirection(dir) {
                    this.$menu.css(dir === "ltr" ? css.ltr : css.rtl);
                },
                moveCursorUp: function moveCursorUp() {
                    this._moveCursor(-1);
                },
                moveCursorDown: function moveCursorDown() {
                    this._moveCursor(+1);
                },
                getDatumForSuggestion: function getDatumForSuggestion($el) {
                    var datum = null;
                    if ($el.length) {
                        datum = {
                            raw: Dataset.extractDatum($el),
                            value: Dataset.extractValue($el),
                            datasetName: Dataset.extractDatasetName($el)
                        };
                    }
                    return datum;
                },
                getDatumForCursor: function getDatumForCursor() {
                    return this.getDatumForSuggestion(this._getCursor().first());
                },
                getDatumForTopSuggestion: function getDatumForTopSuggestion() {
                    return this.getDatumForSuggestion(this._getSuggestions().first());
                },
                update: function update(query) {
                    _.each(this.datasets, updateDataset);
                    function updateDataset(dataset) {
                        dataset.update(query);
                    }
                },
                empty: function empty() {
                    _.each(this.datasets, clearDataset);
                    this.isEmpty = true;
                    function clearDataset(dataset) {
                        dataset.clear();
                    }
                },
                isVisible: function isVisible() {
                    return this.isOpen && !this.isEmpty;
                },
                destroy: function destroy() {
                    this.$menu.off(".tt");
                    this.$menu = null;
                    _.each(this.datasets, destroyDataset);
                    function destroyDataset(dataset) {
                        dataset.destroy();
                    }
                }
            });
            return Dropdown;
            function initializeDataset(oDataset) {
                return new Dataset(oDataset);
            }
        }();
        var Typeahead = function() {
            var attrsKey = "ttAttrs";
            function Typeahead(o) {
                var $menu, $input, $hint;
                o = o || {};
                if (!o.input) {
                    $.error("missing input");
                }
                this.isActivated = false;
                this.autoselect = !!o.autoselect;
                this.minLength = _.isNumber(o.minLength) ? o.minLength : 1;
                this.$node = buildDomStructure(o.input, o.withHint);
                $menu = this.$node.find(".tt-dropdown-menu");
                $input = this.$node.find(".tt-input");
                $hint = this.$node.find(".tt-hint");
                $input.on("blur.tt", function($e) {
                    var active, isActive, hasActive;
                    active = document.activeElement;
                    isActive = $menu.is(active);
                    hasActive = $menu.has(active).length > 0;
                    if (_.isMsie() && (isActive || hasActive)) {
                        $e.preventDefault();
                        $e.stopImmediatePropagation();
                        _.defer(function() {
                            $input.focus();
                        });
                    }
                });
                $menu.on("mousedown.tt", function($e) {
                    $e.preventDefault();
                });
                this.eventBus = o.eventBus || new EventBus({
                    el: $input
                });
                this.dropdown = new Dropdown({
                    menu: $menu,
                    datasets: o.datasets
                }).onSync("suggestionClicked", this._onSuggestionClicked, this).onSync("cursorMoved", this._onCursorMoved, this).onSync("cursorRemoved", this._onCursorRemoved, this).onSync("opened", this._onOpened, this).onSync("closed", this._onClosed, this).onAsync("datasetRendered", this._onDatasetRendered, this);
                this.input = new Input({
                    input: $input,
                    hint: $hint
                }).onSync("focused", this._onFocused, this).onSync("blurred", this._onBlurred, this).onSync("enterKeyed", this._onEnterKeyed, this).onSync("tabKeyed", this._onTabKeyed, this).onSync("escKeyed", this._onEscKeyed, this).onSync("upKeyed", this._onUpKeyed, this).onSync("downKeyed", this._onDownKeyed, this).onSync("leftKeyed", this._onLeftKeyed, this).onSync("rightKeyed", this._onRightKeyed, this).onSync("queryChanged", this._onQueryChanged, this).onSync("whitespaceChanged", this._onWhitespaceChanged, this);
                this._setLanguageDirection();
            }
            _.mixin(Typeahead.prototype, {
                _onSuggestionClicked: function onSuggestionClicked(type, $el) {
                    var datum;
                    if (datum = this.dropdown.getDatumForSuggestion($el)) {
                        this._select(datum);
                    }
                },
                _onCursorMoved: function onCursorMoved() {
                    var datum = this.dropdown.getDatumForCursor();
                    this.input.setInputValue(datum.value, true);
                    this.eventBus.trigger("cursorchanged", datum.raw, datum.datasetName);
                },
                _onCursorRemoved: function onCursorRemoved() {
                    this.input.resetInputValue();
                    this._updateHint();
                },
                _onDatasetRendered: function onDatasetRendered() {
                    this._updateHint();
                },
                _onOpened: function onOpened() {
                    this._updateHint();
                    this.eventBus.trigger("opened");
                },
                _onClosed: function onClosed() {
                    this.input.clearHint();
                    this.eventBus.trigger("closed");
                },
                _onFocused: function onFocused() {
                    this.isActivated = true;
                    this.dropdown.open();
                },
                _onBlurred: function onBlurred() {
                    this.isActivated = false;
                    this.dropdown.empty();
                    this.dropdown.close();
                },
                _onEnterKeyed: function onEnterKeyed(type, $e) {
                    var cursorDatum, topSuggestionDatum;
                    cursorDatum = this.dropdown.getDatumForCursor();
                    topSuggestionDatum = this.dropdown.getDatumForTopSuggestion();
                    if (cursorDatum) {
                        this._select(cursorDatum);
                        $e.preventDefault();
                    } else if (this.autoselect && topSuggestionDatum) {
                        this._select(topSuggestionDatum);
                        $e.preventDefault();
                    }
                },
                _onTabKeyed: function onTabKeyed(type, $e) {
                    var datum;
                    if (datum = this.dropdown.getDatumForCursor()) {
                        this._select(datum);
                        $e.preventDefault();
                    } else {
                        this._autocomplete(true);
                    }
                },
                _onEscKeyed: function onEscKeyed() {
                    this.dropdown.close();
                    this.input.resetInputValue();
                },
                _onUpKeyed: function onUpKeyed() {
                    var query = this.input.getQuery();
                    this.dropdown.isEmpty && query.length >= this.minLength ? this.dropdown.update(query) : this.dropdown.moveCursorUp();
                    this.dropdown.open();
                },
                _onDownKeyed: function onDownKeyed() {
                    var query = this.input.getQuery();
                    this.dropdown.isEmpty && query.length >= this.minLength ? this.dropdown.update(query) : this.dropdown.moveCursorDown();
                    this.dropdown.open();
                },
                _onLeftKeyed: function onLeftKeyed() {
                    this.dir === "rtl" && this._autocomplete();
                },
                _onRightKeyed: function onRightKeyed() {
                    this.dir === "ltr" && this._autocomplete();
                },
                _onQueryChanged: function onQueryChanged(e, query) {
                    this.input.clearHintIfInvalid();
                    query.length >= this.minLength ? this.dropdown.update(query) : this.dropdown.empty();
                    this.dropdown.open();
                    this._setLanguageDirection();
                },
                _onWhitespaceChanged: function onWhitespaceChanged() {
                    this._updateHint();
                    this.dropdown.open();
                },
                _setLanguageDirection: function setLanguageDirection() {
                    var dir;
                    if (this.dir !== (dir = this.input.getLanguageDirection())) {
                        this.dir = dir;
                        this.$node.css("direction", dir);
                        this.dropdown.setLanguageDirection(dir);
                    }
                },
                _updateHint: function updateHint() {
                    var datum, val, query, escapedQuery, frontMatchRegEx, match;
                    datum = this.dropdown.getDatumForTopSuggestion();
                    if (datum && this.dropdown.isVisible() && !this.input.hasOverflow()) {
                        val = this.input.getInputValue();
                        query = Input.normalizeQuery(val);
                        escapedQuery = _.escapeRegExChars(query);
                        frontMatchRegEx = new RegExp("^(?:" + escapedQuery + ")(.+$)", "i");
                        match = frontMatchRegEx.exec(datum.value);
                        match ? this.input.setHint(val + match[1]) : this.input.clearHint();
                    } else {
                        this.input.clearHint();
                    }
                },
                _autocomplete: function autocomplete(laxCursor) {
                    var hint, query, isCursorAtEnd, datum;
                    hint = this.input.getHint();
                    query = this.input.getQuery();
                    isCursorAtEnd = laxCursor || this.input.isCursorAtEnd();
                    if (hint && query !== hint && isCursorAtEnd) {
                        datum = this.dropdown.getDatumForTopSuggestion();
                        datum && this.input.setInputValue(datum.value);
                        this.eventBus.trigger("autocompleted", datum.raw, datum.datasetName);
                    }
                },
                _select: function select(datum) {
                    this.input.setQuery(datum.value);
                    this.input.setInputValue(datum.value, true);
                    this._setLanguageDirection();
                    this.eventBus.trigger("selected", datum.raw, datum.datasetName);
                    this.dropdown.close();
                    _.defer(_.bind(this.dropdown.empty, this.dropdown));
                },
                open: function open() {
                    this.dropdown.open();
                },
                close: function close() {
                    this.dropdown.close();
                },
                setVal: function setVal(val) {
                    if (this.isActivated) {
                        this.input.setInputValue(val);
                    } else {
                        this.input.setQuery(val);
                        this.input.setInputValue(val, true);
                    }
                    this._setLanguageDirection();
                },
                getVal: function getVal() {
                    return this.input.getQuery();
                },
                destroy: function destroy() {
                    this.input.destroy();
                    this.dropdown.destroy();
                    destroyDomStructure(this.$node);
                    this.$node = null;
                }
            });
            return Typeahead;
            function buildDomStructure(input, withHint) {
                var $input, $wrapper, $dropdown, $hint;
                $input = $(input);
                $wrapper = $(html.wrapper).css(css.wrapper);
                $dropdown = $(html.dropdown).css(css.dropdown);
                $hint = $input.clone().css(css.hint).css(getBackgroundStyles($input));
                $hint.val("").removeData().addClass("tt-hint").removeAttr("id name placeholder").prop("disabled", true).attr({
                    autocomplete: "off",
                    spellcheck: "false"
                });
                $input.data(attrsKey, {
                    dir: $input.attr("dir"),
                    autocomplete: $input.attr("autocomplete"),
                    spellcheck: $input.attr("spellcheck"),
                    style: $input.attr("style")
                });
                $input.addClass("tt-input").attr({
                    autocomplete: "off",
                    spellcheck: false
                }).css(withHint ? css.input : css.inputWithNoHint);
                try {
                    !$input.attr("dir") && $input.attr("dir", "auto");
                } catch (e) {}
                return $input.wrap($wrapper).parent().prepend(withHint ? $hint : null).append($dropdown);
            }
            function getBackgroundStyles($el) {
                return {
                    backgroundAttachment: $el.css("background-attachment"),
                    backgroundClip: $el.css("background-clip"),
                    backgroundColor: $el.css("background-color"),
                    backgroundImage: $el.css("background-image"),
                    backgroundOrigin: $el.css("background-origin"),
                    backgroundPosition: $el.css("background-position"),
                    backgroundRepeat: $el.css("background-repeat"),
                    backgroundSize: $el.css("background-size")
                };
            }
            function destroyDomStructure($node) {
                var $input = $node.find(".tt-input");
                _.each($input.data(attrsKey), function(val, key) {
                    _.isUndefined(val) ? $input.removeAttr(key) : $input.attr(key, val);
                });
                $input.detach().removeData(attrsKey).removeClass("tt-input").insertAfter($node);
                $node.remove();
            }
        }();
        (function() {
            var old, typeaheadKey, methods;
            old = $.fn.typeahead;
            typeaheadKey = "ttTypeahead";
            methods = {
                initialize: function initialize(o, datasets) {
                    datasets = _.isArray(datasets) ? datasets : [].slice.call(arguments, 1);
                    o = o || {};
                    return this.each(attach);
                    function attach() {
                        var $input = $(this), eventBus, typeahead;
                        _.each(datasets, function(d) {
                            d.highlight = !!o.highlight;
                        });
                        typeahead = new Typeahead({
                            input: $input,
                            eventBus: eventBus = new EventBus({
                                el: $input
                            }),
                            withHint: _.isUndefined(o.hint) ? true : !!o.hint,
                            minLength: o.minLength,
                            autoselect: o.autoselect,
                            datasets: datasets
                        });
                        $input.data(typeaheadKey, typeahead);
                    }
                },
                open: function open() {
                    return this.each(openTypeahead);
                    function openTypeahead() {
                        var $input = $(this), typeahead;
                        if (typeahead = $input.data(typeaheadKey)) {
                            typeahead.open();
                        }
                    }
                },
                close: function close() {
                    return this.each(closeTypeahead);
                    function closeTypeahead() {
                        var $input = $(this), typeahead;
                        if (typeahead = $input.data(typeaheadKey)) {
                            typeahead.close();
                        }
                    }
                },
                val: function val(newVal) {
                    return !arguments.length ? getVal(this.first()) : this.each(setVal);
                    function setVal() {
                        var $input = $(this), typeahead;
                        if (typeahead = $input.data(typeaheadKey)) {
                            typeahead.setVal(newVal);
                        }
                    }
                    function getVal($input) {
                        var typeahead, query;
                        if (typeahead = $input.data(typeaheadKey)) {
                            query = typeahead.getVal();
                        }
                        return query;
                    }
                },
                destroy: function destroy() {
                    return this.each(unattach);
                    function unattach() {
                        var $input = $(this), typeahead;
                        if (typeahead = $input.data(typeaheadKey)) {
                            typeahead.destroy();
                            $input.removeData(typeaheadKey);
                        }
                    }
                }
            };
            $.fn.typeahead = function(method) {
                if (methods[method]) {
                    return methods[method].apply(this, [].slice.call(arguments, 1));
                } else {
                    return methods.initialize.apply(this, arguments);
                }
            };
            $.fn.typeahead.noConflict = function noConflict() {
                $.fn.typeahead = old;
                return this;
            };
        })();
    })(window.jQuery);
});

define("torabot/main/0.1.0/handlebars-v1.3.0-debug", [], function(require, exports, module) {
    /*!

 handlebars v1.3.0

Copyright (C) 2011 by Yehuda Katz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@license
*/
    /* exported Handlebars */
    var Handlebars = function() {
        // handlebars/safe-string.js
        var __module4__ = function() {
            "use strict";
            var __exports__;
            // Build out our basic SafeString type
            function SafeString(string) {
                this.string = string;
            }
            SafeString.prototype.toString = function() {
                return "" + this.string;
            };
            __exports__ = SafeString;
            return __exports__;
        }();
        // handlebars/utils.js
        var __module3__ = function(__dependency1__) {
            "use strict";
            var __exports__ = {};
            /*jshint -W004 */
            var SafeString = __dependency1__;
            var escape = {
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#x27;",
                "`": "&#x60;"
            };
            var badChars = /[&<>"'`]/g;
            var possible = /[&<>"'`]/;
            function escapeChar(chr) {
                return escape[chr] || "&amp;";
            }
            function extend(obj, value) {
                for (var key in value) {
                    if (Object.prototype.hasOwnProperty.call(value, key)) {
                        obj[key] = value[key];
                    }
                }
            }
            __exports__.extend = extend;
            var toString = Object.prototype.toString;
            __exports__.toString = toString;
            // Sourced from lodash
            // https://github.com/bestiejs/lodash/blob/master/LICENSE.txt
            var isFunction = function(value) {
                return typeof value === "function";
            };
            // fallback for older versions of Chrome and Safari
            if (isFunction(/x/)) {
                isFunction = function(value) {
                    return typeof value === "function" && toString.call(value) === "[object Function]";
                };
            }
            var isFunction;
            __exports__.isFunction = isFunction;
            var isArray = Array.isArray || function(value) {
                return value && typeof value === "object" ? toString.call(value) === "[object Array]" : false;
            };
            __exports__.isArray = isArray;
            function escapeExpression(string) {
                // don't escape SafeStrings, since they're already safe
                if (string instanceof SafeString) {
                    return string.toString();
                } else if (!string && string !== 0) {
                    return "";
                }
                // Force a string conversion as this will be done by the append regardless and
                // the regex test will do this transparently behind the scenes, causing issues if
                // an object's to string has escaped characters in it.
                string = "" + string;
                if (!possible.test(string)) {
                    return string;
                }
                return string.replace(badChars, escapeChar);
            }
            __exports__.escapeExpression = escapeExpression;
            function isEmpty(value) {
                if (!value && value !== 0) {
                    return true;
                } else if (isArray(value) && value.length === 0) {
                    return true;
                } else {
                    return false;
                }
            }
            __exports__.isEmpty = isEmpty;
            return __exports__;
        }(__module4__);
        // handlebars/exception.js
        var __module5__ = function() {
            "use strict";
            var __exports__;
            var errorProps = [ "description", "fileName", "lineNumber", "message", "name", "number", "stack" ];
            function Exception(message, node) {
                var line;
                if (node && node.firstLine) {
                    line = node.firstLine;
                    message += " - " + line + ":" + node.firstColumn;
                }
                var tmp = Error.prototype.constructor.call(this, message);
                // Unfortunately errors are not enumerable in Chrome (at least), so `for prop in tmp` doesn't work.
                for (var idx = 0; idx < errorProps.length; idx++) {
                    this[errorProps[idx]] = tmp[errorProps[idx]];
                }
                if (line) {
                    this.lineNumber = line;
                    this.column = node.firstColumn;
                }
            }
            Exception.prototype = new Error();
            __exports__ = Exception;
            return __exports__;
        }();
        // handlebars/base.js
        var __module2__ = function(__dependency1__, __dependency2__) {
            "use strict";
            var __exports__ = {};
            var Utils = __dependency1__;
            var Exception = __dependency2__;
            var VERSION = "1.3.0";
            __exports__.VERSION = VERSION;
            var COMPILER_REVISION = 4;
            __exports__.COMPILER_REVISION = COMPILER_REVISION;
            var REVISION_CHANGES = {
                1: "<= 1.0.rc.2",
                // 1.0.rc.2 is actually rev2 but doesn't report it
                2: "== 1.0.0-rc.3",
                3: "== 1.0.0-rc.4",
                4: ">= 1.0.0"
            };
            __exports__.REVISION_CHANGES = REVISION_CHANGES;
            var isArray = Utils.isArray, isFunction = Utils.isFunction, toString = Utils.toString, objectType = "[object Object]";
            function HandlebarsEnvironment(helpers, partials) {
                this.helpers = helpers || {};
                this.partials = partials || {};
                registerDefaultHelpers(this);
            }
            __exports__.HandlebarsEnvironment = HandlebarsEnvironment;
            HandlebarsEnvironment.prototype = {
                constructor: HandlebarsEnvironment,
                logger: logger,
                log: log,
                registerHelper: function(name, fn, inverse) {
                    if (toString.call(name) === objectType) {
                        if (inverse || fn) {
                            throw new Exception("Arg not supported with multiple helpers");
                        }
                        Utils.extend(this.helpers, name);
                    } else {
                        if (inverse) {
                            fn.not = inverse;
                        }
                        this.helpers[name] = fn;
                    }
                },
                registerPartial: function(name, str) {
                    if (toString.call(name) === objectType) {
                        Utils.extend(this.partials, name);
                    } else {
                        this.partials[name] = str;
                    }
                }
            };
            function registerDefaultHelpers(instance) {
                instance.registerHelper("helperMissing", function(arg) {
                    if (arguments.length === 2) {
                        return undefined;
                    } else {
                        throw new Exception("Missing helper: '" + arg + "'");
                    }
                });
                instance.registerHelper("blockHelperMissing", function(context, options) {
                    var inverse = options.inverse || function() {}, fn = options.fn;
                    if (isFunction(context)) {
                        context = context.call(this);
                    }
                    if (context === true) {
                        return fn(this);
                    } else if (context === false || context == null) {
                        return inverse(this);
                    } else if (isArray(context)) {
                        if (context.length > 0) {
                            return instance.helpers.each(context, options);
                        } else {
                            return inverse(this);
                        }
                    } else {
                        return fn(context);
                    }
                });
                instance.registerHelper("each", function(context, options) {
                    var fn = options.fn, inverse = options.inverse;
                    var i = 0, ret = "", data;
                    if (isFunction(context)) {
                        context = context.call(this);
                    }
                    if (options.data) {
                        data = createFrame(options.data);
                    }
                    if (context && typeof context === "object") {
                        if (isArray(context)) {
                            for (var j = context.length; i < j; i++) {
                                if (data) {
                                    data.index = i;
                                    data.first = i === 0;
                                    data.last = i === context.length - 1;
                                }
                                ret = ret + fn(context[i], {
                                    data: data
                                });
                            }
                        } else {
                            for (var key in context) {
                                if (context.hasOwnProperty(key)) {
                                    if (data) {
                                        data.key = key;
                                        data.index = i;
                                        data.first = i === 0;
                                    }
                                    ret = ret + fn(context[key], {
                                        data: data
                                    });
                                    i++;
                                }
                            }
                        }
                    }
                    if (i === 0) {
                        ret = inverse(this);
                    }
                    return ret;
                });
                instance.registerHelper("if", function(conditional, options) {
                    if (isFunction(conditional)) {
                        conditional = conditional.call(this);
                    }
                    // Default behavior is to render the positive path if the value is truthy and not empty.
                    // The `includeZero` option may be set to treat the condtional as purely not empty based on the
                    // behavior of isEmpty. Effectively this determines if 0 is handled by the positive path or negative.
                    if (!options.hash.includeZero && !conditional || Utils.isEmpty(conditional)) {
                        return options.inverse(this);
                    } else {
                        return options.fn(this);
                    }
                });
                instance.registerHelper("unless", function(conditional, options) {
                    return instance.helpers["if"].call(this, conditional, {
                        fn: options.inverse,
                        inverse: options.fn,
                        hash: options.hash
                    });
                });
                instance.registerHelper("with", function(context, options) {
                    if (isFunction(context)) {
                        context = context.call(this);
                    }
                    if (!Utils.isEmpty(context)) return options.fn(context);
                });
                instance.registerHelper("log", function(context, options) {
                    var level = options.data && options.data.level != null ? parseInt(options.data.level, 10) : 1;
                    instance.log(level, context);
                });
            }
            var logger = {
                methodMap: {
                    0: "debug",
                    1: "info",
                    2: "warn",
                    3: "error"
                },
                // State enum
                DEBUG: 0,
                INFO: 1,
                WARN: 2,
                ERROR: 3,
                level: 3,
                // can be overridden in the host environment
                log: function(level, obj) {
                    if (logger.level <= level) {
                        var method = logger.methodMap[level];
                        if (typeof console !== "undefined" && console[method]) {
                            console[method].call(console, obj);
                        }
                    }
                }
            };
            __exports__.logger = logger;
            function log(level, obj) {
                logger.log(level, obj);
            }
            __exports__.log = log;
            var createFrame = function(object) {
                var obj = {};
                Utils.extend(obj, object);
                return obj;
            };
            __exports__.createFrame = createFrame;
            return __exports__;
        }(__module3__, __module5__);
        // handlebars/runtime.js
        var __module6__ = function(__dependency1__, __dependency2__, __dependency3__) {
            "use strict";
            var __exports__ = {};
            var Utils = __dependency1__;
            var Exception = __dependency2__;
            var COMPILER_REVISION = __dependency3__.COMPILER_REVISION;
            var REVISION_CHANGES = __dependency3__.REVISION_CHANGES;
            function checkRevision(compilerInfo) {
                var compilerRevision = compilerInfo && compilerInfo[0] || 1, currentRevision = COMPILER_REVISION;
                if (compilerRevision !== currentRevision) {
                    if (compilerRevision < currentRevision) {
                        var runtimeVersions = REVISION_CHANGES[currentRevision], compilerVersions = REVISION_CHANGES[compilerRevision];
                        throw new Exception("Template was precompiled with an older version of Handlebars than the current runtime. " + "Please update your precompiler to a newer version (" + runtimeVersions + ") or downgrade your runtime to an older version (" + compilerVersions + ").");
                    } else {
                        // Use the embedded version info since the runtime doesn't know about this revision yet
                        throw new Exception("Template was precompiled with a newer version of Handlebars than the current runtime. " + "Please update your runtime to a newer version (" + compilerInfo[1] + ").");
                    }
                }
            }
            __exports__.checkRevision = checkRevision;
            // TODO: Remove this line and break up compilePartial
            function template(templateSpec, env) {
                if (!env) {
                    throw new Exception("No environment passed to template");
                }
                // Note: Using env.VM references rather than local var references throughout this section to allow
                // for external users to override these as psuedo-supported APIs.
                var invokePartialWrapper = function(partial, name, context, helpers, partials, data) {
                    var result = env.VM.invokePartial.apply(this, arguments);
                    if (result != null) {
                        return result;
                    }
                    if (env.compile) {
                        var options = {
                            helpers: helpers,
                            partials: partials,
                            data: data
                        };
                        partials[name] = env.compile(partial, {
                            data: data !== undefined
                        }, env);
                        return partials[name](context, options);
                    } else {
                        throw new Exception("The partial " + name + " could not be compiled when running in runtime-only mode");
                    }
                };
                // Just add water
                var container = {
                    escapeExpression: Utils.escapeExpression,
                    invokePartial: invokePartialWrapper,
                    programs: [],
                    program: function(i, fn, data) {
                        var programWrapper = this.programs[i];
                        if (data) {
                            programWrapper = program(i, fn, data);
                        } else if (!programWrapper) {
                            programWrapper = this.programs[i] = program(i, fn);
                        }
                        return programWrapper;
                    },
                    merge: function(param, common) {
                        var ret = param || common;
                        if (param && common && param !== common) {
                            ret = {};
                            Utils.extend(ret, common);
                            Utils.extend(ret, param);
                        }
                        return ret;
                    },
                    programWithDepth: env.VM.programWithDepth,
                    noop: env.VM.noop,
                    compilerInfo: null
                };
                return function(context, options) {
                    options = options || {};
                    var namespace = options.partial ? options : env, helpers, partials;
                    if (!options.partial) {
                        helpers = options.helpers;
                        partials = options.partials;
                    }
                    var result = templateSpec.call(container, namespace, context, helpers, partials, options.data);
                    if (!options.partial) {
                        env.VM.checkRevision(container.compilerInfo);
                    }
                    return result;
                };
            }
            __exports__.template = template;
            function programWithDepth(i, fn, data) {
                var args = Array.prototype.slice.call(arguments, 3);
                var prog = function(context, options) {
                    options = options || {};
                    return fn.apply(this, [ context, options.data || data ].concat(args));
                };
                prog.program = i;
                prog.depth = args.length;
                return prog;
            }
            __exports__.programWithDepth = programWithDepth;
            function program(i, fn, data) {
                var prog = function(context, options) {
                    options = options || {};
                    return fn(context, options.data || data);
                };
                prog.program = i;
                prog.depth = 0;
                return prog;
            }
            __exports__.program = program;
            function invokePartial(partial, name, context, helpers, partials, data) {
                var options = {
                    partial: true,
                    helpers: helpers,
                    partials: partials,
                    data: data
                };
                if (partial === undefined) {
                    throw new Exception("The partial " + name + " could not be found");
                } else if (partial instanceof Function) {
                    return partial(context, options);
                }
            }
            __exports__.invokePartial = invokePartial;
            function noop() {
                return "";
            }
            __exports__.noop = noop;
            return __exports__;
        }(__module3__, __module5__, __module2__);
        // handlebars.runtime.js
        var __module1__ = function(__dependency1__, __dependency2__, __dependency3__, __dependency4__, __dependency5__) {
            "use strict";
            var __exports__;
            /*globals Handlebars: true */
            var base = __dependency1__;
            // Each of these augment the Handlebars object. No need to setup here.
            // (This is done to easily share code between commonjs and browse envs)
            var SafeString = __dependency2__;
            var Exception = __dependency3__;
            var Utils = __dependency4__;
            var runtime = __dependency5__;
            // For compatibility and usage outside of module systems, make the Handlebars object a namespace
            var create = function() {
                var hb = new base.HandlebarsEnvironment();
                Utils.extend(hb, base);
                hb.SafeString = SafeString;
                hb.Exception = Exception;
                hb.Utils = Utils;
                hb.VM = runtime;
                hb.template = function(spec) {
                    return runtime.template(spec, hb);
                };
                return hb;
            };
            var Handlebars = create();
            Handlebars.create = create;
            __exports__ = Handlebars;
            return __exports__;
        }(__module2__, __module4__, __module5__, __module3__, __module6__);
        // handlebars/compiler/ast.js
        var __module7__ = function(__dependency1__) {
            "use strict";
            var __exports__;
            var Exception = __dependency1__;
            function LocationInfo(locInfo) {
                locInfo = locInfo || {};
                this.firstLine = locInfo.first_line;
                this.firstColumn = locInfo.first_column;
                this.lastColumn = locInfo.last_column;
                this.lastLine = locInfo.last_line;
            }
            var AST = {
                ProgramNode: function(statements, inverseStrip, inverse, locInfo) {
                    var inverseLocationInfo, firstInverseNode;
                    if (arguments.length === 3) {
                        locInfo = inverse;
                        inverse = null;
                    } else if (arguments.length === 2) {
                        locInfo = inverseStrip;
                        inverseStrip = null;
                    }
                    LocationInfo.call(this, locInfo);
                    this.type = "program";
                    this.statements = statements;
                    this.strip = {};
                    if (inverse) {
                        firstInverseNode = inverse[0];
                        if (firstInverseNode) {
                            inverseLocationInfo = {
                                first_line: firstInverseNode.firstLine,
                                last_line: firstInverseNode.lastLine,
                                last_column: firstInverseNode.lastColumn,
                                first_column: firstInverseNode.firstColumn
                            };
                            this.inverse = new AST.ProgramNode(inverse, inverseStrip, inverseLocationInfo);
                        } else {
                            this.inverse = new AST.ProgramNode(inverse, inverseStrip);
                        }
                        this.strip.right = inverseStrip.left;
                    } else if (inverseStrip) {
                        this.strip.left = inverseStrip.right;
                    }
                },
                MustacheNode: function(rawParams, hash, open, strip, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "mustache";
                    this.strip = strip;
                    // Open may be a string parsed from the parser or a passed boolean flag
                    if (open != null && open.charAt) {
                        // Must use charAt to support IE pre-10
                        var escapeFlag = open.charAt(3) || open.charAt(2);
                        this.escaped = escapeFlag !== "{" && escapeFlag !== "&";
                    } else {
                        this.escaped = !!open;
                    }
                    if (rawParams instanceof AST.SexprNode) {
                        this.sexpr = rawParams;
                    } else {
                        // Support old AST API
                        this.sexpr = new AST.SexprNode(rawParams, hash);
                    }
                    this.sexpr.isRoot = true;
                    // Support old AST API that stored this info in MustacheNode
                    this.id = this.sexpr.id;
                    this.params = this.sexpr.params;
                    this.hash = this.sexpr.hash;
                    this.eligibleHelper = this.sexpr.eligibleHelper;
                    this.isHelper = this.sexpr.isHelper;
                },
                SexprNode: function(rawParams, hash, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "sexpr";
                    this.hash = hash;
                    var id = this.id = rawParams[0];
                    var params = this.params = rawParams.slice(1);
                    // a mustache is an eligible helper if:
                    // * its id is simple (a single part, not `this` or `..`)
                    var eligibleHelper = this.eligibleHelper = id.isSimple;
                    // a mustache is definitely a helper if:
                    // * it is an eligible helper, and
                    // * it has at least one parameter or hash segment
                    this.isHelper = eligibleHelper && (params.length || hash);
                },
                PartialNode: function(partialName, context, strip, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "partial";
                    this.partialName = partialName;
                    this.context = context;
                    this.strip = strip;
                },
                BlockNode: function(mustache, program, inverse, close, locInfo) {
                    LocationInfo.call(this, locInfo);
                    if (mustache.sexpr.id.original !== close.path.original) {
                        throw new Exception(mustache.sexpr.id.original + " doesn't match " + close.path.original, this);
                    }
                    this.type = "block";
                    this.mustache = mustache;
                    this.program = program;
                    this.inverse = inverse;
                    this.strip = {
                        left: mustache.strip.left,
                        right: close.strip.right
                    };
                    (program || inverse).strip.left = mustache.strip.right;
                    (inverse || program).strip.right = close.strip.left;
                    if (inverse && !program) {
                        this.isInverse = true;
                    }
                },
                ContentNode: function(string, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "content";
                    this.string = string;
                },
                HashNode: function(pairs, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "hash";
                    this.pairs = pairs;
                },
                IdNode: function(parts, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "ID";
                    var original = "", dig = [], depth = 0;
                    for (var i = 0, l = parts.length; i < l; i++) {
                        var part = parts[i].part;
                        original += (parts[i].separator || "") + part;
                        if (part === ".." || part === "." || part === "this") {
                            if (dig.length > 0) {
                                throw new Exception("Invalid path: " + original, this);
                            } else if (part === "..") {
                                depth++;
                            } else {
                                this.isScoped = true;
                            }
                        } else {
                            dig.push(part);
                        }
                    }
                    this.original = original;
                    this.parts = dig;
                    this.string = dig.join(".");
                    this.depth = depth;
                    // an ID is simple if it only has one part, and that part is not
                    // `..` or `this`.
                    this.isSimple = parts.length === 1 && !this.isScoped && depth === 0;
                    this.stringModeValue = this.string;
                },
                PartialNameNode: function(name, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "PARTIAL_NAME";
                    this.name = name.original;
                },
                DataNode: function(id, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "DATA";
                    this.id = id;
                },
                StringNode: function(string, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "STRING";
                    this.original = this.string = this.stringModeValue = string;
                },
                IntegerNode: function(integer, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "INTEGER";
                    this.original = this.integer = integer;
                    this.stringModeValue = Number(integer);
                },
                BooleanNode: function(bool, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "BOOLEAN";
                    this.bool = bool;
                    this.stringModeValue = bool === "true";
                },
                CommentNode: function(comment, locInfo) {
                    LocationInfo.call(this, locInfo);
                    this.type = "comment";
                    this.comment = comment;
                }
            };
            // Must be exported as an object rather than the root of the module as the jison lexer
            // most modify the object to operate properly.
            __exports__ = AST;
            return __exports__;
        }(__module5__);
        // handlebars/compiler/parser.js
        var __module9__ = function() {
            "use strict";
            var __exports__;
            /* jshint ignore:start */
            /* Jison generated parser */
            var handlebars = function() {
                var parser = {
                    trace: function trace() {},
                    yy: {},
                    symbols_: {
                        error: 2,
                        root: 3,
                        statements: 4,
                        EOF: 5,
                        program: 6,
                        simpleInverse: 7,
                        statement: 8,
                        openInverse: 9,
                        closeBlock: 10,
                        openBlock: 11,
                        mustache: 12,
                        partial: 13,
                        CONTENT: 14,
                        COMMENT: 15,
                        OPEN_BLOCK: 16,
                        sexpr: 17,
                        CLOSE: 18,
                        OPEN_INVERSE: 19,
                        OPEN_ENDBLOCK: 20,
                        path: 21,
                        OPEN: 22,
                        OPEN_UNESCAPED: 23,
                        CLOSE_UNESCAPED: 24,
                        OPEN_PARTIAL: 25,
                        partialName: 26,
                        partial_option0: 27,
                        sexpr_repetition0: 28,
                        sexpr_option0: 29,
                        dataName: 30,
                        param: 31,
                        STRING: 32,
                        INTEGER: 33,
                        BOOLEAN: 34,
                        OPEN_SEXPR: 35,
                        CLOSE_SEXPR: 36,
                        hash: 37,
                        hash_repetition_plus0: 38,
                        hashSegment: 39,
                        ID: 40,
                        EQUALS: 41,
                        DATA: 42,
                        pathSegments: 43,
                        SEP: 44,
                        $accept: 0,
                        $end: 1
                    },
                    terminals_: {
                        2: "error",
                        5: "EOF",
                        14: "CONTENT",
                        15: "COMMENT",
                        16: "OPEN_BLOCK",
                        18: "CLOSE",
                        19: "OPEN_INVERSE",
                        20: "OPEN_ENDBLOCK",
                        22: "OPEN",
                        23: "OPEN_UNESCAPED",
                        24: "CLOSE_UNESCAPED",
                        25: "OPEN_PARTIAL",
                        32: "STRING",
                        33: "INTEGER",
                        34: "BOOLEAN",
                        35: "OPEN_SEXPR",
                        36: "CLOSE_SEXPR",
                        40: "ID",
                        41: "EQUALS",
                        42: "DATA",
                        44: "SEP"
                    },
                    productions_: [ 0, [ 3, 2 ], [ 3, 1 ], [ 6, 2 ], [ 6, 3 ], [ 6, 2 ], [ 6, 1 ], [ 6, 1 ], [ 6, 0 ], [ 4, 1 ], [ 4, 2 ], [ 8, 3 ], [ 8, 3 ], [ 8, 1 ], [ 8, 1 ], [ 8, 1 ], [ 8, 1 ], [ 11, 3 ], [ 9, 3 ], [ 10, 3 ], [ 12, 3 ], [ 12, 3 ], [ 13, 4 ], [ 7, 2 ], [ 17, 3 ], [ 17, 1 ], [ 31, 1 ], [ 31, 1 ], [ 31, 1 ], [ 31, 1 ], [ 31, 1 ], [ 31, 3 ], [ 37, 1 ], [ 39, 3 ], [ 26, 1 ], [ 26, 1 ], [ 26, 1 ], [ 30, 2 ], [ 21, 1 ], [ 43, 3 ], [ 43, 1 ], [ 27, 0 ], [ 27, 1 ], [ 28, 0 ], [ 28, 2 ], [ 29, 0 ], [ 29, 1 ], [ 38, 1 ], [ 38, 2 ] ],
                    performAction: function anonymous(yytext, yyleng, yylineno, yy, yystate, $$, _$) {
                        var $0 = $$.length - 1;
                        switch (yystate) {
                          case 1:
                            return new yy.ProgramNode($$[$0 - 1], this._$);
                            break;

                          case 2:
                            return new yy.ProgramNode([], this._$);
                            break;

                          case 3:
                            this.$ = new yy.ProgramNode([], $$[$0 - 1], $$[$0], this._$);
                            break;

                          case 4:
                            this.$ = new yy.ProgramNode($$[$0 - 2], $$[$0 - 1], $$[$0], this._$);
                            break;

                          case 5:
                            this.$ = new yy.ProgramNode($$[$0 - 1], $$[$0], [], this._$);
                            break;

                          case 6:
                            this.$ = new yy.ProgramNode($$[$0], this._$);
                            break;

                          case 7:
                            this.$ = new yy.ProgramNode([], this._$);
                            break;

                          case 8:
                            this.$ = new yy.ProgramNode([], this._$);
                            break;

                          case 9:
                            this.$ = [ $$[$0] ];
                            break;

                          case 10:
                            $$[$0 - 1].push($$[$0]);
                            this.$ = $$[$0 - 1];
                            break;

                          case 11:
                            this.$ = new yy.BlockNode($$[$0 - 2], $$[$0 - 1].inverse, $$[$0 - 1], $$[$0], this._$);
                            break;

                          case 12:
                            this.$ = new yy.BlockNode($$[$0 - 2], $$[$0 - 1], $$[$0 - 1].inverse, $$[$0], this._$);
                            break;

                          case 13:
                            this.$ = $$[$0];
                            break;

                          case 14:
                            this.$ = $$[$0];
                            break;

                          case 15:
                            this.$ = new yy.ContentNode($$[$0], this._$);
                            break;

                          case 16:
                            this.$ = new yy.CommentNode($$[$0], this._$);
                            break;

                          case 17:
                            this.$ = new yy.MustacheNode($$[$0 - 1], null, $$[$0 - 2], stripFlags($$[$0 - 2], $$[$0]), this._$);
                            break;

                          case 18:
                            this.$ = new yy.MustacheNode($$[$0 - 1], null, $$[$0 - 2], stripFlags($$[$0 - 2], $$[$0]), this._$);
                            break;

                          case 19:
                            this.$ = {
                                path: $$[$0 - 1],
                                strip: stripFlags($$[$0 - 2], $$[$0])
                            };
                            break;

                          case 20:
                            this.$ = new yy.MustacheNode($$[$0 - 1], null, $$[$0 - 2], stripFlags($$[$0 - 2], $$[$0]), this._$);
                            break;

                          case 21:
                            this.$ = new yy.MustacheNode($$[$0 - 1], null, $$[$0 - 2], stripFlags($$[$0 - 2], $$[$0]), this._$);
                            break;

                          case 22:
                            this.$ = new yy.PartialNode($$[$0 - 2], $$[$0 - 1], stripFlags($$[$0 - 3], $$[$0]), this._$);
                            break;

                          case 23:
                            this.$ = stripFlags($$[$0 - 1], $$[$0]);
                            break;

                          case 24:
                            this.$ = new yy.SexprNode([ $$[$0 - 2] ].concat($$[$0 - 1]), $$[$0], this._$);
                            break;

                          case 25:
                            this.$ = new yy.SexprNode([ $$[$0] ], null, this._$);
                            break;

                          case 26:
                            this.$ = $$[$0];
                            break;

                          case 27:
                            this.$ = new yy.StringNode($$[$0], this._$);
                            break;

                          case 28:
                            this.$ = new yy.IntegerNode($$[$0], this._$);
                            break;

                          case 29:
                            this.$ = new yy.BooleanNode($$[$0], this._$);
                            break;

                          case 30:
                            this.$ = $$[$0];
                            break;

                          case 31:
                            $$[$0 - 1].isHelper = true;
                            this.$ = $$[$0 - 1];
                            break;

                          case 32:
                            this.$ = new yy.HashNode($$[$0], this._$);
                            break;

                          case 33:
                            this.$ = [ $$[$0 - 2], $$[$0] ];
                            break;

                          case 34:
                            this.$ = new yy.PartialNameNode($$[$0], this._$);
                            break;

                          case 35:
                            this.$ = new yy.PartialNameNode(new yy.StringNode($$[$0], this._$), this._$);
                            break;

                          case 36:
                            this.$ = new yy.PartialNameNode(new yy.IntegerNode($$[$0], this._$));
                            break;

                          case 37:
                            this.$ = new yy.DataNode($$[$0], this._$);
                            break;

                          case 38:
                            this.$ = new yy.IdNode($$[$0], this._$);
                            break;

                          case 39:
                            $$[$0 - 2].push({
                                part: $$[$0],
                                separator: $$[$0 - 1]
                            });
                            this.$ = $$[$0 - 2];
                            break;

                          case 40:
                            this.$ = [ {
                                part: $$[$0]
                            } ];
                            break;

                          case 43:
                            this.$ = [];
                            break;

                          case 44:
                            $$[$0 - 1].push($$[$0]);
                            break;

                          case 47:
                            this.$ = [ $$[$0] ];
                            break;

                          case 48:
                            $$[$0 - 1].push($$[$0]);
                            break;
                        }
                    },
                    table: [ {
                        3: 1,
                        4: 2,
                        5: [ 1, 3 ],
                        8: 4,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 11 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        1: [ 3 ]
                    }, {
                        5: [ 1, 16 ],
                        8: 17,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 11 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        1: [ 2, 2 ]
                    }, {
                        5: [ 2, 9 ],
                        14: [ 2, 9 ],
                        15: [ 2, 9 ],
                        16: [ 2, 9 ],
                        19: [ 2, 9 ],
                        20: [ 2, 9 ],
                        22: [ 2, 9 ],
                        23: [ 2, 9 ],
                        25: [ 2, 9 ]
                    }, {
                        4: 20,
                        6: 18,
                        7: 19,
                        8: 4,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 21 ],
                        20: [ 2, 8 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        4: 20,
                        6: 22,
                        7: 19,
                        8: 4,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 21 ],
                        20: [ 2, 8 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        5: [ 2, 13 ],
                        14: [ 2, 13 ],
                        15: [ 2, 13 ],
                        16: [ 2, 13 ],
                        19: [ 2, 13 ],
                        20: [ 2, 13 ],
                        22: [ 2, 13 ],
                        23: [ 2, 13 ],
                        25: [ 2, 13 ]
                    }, {
                        5: [ 2, 14 ],
                        14: [ 2, 14 ],
                        15: [ 2, 14 ],
                        16: [ 2, 14 ],
                        19: [ 2, 14 ],
                        20: [ 2, 14 ],
                        22: [ 2, 14 ],
                        23: [ 2, 14 ],
                        25: [ 2, 14 ]
                    }, {
                        5: [ 2, 15 ],
                        14: [ 2, 15 ],
                        15: [ 2, 15 ],
                        16: [ 2, 15 ],
                        19: [ 2, 15 ],
                        20: [ 2, 15 ],
                        22: [ 2, 15 ],
                        23: [ 2, 15 ],
                        25: [ 2, 15 ]
                    }, {
                        5: [ 2, 16 ],
                        14: [ 2, 16 ],
                        15: [ 2, 16 ],
                        16: [ 2, 16 ],
                        19: [ 2, 16 ],
                        20: [ 2, 16 ],
                        22: [ 2, 16 ],
                        23: [ 2, 16 ],
                        25: [ 2, 16 ]
                    }, {
                        17: 23,
                        21: 24,
                        30: 25,
                        40: [ 1, 28 ],
                        42: [ 1, 27 ],
                        43: 26
                    }, {
                        17: 29,
                        21: 24,
                        30: 25,
                        40: [ 1, 28 ],
                        42: [ 1, 27 ],
                        43: 26
                    }, {
                        17: 30,
                        21: 24,
                        30: 25,
                        40: [ 1, 28 ],
                        42: [ 1, 27 ],
                        43: 26
                    }, {
                        17: 31,
                        21: 24,
                        30: 25,
                        40: [ 1, 28 ],
                        42: [ 1, 27 ],
                        43: 26
                    }, {
                        21: 33,
                        26: 32,
                        32: [ 1, 34 ],
                        33: [ 1, 35 ],
                        40: [ 1, 28 ],
                        43: 26
                    }, {
                        1: [ 2, 1 ]
                    }, {
                        5: [ 2, 10 ],
                        14: [ 2, 10 ],
                        15: [ 2, 10 ],
                        16: [ 2, 10 ],
                        19: [ 2, 10 ],
                        20: [ 2, 10 ],
                        22: [ 2, 10 ],
                        23: [ 2, 10 ],
                        25: [ 2, 10 ]
                    }, {
                        10: 36,
                        20: [ 1, 37 ]
                    }, {
                        4: 38,
                        8: 4,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 11 ],
                        20: [ 2, 7 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        7: 39,
                        8: 17,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 21 ],
                        20: [ 2, 6 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        17: 23,
                        18: [ 1, 40 ],
                        21: 24,
                        30: 25,
                        40: [ 1, 28 ],
                        42: [ 1, 27 ],
                        43: 26
                    }, {
                        10: 41,
                        20: [ 1, 37 ]
                    }, {
                        18: [ 1, 42 ]
                    }, {
                        18: [ 2, 43 ],
                        24: [ 2, 43 ],
                        28: 43,
                        32: [ 2, 43 ],
                        33: [ 2, 43 ],
                        34: [ 2, 43 ],
                        35: [ 2, 43 ],
                        36: [ 2, 43 ],
                        40: [ 2, 43 ],
                        42: [ 2, 43 ]
                    }, {
                        18: [ 2, 25 ],
                        24: [ 2, 25 ],
                        36: [ 2, 25 ]
                    }, {
                        18: [ 2, 38 ],
                        24: [ 2, 38 ],
                        32: [ 2, 38 ],
                        33: [ 2, 38 ],
                        34: [ 2, 38 ],
                        35: [ 2, 38 ],
                        36: [ 2, 38 ],
                        40: [ 2, 38 ],
                        42: [ 2, 38 ],
                        44: [ 1, 44 ]
                    }, {
                        21: 45,
                        40: [ 1, 28 ],
                        43: 26
                    }, {
                        18: [ 2, 40 ],
                        24: [ 2, 40 ],
                        32: [ 2, 40 ],
                        33: [ 2, 40 ],
                        34: [ 2, 40 ],
                        35: [ 2, 40 ],
                        36: [ 2, 40 ],
                        40: [ 2, 40 ],
                        42: [ 2, 40 ],
                        44: [ 2, 40 ]
                    }, {
                        18: [ 1, 46 ]
                    }, {
                        18: [ 1, 47 ]
                    }, {
                        24: [ 1, 48 ]
                    }, {
                        18: [ 2, 41 ],
                        21: 50,
                        27: 49,
                        40: [ 1, 28 ],
                        43: 26
                    }, {
                        18: [ 2, 34 ],
                        40: [ 2, 34 ]
                    }, {
                        18: [ 2, 35 ],
                        40: [ 2, 35 ]
                    }, {
                        18: [ 2, 36 ],
                        40: [ 2, 36 ]
                    }, {
                        5: [ 2, 11 ],
                        14: [ 2, 11 ],
                        15: [ 2, 11 ],
                        16: [ 2, 11 ],
                        19: [ 2, 11 ],
                        20: [ 2, 11 ],
                        22: [ 2, 11 ],
                        23: [ 2, 11 ],
                        25: [ 2, 11 ]
                    }, {
                        21: 51,
                        40: [ 1, 28 ],
                        43: 26
                    }, {
                        8: 17,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 11 ],
                        20: [ 2, 3 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        4: 52,
                        8: 4,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 11 ],
                        20: [ 2, 5 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        14: [ 2, 23 ],
                        15: [ 2, 23 ],
                        16: [ 2, 23 ],
                        19: [ 2, 23 ],
                        20: [ 2, 23 ],
                        22: [ 2, 23 ],
                        23: [ 2, 23 ],
                        25: [ 2, 23 ]
                    }, {
                        5: [ 2, 12 ],
                        14: [ 2, 12 ],
                        15: [ 2, 12 ],
                        16: [ 2, 12 ],
                        19: [ 2, 12 ],
                        20: [ 2, 12 ],
                        22: [ 2, 12 ],
                        23: [ 2, 12 ],
                        25: [ 2, 12 ]
                    }, {
                        14: [ 2, 18 ],
                        15: [ 2, 18 ],
                        16: [ 2, 18 ],
                        19: [ 2, 18 ],
                        20: [ 2, 18 ],
                        22: [ 2, 18 ],
                        23: [ 2, 18 ],
                        25: [ 2, 18 ]
                    }, {
                        18: [ 2, 45 ],
                        21: 56,
                        24: [ 2, 45 ],
                        29: 53,
                        30: 60,
                        31: 54,
                        32: [ 1, 57 ],
                        33: [ 1, 58 ],
                        34: [ 1, 59 ],
                        35: [ 1, 61 ],
                        36: [ 2, 45 ],
                        37: 55,
                        38: 62,
                        39: 63,
                        40: [ 1, 64 ],
                        42: [ 1, 27 ],
                        43: 26
                    }, {
                        40: [ 1, 65 ]
                    }, {
                        18: [ 2, 37 ],
                        24: [ 2, 37 ],
                        32: [ 2, 37 ],
                        33: [ 2, 37 ],
                        34: [ 2, 37 ],
                        35: [ 2, 37 ],
                        36: [ 2, 37 ],
                        40: [ 2, 37 ],
                        42: [ 2, 37 ]
                    }, {
                        14: [ 2, 17 ],
                        15: [ 2, 17 ],
                        16: [ 2, 17 ],
                        19: [ 2, 17 ],
                        20: [ 2, 17 ],
                        22: [ 2, 17 ],
                        23: [ 2, 17 ],
                        25: [ 2, 17 ]
                    }, {
                        5: [ 2, 20 ],
                        14: [ 2, 20 ],
                        15: [ 2, 20 ],
                        16: [ 2, 20 ],
                        19: [ 2, 20 ],
                        20: [ 2, 20 ],
                        22: [ 2, 20 ],
                        23: [ 2, 20 ],
                        25: [ 2, 20 ]
                    }, {
                        5: [ 2, 21 ],
                        14: [ 2, 21 ],
                        15: [ 2, 21 ],
                        16: [ 2, 21 ],
                        19: [ 2, 21 ],
                        20: [ 2, 21 ],
                        22: [ 2, 21 ],
                        23: [ 2, 21 ],
                        25: [ 2, 21 ]
                    }, {
                        18: [ 1, 66 ]
                    }, {
                        18: [ 2, 42 ]
                    }, {
                        18: [ 1, 67 ]
                    }, {
                        8: 17,
                        9: 5,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: [ 1, 9 ],
                        15: [ 1, 10 ],
                        16: [ 1, 12 ],
                        19: [ 1, 11 ],
                        20: [ 2, 4 ],
                        22: [ 1, 13 ],
                        23: [ 1, 14 ],
                        25: [ 1, 15 ]
                    }, {
                        18: [ 2, 24 ],
                        24: [ 2, 24 ],
                        36: [ 2, 24 ]
                    }, {
                        18: [ 2, 44 ],
                        24: [ 2, 44 ],
                        32: [ 2, 44 ],
                        33: [ 2, 44 ],
                        34: [ 2, 44 ],
                        35: [ 2, 44 ],
                        36: [ 2, 44 ],
                        40: [ 2, 44 ],
                        42: [ 2, 44 ]
                    }, {
                        18: [ 2, 46 ],
                        24: [ 2, 46 ],
                        36: [ 2, 46 ]
                    }, {
                        18: [ 2, 26 ],
                        24: [ 2, 26 ],
                        32: [ 2, 26 ],
                        33: [ 2, 26 ],
                        34: [ 2, 26 ],
                        35: [ 2, 26 ],
                        36: [ 2, 26 ],
                        40: [ 2, 26 ],
                        42: [ 2, 26 ]
                    }, {
                        18: [ 2, 27 ],
                        24: [ 2, 27 ],
                        32: [ 2, 27 ],
                        33: [ 2, 27 ],
                        34: [ 2, 27 ],
                        35: [ 2, 27 ],
                        36: [ 2, 27 ],
                        40: [ 2, 27 ],
                        42: [ 2, 27 ]
                    }, {
                        18: [ 2, 28 ],
                        24: [ 2, 28 ],
                        32: [ 2, 28 ],
                        33: [ 2, 28 ],
                        34: [ 2, 28 ],
                        35: [ 2, 28 ],
                        36: [ 2, 28 ],
                        40: [ 2, 28 ],
                        42: [ 2, 28 ]
                    }, {
                        18: [ 2, 29 ],
                        24: [ 2, 29 ],
                        32: [ 2, 29 ],
                        33: [ 2, 29 ],
                        34: [ 2, 29 ],
                        35: [ 2, 29 ],
                        36: [ 2, 29 ],
                        40: [ 2, 29 ],
                        42: [ 2, 29 ]
                    }, {
                        18: [ 2, 30 ],
                        24: [ 2, 30 ],
                        32: [ 2, 30 ],
                        33: [ 2, 30 ],
                        34: [ 2, 30 ],
                        35: [ 2, 30 ],
                        36: [ 2, 30 ],
                        40: [ 2, 30 ],
                        42: [ 2, 30 ]
                    }, {
                        17: 68,
                        21: 24,
                        30: 25,
                        40: [ 1, 28 ],
                        42: [ 1, 27 ],
                        43: 26
                    }, {
                        18: [ 2, 32 ],
                        24: [ 2, 32 ],
                        36: [ 2, 32 ],
                        39: 69,
                        40: [ 1, 70 ]
                    }, {
                        18: [ 2, 47 ],
                        24: [ 2, 47 ],
                        36: [ 2, 47 ],
                        40: [ 2, 47 ]
                    }, {
                        18: [ 2, 40 ],
                        24: [ 2, 40 ],
                        32: [ 2, 40 ],
                        33: [ 2, 40 ],
                        34: [ 2, 40 ],
                        35: [ 2, 40 ],
                        36: [ 2, 40 ],
                        40: [ 2, 40 ],
                        41: [ 1, 71 ],
                        42: [ 2, 40 ],
                        44: [ 2, 40 ]
                    }, {
                        18: [ 2, 39 ],
                        24: [ 2, 39 ],
                        32: [ 2, 39 ],
                        33: [ 2, 39 ],
                        34: [ 2, 39 ],
                        35: [ 2, 39 ],
                        36: [ 2, 39 ],
                        40: [ 2, 39 ],
                        42: [ 2, 39 ],
                        44: [ 2, 39 ]
                    }, {
                        5: [ 2, 22 ],
                        14: [ 2, 22 ],
                        15: [ 2, 22 ],
                        16: [ 2, 22 ],
                        19: [ 2, 22 ],
                        20: [ 2, 22 ],
                        22: [ 2, 22 ],
                        23: [ 2, 22 ],
                        25: [ 2, 22 ]
                    }, {
                        5: [ 2, 19 ],
                        14: [ 2, 19 ],
                        15: [ 2, 19 ],
                        16: [ 2, 19 ],
                        19: [ 2, 19 ],
                        20: [ 2, 19 ],
                        22: [ 2, 19 ],
                        23: [ 2, 19 ],
                        25: [ 2, 19 ]
                    }, {
                        36: [ 1, 72 ]
                    }, {
                        18: [ 2, 48 ],
                        24: [ 2, 48 ],
                        36: [ 2, 48 ],
                        40: [ 2, 48 ]
                    }, {
                        41: [ 1, 71 ]
                    }, {
                        21: 56,
                        30: 60,
                        31: 73,
                        32: [ 1, 57 ],
                        33: [ 1, 58 ],
                        34: [ 1, 59 ],
                        35: [ 1, 61 ],
                        40: [ 1, 28 ],
                        42: [ 1, 27 ],
                        43: 26
                    }, {
                        18: [ 2, 31 ],
                        24: [ 2, 31 ],
                        32: [ 2, 31 ],
                        33: [ 2, 31 ],
                        34: [ 2, 31 ],
                        35: [ 2, 31 ],
                        36: [ 2, 31 ],
                        40: [ 2, 31 ],
                        42: [ 2, 31 ]
                    }, {
                        18: [ 2, 33 ],
                        24: [ 2, 33 ],
                        36: [ 2, 33 ],
                        40: [ 2, 33 ]
                    } ],
                    defaultActions: {
                        3: [ 2, 2 ],
                        16: [ 2, 1 ],
                        50: [ 2, 42 ]
                    },
                    parseError: function parseError(str, hash) {
                        throw new Error(str);
                    },
                    parse: function parse(input) {
                        var self = this, stack = [ 0 ], vstack = [ null ], lstack = [], table = this.table, yytext = "", yylineno = 0, yyleng = 0, recovering = 0, TERROR = 2, EOF = 1;
                        this.lexer.setInput(input);
                        this.lexer.yy = this.yy;
                        this.yy.lexer = this.lexer;
                        this.yy.parser = this;
                        if (typeof this.lexer.yylloc == "undefined") this.lexer.yylloc = {};
                        var yyloc = this.lexer.yylloc;
                        lstack.push(yyloc);
                        var ranges = this.lexer.options && this.lexer.options.ranges;
                        if (typeof this.yy.parseError === "function") this.parseError = this.yy.parseError;
                        function popStack(n) {
                            stack.length = stack.length - 2 * n;
                            vstack.length = vstack.length - n;
                            lstack.length = lstack.length - n;
                        }
                        function lex() {
                            var token;
                            token = self.lexer.lex() || 1;
                            if (typeof token !== "number") {
                                token = self.symbols_[token] || token;
                            }
                            return token;
                        }
                        var symbol, preErrorSymbol, state, action, a, r, yyval = {}, p, len, newState, expected;
                        while (true) {
                            state = stack[stack.length - 1];
                            if (this.defaultActions[state]) {
                                action = this.defaultActions[state];
                            } else {
                                if (symbol === null || typeof symbol == "undefined") {
                                    symbol = lex();
                                }
                                action = table[state] && table[state][symbol];
                            }
                            if (typeof action === "undefined" || !action.length || !action[0]) {
                                var errStr = "";
                                if (!recovering) {
                                    expected = [];
                                    for (p in table[state]) if (this.terminals_[p] && p > 2) {
                                        expected.push("'" + this.terminals_[p] + "'");
                                    }
                                    if (this.lexer.showPosition) {
                                        errStr = "Parse error on line " + (yylineno + 1) + ":\n" + this.lexer.showPosition() + "\nExpecting " + expected.join(", ") + ", got '" + (this.terminals_[symbol] || symbol) + "'";
                                    } else {
                                        errStr = "Parse error on line " + (yylineno + 1) + ": Unexpected " + (symbol == 1 ? "end of input" : "'" + (this.terminals_[symbol] || symbol) + "'");
                                    }
                                    this.parseError(errStr, {
                                        text: this.lexer.match,
                                        token: this.terminals_[symbol] || symbol,
                                        line: this.lexer.yylineno,
                                        loc: yyloc,
                                        expected: expected
                                    });
                                }
                            }
                            if (action[0] instanceof Array && action.length > 1) {
                                throw new Error("Parse Error: multiple actions possible at state: " + state + ", token: " + symbol);
                            }
                            switch (action[0]) {
                              case 1:
                                stack.push(symbol);
                                vstack.push(this.lexer.yytext);
                                lstack.push(this.lexer.yylloc);
                                stack.push(action[1]);
                                symbol = null;
                                if (!preErrorSymbol) {
                                    yyleng = this.lexer.yyleng;
                                    yytext = this.lexer.yytext;
                                    yylineno = this.lexer.yylineno;
                                    yyloc = this.lexer.yylloc;
                                    if (recovering > 0) recovering--;
                                } else {
                                    symbol = preErrorSymbol;
                                    preErrorSymbol = null;
                                }
                                break;

                              case 2:
                                len = this.productions_[action[1]][1];
                                yyval.$ = vstack[vstack.length - len];
                                yyval._$ = {
                                    first_line: lstack[lstack.length - (len || 1)].first_line,
                                    last_line: lstack[lstack.length - 1].last_line,
                                    first_column: lstack[lstack.length - (len || 1)].first_column,
                                    last_column: lstack[lstack.length - 1].last_column
                                };
                                if (ranges) {
                                    yyval._$.range = [ lstack[lstack.length - (len || 1)].range[0], lstack[lstack.length - 1].range[1] ];
                                }
                                r = this.performAction.call(yyval, yytext, yyleng, yylineno, this.yy, action[1], vstack, lstack);
                                if (typeof r !== "undefined") {
                                    return r;
                                }
                                if (len) {
                                    stack = stack.slice(0, -1 * len * 2);
                                    vstack = vstack.slice(0, -1 * len);
                                    lstack = lstack.slice(0, -1 * len);
                                }
                                stack.push(this.productions_[action[1]][0]);
                                vstack.push(yyval.$);
                                lstack.push(yyval._$);
                                newState = table[stack[stack.length - 2]][stack[stack.length - 1]];
                                stack.push(newState);
                                break;

                              case 3:
                                return true;
                            }
                        }
                        return true;
                    }
                };
                function stripFlags(open, close) {
                    return {
                        left: open.charAt(2) === "~",
                        right: close.charAt(0) === "~" || close.charAt(1) === "~"
                    };
                }
                /* Jison generated lexer */
                var lexer = function() {
                    var lexer = {
                        EOF: 1,
                        parseError: function parseError(str, hash) {
                            if (this.yy.parser) {
                                this.yy.parser.parseError(str, hash);
                            } else {
                                throw new Error(str);
                            }
                        },
                        setInput: function(input) {
                            this._input = input;
                            this._more = this._less = this.done = false;
                            this.yylineno = this.yyleng = 0;
                            this.yytext = this.matched = this.match = "";
                            this.conditionStack = [ "INITIAL" ];
                            this.yylloc = {
                                first_line: 1,
                                first_column: 0,
                                last_line: 1,
                                last_column: 0
                            };
                            if (this.options.ranges) this.yylloc.range = [ 0, 0 ];
                            this.offset = 0;
                            return this;
                        },
                        input: function() {
                            var ch = this._input[0];
                            this.yytext += ch;
                            this.yyleng++;
                            this.offset++;
                            this.match += ch;
                            this.matched += ch;
                            var lines = ch.match(/(?:\r\n?|\n).*/g);
                            if (lines) {
                                this.yylineno++;
                                this.yylloc.last_line++;
                            } else {
                                this.yylloc.last_column++;
                            }
                            if (this.options.ranges) this.yylloc.range[1]++;
                            this._input = this._input.slice(1);
                            return ch;
                        },
                        unput: function(ch) {
                            var len = ch.length;
                            var lines = ch.split(/(?:\r\n?|\n)/g);
                            this._input = ch + this._input;
                            this.yytext = this.yytext.substr(0, this.yytext.length - len - 1);
                            //this.yyleng -= len;
                            this.offset -= len;
                            var oldLines = this.match.split(/(?:\r\n?|\n)/g);
                            this.match = this.match.substr(0, this.match.length - 1);
                            this.matched = this.matched.substr(0, this.matched.length - 1);
                            if (lines.length - 1) this.yylineno -= lines.length - 1;
                            var r = this.yylloc.range;
                            this.yylloc = {
                                first_line: this.yylloc.first_line,
                                last_line: this.yylineno + 1,
                                first_column: this.yylloc.first_column,
                                last_column: lines ? (lines.length === oldLines.length ? this.yylloc.first_column : 0) + oldLines[oldLines.length - lines.length].length - lines[0].length : this.yylloc.first_column - len
                            };
                            if (this.options.ranges) {
                                this.yylloc.range = [ r[0], r[0] + this.yyleng - len ];
                            }
                            return this;
                        },
                        more: function() {
                            this._more = true;
                            return this;
                        },
                        less: function(n) {
                            this.unput(this.match.slice(n));
                        },
                        pastInput: function() {
                            var past = this.matched.substr(0, this.matched.length - this.match.length);
                            return (past.length > 20 ? "..." : "") + past.substr(-20).replace(/\n/g, "");
                        },
                        upcomingInput: function() {
                            var next = this.match;
                            if (next.length < 20) {
                                next += this._input.substr(0, 20 - next.length);
                            }
                            return (next.substr(0, 20) + (next.length > 20 ? "..." : "")).replace(/\n/g, "");
                        },
                        showPosition: function() {
                            var pre = this.pastInput();
                            var c = new Array(pre.length + 1).join("-");
                            return pre + this.upcomingInput() + "\n" + c + "^";
                        },
                        next: function() {
                            if (this.done) {
                                return this.EOF;
                            }
                            if (!this._input) this.done = true;
                            var token, match, tempMatch, index, col, lines;
                            if (!this._more) {
                                this.yytext = "";
                                this.match = "";
                            }
                            var rules = this._currentRules();
                            for (var i = 0; i < rules.length; i++) {
                                tempMatch = this._input.match(this.rules[rules[i]]);
                                if (tempMatch && (!match || tempMatch[0].length > match[0].length)) {
                                    match = tempMatch;
                                    index = i;
                                    if (!this.options.flex) break;
                                }
                            }
                            if (match) {
                                lines = match[0].match(/(?:\r\n?|\n).*/g);
                                if (lines) this.yylineno += lines.length;
                                this.yylloc = {
                                    first_line: this.yylloc.last_line,
                                    last_line: this.yylineno + 1,
                                    first_column: this.yylloc.last_column,
                                    last_column: lines ? lines[lines.length - 1].length - lines[lines.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + match[0].length
                                };
                                this.yytext += match[0];
                                this.match += match[0];
                                this.matches = match;
                                this.yyleng = this.yytext.length;
                                if (this.options.ranges) {
                                    this.yylloc.range = [ this.offset, this.offset += this.yyleng ];
                                }
                                this._more = false;
                                this._input = this._input.slice(match[0].length);
                                this.matched += match[0];
                                token = this.performAction.call(this, this.yy, this, rules[index], this.conditionStack[this.conditionStack.length - 1]);
                                if (this.done && this._input) this.done = false;
                                if (token) return token; else return;
                            }
                            if (this._input === "") {
                                return this.EOF;
                            } else {
                                return this.parseError("Lexical error on line " + (this.yylineno + 1) + ". Unrecognized text.\n" + this.showPosition(), {
                                    text: "",
                                    token: null,
                                    line: this.yylineno
                                });
                            }
                        },
                        lex: function lex() {
                            var r = this.next();
                            if (typeof r !== "undefined") {
                                return r;
                            } else {
                                return this.lex();
                            }
                        },
                        begin: function begin(condition) {
                            this.conditionStack.push(condition);
                        },
                        popState: function popState() {
                            return this.conditionStack.pop();
                        },
                        _currentRules: function _currentRules() {
                            return this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules;
                        },
                        topState: function() {
                            return this.conditionStack[this.conditionStack.length - 2];
                        },
                        pushState: function begin(condition) {
                            this.begin(condition);
                        }
                    };
                    lexer.options = {};
                    lexer.performAction = function anonymous(yy, yy_, $avoiding_name_collisions, YY_START) {
                        function strip(start, end) {
                            return yy_.yytext = yy_.yytext.substr(start, yy_.yyleng - end);
                        }
                        var YYSTATE = YY_START;
                        switch ($avoiding_name_collisions) {
                          case 0:
                            if (yy_.yytext.slice(-2) === "\\\\") {
                                strip(0, 1);
                                this.begin("mu");
                            } else if (yy_.yytext.slice(-1) === "\\") {
                                strip(0, 1);
                                this.begin("emu");
                            } else {
                                this.begin("mu");
                            }
                            if (yy_.yytext) return 14;
                            break;

                          case 1:
                            return 14;
                            break;

                          case 2:
                            this.popState();
                            return 14;
                            break;

                          case 3:
                            strip(0, 4);
                            this.popState();
                            return 15;
                            break;

                          case 4:
                            return 35;
                            break;

                          case 5:
                            return 36;
                            break;

                          case 6:
                            return 25;
                            break;

                          case 7:
                            return 16;
                            break;

                          case 8:
                            return 20;
                            break;

                          case 9:
                            return 19;
                            break;

                          case 10:
                            return 19;
                            break;

                          case 11:
                            return 23;
                            break;

                          case 12:
                            return 22;
                            break;

                          case 13:
                            this.popState();
                            this.begin("com");
                            break;

                          case 14:
                            strip(3, 5);
                            this.popState();
                            return 15;
                            break;

                          case 15:
                            return 22;
                            break;

                          case 16:
                            return 41;
                            break;

                          case 17:
                            return 40;
                            break;

                          case 18:
                            return 40;
                            break;

                          case 19:
                            return 44;
                            break;

                          case 20:
                            // ignore whitespace
                            break;

                          case 21:
                            this.popState();
                            return 24;
                            break;

                          case 22:
                            this.popState();
                            return 18;
                            break;

                          case 23:
                            yy_.yytext = strip(1, 2).replace(/\\"/g, '"');
                            return 32;
                            break;

                          case 24:
                            yy_.yytext = strip(1, 2).replace(/\\'/g, "'");
                            return 32;
                            break;

                          case 25:
                            return 42;
                            break;

                          case 26:
                            return 34;
                            break;

                          case 27:
                            return 34;
                            break;

                          case 28:
                            return 33;
                            break;

                          case 29:
                            return 40;
                            break;

                          case 30:
                            yy_.yytext = strip(1, 2);
                            return 40;
                            break;

                          case 31:
                            return "INVALID";
                            break;

                          case 32:
                            return 5;
                            break;
                        }
                    };
                    lexer.rules = [ /^(?:[^\x00]*?(?=(\{\{)))/, /^(?:[^\x00]+)/, /^(?:[^\x00]{2,}?(?=(\{\{|\\\{\{|\\\\\{\{|$)))/, /^(?:[\s\S]*?--\}\})/, /^(?:\()/, /^(?:\))/, /^(?:\{\{(~)?>)/, /^(?:\{\{(~)?#)/, /^(?:\{\{(~)?\/)/, /^(?:\{\{(~)?\^)/, /^(?:\{\{(~)?\s*else\b)/, /^(?:\{\{(~)?\{)/, /^(?:\{\{(~)?&)/, /^(?:\{\{!--)/, /^(?:\{\{![\s\S]*?\}\})/, /^(?:\{\{(~)?)/, /^(?:=)/, /^(?:\.\.)/, /^(?:\.(?=([=~}\s\/.)])))/, /^(?:[\/.])/, /^(?:\s+)/, /^(?:\}(~)?\}\})/, /^(?:(~)?\}\})/, /^(?:"(\\["]|[^"])*")/, /^(?:'(\\[']|[^'])*')/, /^(?:@)/, /^(?:true(?=([~}\s)])))/, /^(?:false(?=([~}\s)])))/, /^(?:-?[0-9]+(?=([~}\s)])))/, /^(?:([^\s!"#%-,\.\/;->@\[-\^`\{-~]+(?=([=~}\s\/.)]))))/, /^(?:\[[^\]]*\])/, /^(?:.)/, /^(?:$)/ ];
                    lexer.conditions = {
                        mu: {
                            rules: [ 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32 ],
                            inclusive: false
                        },
                        emu: {
                            rules: [ 2 ],
                            inclusive: false
                        },
                        com: {
                            rules: [ 3 ],
                            inclusive: false
                        },
                        INITIAL: {
                            rules: [ 0, 1, 32 ],
                            inclusive: true
                        }
                    };
                    return lexer;
                }();
                parser.lexer = lexer;
                function Parser() {
                    this.yy = {};
                }
                Parser.prototype = parser;
                parser.Parser = Parser;
                return new Parser();
            }();
            __exports__ = handlebars;
            /* jshint ignore:end */
            return __exports__;
        }();
        // handlebars/compiler/base.js
        var __module8__ = function(__dependency1__, __dependency2__) {
            "use strict";
            var __exports__ = {};
            var parser = __dependency1__;
            var AST = __dependency2__;
            __exports__.parser = parser;
            function parse(input) {
                // Just return if an already-compile AST was passed in.
                if (input.constructor === AST.ProgramNode) {
                    return input;
                }
                parser.yy = AST;
                return parser.parse(input);
            }
            __exports__.parse = parse;
            return __exports__;
        }(__module9__, __module7__);
        // handlebars/compiler/compiler.js
        var __module10__ = function(__dependency1__) {
            "use strict";
            var __exports__ = {};
            var Exception = __dependency1__;
            function Compiler() {}
            __exports__.Compiler = Compiler;
            // the foundHelper register will disambiguate helper lookup from finding a
            // function in a context. This is necessary for mustache compatibility, which
            // requires that context functions in blocks are evaluated by blockHelperMissing,
            // and then proceed as if the resulting value was provided to blockHelperMissing.
            Compiler.prototype = {
                compiler: Compiler,
                disassemble: function() {
                    var opcodes = this.opcodes, opcode, out = [], params, param;
                    for (var i = 0, l = opcodes.length; i < l; i++) {
                        opcode = opcodes[i];
                        if (opcode.opcode === "DECLARE") {
                            out.push("DECLARE " + opcode.name + "=" + opcode.value);
                        } else {
                            params = [];
                            for (var j = 0; j < opcode.args.length; j++) {
                                param = opcode.args[j];
                                if (typeof param === "string") {
                                    param = '"' + param.replace("\n", "\\n") + '"';
                                }
                                params.push(param);
                            }
                            out.push(opcode.opcode + " " + params.join(" "));
                        }
                    }
                    return out.join("\n");
                },
                equals: function(other) {
                    var len = this.opcodes.length;
                    if (other.opcodes.length !== len) {
                        return false;
                    }
                    for (var i = 0; i < len; i++) {
                        var opcode = this.opcodes[i], otherOpcode = other.opcodes[i];
                        if (opcode.opcode !== otherOpcode.opcode || opcode.args.length !== otherOpcode.args.length) {
                            return false;
                        }
                        for (var j = 0; j < opcode.args.length; j++) {
                            if (opcode.args[j] !== otherOpcode.args[j]) {
                                return false;
                            }
                        }
                    }
                    len = this.children.length;
                    if (other.children.length !== len) {
                        return false;
                    }
                    for (i = 0; i < len; i++) {
                        if (!this.children[i].equals(other.children[i])) {
                            return false;
                        }
                    }
                    return true;
                },
                guid: 0,
                compile: function(program, options) {
                    this.opcodes = [];
                    this.children = [];
                    this.depths = {
                        list: []
                    };
                    this.options = options;
                    // These changes will propagate to the other compiler components
                    var knownHelpers = this.options.knownHelpers;
                    this.options.knownHelpers = {
                        helperMissing: true,
                        blockHelperMissing: true,
                        each: true,
                        "if": true,
                        unless: true,
                        "with": true,
                        log: true
                    };
                    if (knownHelpers) {
                        for (var name in knownHelpers) {
                            this.options.knownHelpers[name] = knownHelpers[name];
                        }
                    }
                    return this.accept(program);
                },
                accept: function(node) {
                    var strip = node.strip || {}, ret;
                    if (strip.left) {
                        this.opcode("strip");
                    }
                    ret = this[node.type](node);
                    if (strip.right) {
                        this.opcode("strip");
                    }
                    return ret;
                },
                program: function(program) {
                    var statements = program.statements;
                    for (var i = 0, l = statements.length; i < l; i++) {
                        this.accept(statements[i]);
                    }
                    this.isSimple = l === 1;
                    this.depths.list = this.depths.list.sort(function(a, b) {
                        return a - b;
                    });
                    return this;
                },
                compileProgram: function(program) {
                    var result = new this.compiler().compile(program, this.options);
                    var guid = this.guid++, depth;
                    this.usePartial = this.usePartial || result.usePartial;
                    this.children[guid] = result;
                    for (var i = 0, l = result.depths.list.length; i < l; i++) {
                        depth = result.depths.list[i];
                        if (depth < 2) {
                            continue;
                        } else {
                            this.addDepth(depth - 1);
                        }
                    }
                    return guid;
                },
                block: function(block) {
                    var mustache = block.mustache, program = block.program, inverse = block.inverse;
                    if (program) {
                        program = this.compileProgram(program);
                    }
                    if (inverse) {
                        inverse = this.compileProgram(inverse);
                    }
                    var sexpr = mustache.sexpr;
                    var type = this.classifySexpr(sexpr);
                    if (type === "helper") {
                        this.helperSexpr(sexpr, program, inverse);
                    } else if (type === "simple") {
                        this.simpleSexpr(sexpr);
                        // now that the simple mustache is resolved, we need to
                        // evaluate it by executing `blockHelperMissing`
                        this.opcode("pushProgram", program);
                        this.opcode("pushProgram", inverse);
                        this.opcode("emptyHash");
                        this.opcode("blockValue");
                    } else {
                        this.ambiguousSexpr(sexpr, program, inverse);
                        // now that the simple mustache is resolved, we need to
                        // evaluate it by executing `blockHelperMissing`
                        this.opcode("pushProgram", program);
                        this.opcode("pushProgram", inverse);
                        this.opcode("emptyHash");
                        this.opcode("ambiguousBlockValue");
                    }
                    this.opcode("append");
                },
                hash: function(hash) {
                    var pairs = hash.pairs, pair, val;
                    this.opcode("pushHash");
                    for (var i = 0, l = pairs.length; i < l; i++) {
                        pair = pairs[i];
                        val = pair[1];
                        if (this.options.stringParams) {
                            if (val.depth) {
                                this.addDepth(val.depth);
                            }
                            this.opcode("getContext", val.depth || 0);
                            this.opcode("pushStringParam", val.stringModeValue, val.type);
                            if (val.type === "sexpr") {
                                // Subexpressions get evaluated and passed in
                                // in string params mode.
                                this.sexpr(val);
                            }
                        } else {
                            this.accept(val);
                        }
                        this.opcode("assignToHash", pair[0]);
                    }
                    this.opcode("popHash");
                },
                partial: function(partial) {
                    var partialName = partial.partialName;
                    this.usePartial = true;
                    if (partial.context) {
                        this.ID(partial.context);
                    } else {
                        this.opcode("push", "depth0");
                    }
                    this.opcode("invokePartial", partialName.name);
                    this.opcode("append");
                },
                content: function(content) {
                    this.opcode("appendContent", content.string);
                },
                mustache: function(mustache) {
                    this.sexpr(mustache.sexpr);
                    if (mustache.escaped && !this.options.noEscape) {
                        this.opcode("appendEscaped");
                    } else {
                        this.opcode("append");
                    }
                },
                ambiguousSexpr: function(sexpr, program, inverse) {
                    var id = sexpr.id, name = id.parts[0], isBlock = program != null || inverse != null;
                    this.opcode("getContext", id.depth);
                    this.opcode("pushProgram", program);
                    this.opcode("pushProgram", inverse);
                    this.opcode("invokeAmbiguous", name, isBlock);
                },
                simpleSexpr: function(sexpr) {
                    var id = sexpr.id;
                    if (id.type === "DATA") {
                        this.DATA(id);
                    } else if (id.parts.length) {
                        this.ID(id);
                    } else {
                        // Simplified ID for `this`
                        this.addDepth(id.depth);
                        this.opcode("getContext", id.depth);
                        this.opcode("pushContext");
                    }
                    this.opcode("resolvePossibleLambda");
                },
                helperSexpr: function(sexpr, program, inverse) {
                    var params = this.setupFullMustacheParams(sexpr, program, inverse), name = sexpr.id.parts[0];
                    if (this.options.knownHelpers[name]) {
                        this.opcode("invokeKnownHelper", params.length, name);
                    } else if (this.options.knownHelpersOnly) {
                        throw new Exception("You specified knownHelpersOnly, but used the unknown helper " + name, sexpr);
                    } else {
                        this.opcode("invokeHelper", params.length, name, sexpr.isRoot);
                    }
                },
                sexpr: function(sexpr) {
                    var type = this.classifySexpr(sexpr);
                    if (type === "simple") {
                        this.simpleSexpr(sexpr);
                    } else if (type === "helper") {
                        this.helperSexpr(sexpr);
                    } else {
                        this.ambiguousSexpr(sexpr);
                    }
                },
                ID: function(id) {
                    this.addDepth(id.depth);
                    this.opcode("getContext", id.depth);
                    var name = id.parts[0];
                    if (!name) {
                        this.opcode("pushContext");
                    } else {
                        this.opcode("lookupOnContext", id.parts[0]);
                    }
                    for (var i = 1, l = id.parts.length; i < l; i++) {
                        this.opcode("lookup", id.parts[i]);
                    }
                },
                DATA: function(data) {
                    this.options.data = true;
                    if (data.id.isScoped || data.id.depth) {
                        throw new Exception("Scoped data references are not supported: " + data.original, data);
                    }
                    this.opcode("lookupData");
                    var parts = data.id.parts;
                    for (var i = 0, l = parts.length; i < l; i++) {
                        this.opcode("lookup", parts[i]);
                    }
                },
                STRING: function(string) {
                    this.opcode("pushString", string.string);
                },
                INTEGER: function(integer) {
                    this.opcode("pushLiteral", integer.integer);
                },
                BOOLEAN: function(bool) {
                    this.opcode("pushLiteral", bool.bool);
                },
                comment: function() {},
                // HELPERS
                opcode: function(name) {
                    this.opcodes.push({
                        opcode: name,
                        args: [].slice.call(arguments, 1)
                    });
                },
                declare: function(name, value) {
                    this.opcodes.push({
                        opcode: "DECLARE",
                        name: name,
                        value: value
                    });
                },
                addDepth: function(depth) {
                    if (depth === 0) {
                        return;
                    }
                    if (!this.depths[depth]) {
                        this.depths[depth] = true;
                        this.depths.list.push(depth);
                    }
                },
                classifySexpr: function(sexpr) {
                    var isHelper = sexpr.isHelper;
                    var isEligible = sexpr.eligibleHelper;
                    var options = this.options;
                    // if ambiguous, we can possibly resolve the ambiguity now
                    if (isEligible && !isHelper) {
                        var name = sexpr.id.parts[0];
                        if (options.knownHelpers[name]) {
                            isHelper = true;
                        } else if (options.knownHelpersOnly) {
                            isEligible = false;
                        }
                    }
                    if (isHelper) {
                        return "helper";
                    } else if (isEligible) {
                        return "ambiguous";
                    } else {
                        return "simple";
                    }
                },
                pushParams: function(params) {
                    var i = params.length, param;
                    while (i--) {
                        param = params[i];
                        if (this.options.stringParams) {
                            if (param.depth) {
                                this.addDepth(param.depth);
                            }
                            this.opcode("getContext", param.depth || 0);
                            this.opcode("pushStringParam", param.stringModeValue, param.type);
                            if (param.type === "sexpr") {
                                // Subexpressions get evaluated and passed in
                                // in string params mode.
                                this.sexpr(param);
                            }
                        } else {
                            this[param.type](param);
                        }
                    }
                },
                setupFullMustacheParams: function(sexpr, program, inverse) {
                    var params = sexpr.params;
                    this.pushParams(params);
                    this.opcode("pushProgram", program);
                    this.opcode("pushProgram", inverse);
                    if (sexpr.hash) {
                        this.hash(sexpr.hash);
                    } else {
                        this.opcode("emptyHash");
                    }
                    return params;
                }
            };
            function precompile(input, options, env) {
                if (input == null || typeof input !== "string" && input.constructor !== env.AST.ProgramNode) {
                    throw new Exception("You must pass a string or Handlebars AST to Handlebars.precompile. You passed " + input);
                }
                options = options || {};
                if (!("data" in options)) {
                    options.data = true;
                }
                var ast = env.parse(input);
                var environment = new env.Compiler().compile(ast, options);
                return new env.JavaScriptCompiler().compile(environment, options);
            }
            __exports__.precompile = precompile;
            function compile(input, options, env) {
                if (input == null || typeof input !== "string" && input.constructor !== env.AST.ProgramNode) {
                    throw new Exception("You must pass a string or Handlebars AST to Handlebars.compile. You passed " + input);
                }
                options = options || {};
                if (!("data" in options)) {
                    options.data = true;
                }
                var compiled;
                function compileInput() {
                    var ast = env.parse(input);
                    var environment = new env.Compiler().compile(ast, options);
                    var templateSpec = new env.JavaScriptCompiler().compile(environment, options, undefined, true);
                    return env.template(templateSpec);
                }
                // Template is only compiled on first use and cached after that point.
                return function(context, options) {
                    if (!compiled) {
                        compiled = compileInput();
                    }
                    return compiled.call(this, context, options);
                };
            }
            __exports__.compile = compile;
            return __exports__;
        }(__module5__);
        // handlebars/compiler/javascript-compiler.js
        var __module11__ = function(__dependency1__, __dependency2__) {
            "use strict";
            var __exports__;
            var COMPILER_REVISION = __dependency1__.COMPILER_REVISION;
            var REVISION_CHANGES = __dependency1__.REVISION_CHANGES;
            var log = __dependency1__.log;
            var Exception = __dependency2__;
            function Literal(value) {
                this.value = value;
            }
            function JavaScriptCompiler() {}
            JavaScriptCompiler.prototype = {
                // PUBLIC API: You can override these methods in a subclass to provide
                // alternative compiled forms for name lookup and buffering semantics
                nameLookup: function(parent, name) {
                    var wrap, ret;
                    if (parent.indexOf("depth") === 0) {
                        wrap = true;
                    }
                    if (/^[0-9]+$/.test(name)) {
                        ret = parent + "[" + name + "]";
                    } else if (JavaScriptCompiler.isValidJavaScriptVariableName(name)) {
                        ret = parent + "." + name;
                    } else {
                        ret = parent + "['" + name + "']";
                    }
                    if (wrap) {
                        return "(" + parent + " && " + ret + ")";
                    } else {
                        return ret;
                    }
                },
                compilerInfo: function() {
                    var revision = COMPILER_REVISION, versions = REVISION_CHANGES[revision];
                    return "this.compilerInfo = [" + revision + ",'" + versions + "'];\n";
                },
                appendToBuffer: function(string) {
                    if (this.environment.isSimple) {
                        return "return " + string + ";";
                    } else {
                        return {
                            appendToBuffer: true,
                            content: string,
                            toString: function() {
                                return "buffer += " + string + ";";
                            }
                        };
                    }
                },
                initializeBuffer: function() {
                    return this.quotedString("");
                },
                namespace: "Handlebars",
                // END PUBLIC API
                compile: function(environment, options, context, asObject) {
                    this.environment = environment;
                    this.options = options || {};
                    log("debug", this.environment.disassemble() + "\n\n");
                    this.name = this.environment.name;
                    this.isChild = !!context;
                    this.context = context || {
                        programs: [],
                        environments: [],
                        aliases: {}
                    };
                    this.preamble();
                    this.stackSlot = 0;
                    this.stackVars = [];
                    this.registers = {
                        list: []
                    };
                    this.hashes = [];
                    this.compileStack = [];
                    this.inlineStack = [];
                    this.compileChildren(environment, options);
                    var opcodes = environment.opcodes, opcode;
                    this.i = 0;
                    for (var l = opcodes.length; this.i < l; this.i++) {
                        opcode = opcodes[this.i];
                        if (opcode.opcode === "DECLARE") {
                            this[opcode.name] = opcode.value;
                        } else {
                            this[opcode.opcode].apply(this, opcode.args);
                        }
                        // Reset the stripNext flag if it was not set by this operation.
                        if (opcode.opcode !== this.stripNext) {
                            this.stripNext = false;
                        }
                    }
                    // Flush any trailing content that might be pending.
                    this.pushSource("");
                    if (this.stackSlot || this.inlineStack.length || this.compileStack.length) {
                        throw new Exception("Compile completed with content left on stack");
                    }
                    return this.createFunctionContext(asObject);
                },
                preamble: function() {
                    var out = [];
                    if (!this.isChild) {
                        var namespace = this.namespace;
                        var copies = "helpers = this.merge(helpers, " + namespace + ".helpers);";
                        if (this.environment.usePartial) {
                            copies = copies + " partials = this.merge(partials, " + namespace + ".partials);";
                        }
                        if (this.options.data) {
                            copies = copies + " data = data || {};";
                        }
                        out.push(copies);
                    } else {
                        out.push("");
                    }
                    if (!this.environment.isSimple) {
                        out.push(", buffer = " + this.initializeBuffer());
                    } else {
                        out.push("");
                    }
                    // track the last context pushed into place to allow skipping the
                    // getContext opcode when it would be a noop
                    this.lastContext = 0;
                    this.source = out;
                },
                createFunctionContext: function(asObject) {
                    var locals = this.stackVars.concat(this.registers.list);
                    if (locals.length > 0) {
                        this.source[1] = this.source[1] + ", " + locals.join(", ");
                    }
                    // Generate minimizer alias mappings
                    if (!this.isChild) {
                        for (var alias in this.context.aliases) {
                            if (this.context.aliases.hasOwnProperty(alias)) {
                                this.source[1] = this.source[1] + ", " + alias + "=" + this.context.aliases[alias];
                            }
                        }
                    }
                    if (this.source[1]) {
                        this.source[1] = "var " + this.source[1].substring(2) + ";";
                    }
                    // Merge children
                    if (!this.isChild) {
                        this.source[1] += "\n" + this.context.programs.join("\n") + "\n";
                    }
                    if (!this.environment.isSimple) {
                        this.pushSource("return buffer;");
                    }
                    var params = this.isChild ? [ "depth0", "data" ] : [ "Handlebars", "depth0", "helpers", "partials", "data" ];
                    for (var i = 0, l = this.environment.depths.list.length; i < l; i++) {
                        params.push("depth" + this.environment.depths.list[i]);
                    }
                    // Perform a second pass over the output to merge content when possible
                    var source = this.mergeSource();
                    if (!this.isChild) {
                        source = this.compilerInfo() + source;
                    }
                    if (asObject) {
                        params.push(source);
                        return Function.apply(this, params);
                    } else {
                        var functionSource = "function " + (this.name || "") + "(" + params.join(",") + ") {\n  " + source + "}";
                        log("debug", functionSource + "\n\n");
                        return functionSource;
                    }
                },
                mergeSource: function() {
                    // WARN: We are not handling the case where buffer is still populated as the source should
                    // not have buffer append operations as their final action.
                    var source = "", buffer;
                    for (var i = 0, len = this.source.length; i < len; i++) {
                        var line = this.source[i];
                        if (line.appendToBuffer) {
                            if (buffer) {
                                buffer = buffer + "\n    + " + line.content;
                            } else {
                                buffer = line.content;
                            }
                        } else {
                            if (buffer) {
                                source += "buffer += " + buffer + ";\n  ";
                                buffer = undefined;
                            }
                            source += line + "\n  ";
                        }
                    }
                    return source;
                },
                // [blockValue]
                //
                // On stack, before: hash, inverse, program, value
                // On stack, after: return value of blockHelperMissing
                //
                // The purpose of this opcode is to take a block of the form
                // `{{#foo}}...{{/foo}}`, resolve the value of `foo`, and
                // replace it on the stack with the result of properly
                // invoking blockHelperMissing.
                blockValue: function() {
                    this.context.aliases.blockHelperMissing = "helpers.blockHelperMissing";
                    var params = [ "depth0" ];
                    this.setupParams(0, params);
                    this.replaceStack(function(current) {
                        params.splice(1, 0, current);
                        return "blockHelperMissing.call(" + params.join(", ") + ")";
                    });
                },
                // [ambiguousBlockValue]
                //
                // On stack, before: hash, inverse, program, value
                // Compiler value, before: lastHelper=value of last found helper, if any
                // On stack, after, if no lastHelper: same as [blockValue]
                // On stack, after, if lastHelper: value
                ambiguousBlockValue: function() {
                    this.context.aliases.blockHelperMissing = "helpers.blockHelperMissing";
                    var params = [ "depth0" ];
                    this.setupParams(0, params);
                    var current = this.topStack();
                    params.splice(1, 0, current);
                    this.pushSource("if (!" + this.lastHelper + ") { " + current + " = blockHelperMissing.call(" + params.join(", ") + "); }");
                },
                // [appendContent]
                //
                // On stack, before: ...
                // On stack, after: ...
                //
                // Appends the string value of `content` to the current buffer
                appendContent: function(content) {
                    if (this.pendingContent) {
                        content = this.pendingContent + content;
                    }
                    if (this.stripNext) {
                        content = content.replace(/^\s+/, "");
                    }
                    this.pendingContent = content;
                },
                // [strip]
                //
                // On stack, before: ...
                // On stack, after: ...
                //
                // Removes any trailing whitespace from the prior content node and flags
                // the next operation for stripping if it is a content node.
                strip: function() {
                    if (this.pendingContent) {
                        this.pendingContent = this.pendingContent.replace(/\s+$/, "");
                    }
                    this.stripNext = "strip";
                },
                // [append]
                //
                // On stack, before: value, ...
                // On stack, after: ...
                //
                // Coerces `value` to a String and appends it to the current buffer.
                //
                // If `value` is truthy, or 0, it is coerced into a string and appended
                // Otherwise, the empty string is appended
                append: function() {
                    // Force anything that is inlined onto the stack so we don't have duplication
                    // when we examine local
                    this.flushInline();
                    var local = this.popStack();
                    this.pushSource("if(" + local + " || " + local + " === 0) { " + this.appendToBuffer(local) + " }");
                    if (this.environment.isSimple) {
                        this.pushSource("else { " + this.appendToBuffer("''") + " }");
                    }
                },
                // [appendEscaped]
                //
                // On stack, before: value, ...
                // On stack, after: ...
                //
                // Escape `value` and append it to the buffer
                appendEscaped: function() {
                    this.context.aliases.escapeExpression = "this.escapeExpression";
                    this.pushSource(this.appendToBuffer("escapeExpression(" + this.popStack() + ")"));
                },
                // [getContext]
                //
                // On stack, before: ...
                // On stack, after: ...
                // Compiler value, after: lastContext=depth
                //
                // Set the value of the `lastContext` compiler value to the depth
                getContext: function(depth) {
                    if (this.lastContext !== depth) {
                        this.lastContext = depth;
                    }
                },
                // [lookupOnContext]
                //
                // On stack, before: ...
                // On stack, after: currentContext[name], ...
                //
                // Looks up the value of `name` on the current context and pushes
                // it onto the stack.
                lookupOnContext: function(name) {
                    this.push(this.nameLookup("depth" + this.lastContext, name, "context"));
                },
                // [pushContext]
                //
                // On stack, before: ...
                // On stack, after: currentContext, ...
                //
                // Pushes the value of the current context onto the stack.
                pushContext: function() {
                    this.pushStackLiteral("depth" + this.lastContext);
                },
                // [resolvePossibleLambda]
                //
                // On stack, before: value, ...
                // On stack, after: resolved value, ...
                //
                // If the `value` is a lambda, replace it on the stack by
                // the return value of the lambda
                resolvePossibleLambda: function() {
                    this.context.aliases.functionType = '"function"';
                    this.replaceStack(function(current) {
                        return "typeof " + current + " === functionType ? " + current + ".apply(depth0) : " + current;
                    });
                },
                // [lookup]
                //
                // On stack, before: value, ...
                // On stack, after: value[name], ...
                //
                // Replace the value on the stack with the result of looking
                // up `name` on `value`
                lookup: function(name) {
                    this.replaceStack(function(current) {
                        return current + " == null || " + current + " === false ? " + current + " : " + this.nameLookup(current, name, "context");
                    });
                },
                // [lookupData]
                //
                // On stack, before: ...
                // On stack, after: data, ...
                //
                // Push the data lookup operator
                lookupData: function() {
                    this.pushStackLiteral("data");
                },
                // [pushStringParam]
                //
                // On stack, before: ...
                // On stack, after: string, currentContext, ...
                //
                // This opcode is designed for use in string mode, which
                // provides the string value of a parameter along with its
                // depth rather than resolving it immediately.
                pushStringParam: function(string, type) {
                    this.pushStackLiteral("depth" + this.lastContext);
                    this.pushString(type);
                    // If it's a subexpression, the string result
                    // will be pushed after this opcode.
                    if (type !== "sexpr") {
                        if (typeof string === "string") {
                            this.pushString(string);
                        } else {
                            this.pushStackLiteral(string);
                        }
                    }
                },
                emptyHash: function() {
                    this.pushStackLiteral("{}");
                    if (this.options.stringParams) {
                        this.push("{}");
                        // hashContexts
                        this.push("{}");
                    }
                },
                pushHash: function() {
                    if (this.hash) {
                        this.hashes.push(this.hash);
                    }
                    this.hash = {
                        values: [],
                        types: [],
                        contexts: []
                    };
                },
                popHash: function() {
                    var hash = this.hash;
                    this.hash = this.hashes.pop();
                    if (this.options.stringParams) {
                        this.push("{" + hash.contexts.join(",") + "}");
                        this.push("{" + hash.types.join(",") + "}");
                    }
                    this.push("{\n    " + hash.values.join(",\n    ") + "\n  }");
                },
                // [pushString]
                //
                // On stack, before: ...
                // On stack, after: quotedString(string), ...
                //
                // Push a quoted version of `string` onto the stack
                pushString: function(string) {
                    this.pushStackLiteral(this.quotedString(string));
                },
                // [push]
                //
                // On stack, before: ...
                // On stack, after: expr, ...
                //
                // Push an expression onto the stack
                push: function(expr) {
                    this.inlineStack.push(expr);
                    return expr;
                },
                // [pushLiteral]
                //
                // On stack, before: ...
                // On stack, after: value, ...
                //
                // Pushes a value onto the stack. This operation prevents
                // the compiler from creating a temporary variable to hold
                // it.
                pushLiteral: function(value) {
                    this.pushStackLiteral(value);
                },
                // [pushProgram]
                //
                // On stack, before: ...
                // On stack, after: program(guid), ...
                //
                // Push a program expression onto the stack. This takes
                // a compile-time guid and converts it into a runtime-accessible
                // expression.
                pushProgram: function(guid) {
                    if (guid != null) {
                        this.pushStackLiteral(this.programExpression(guid));
                    } else {
                        this.pushStackLiteral(null);
                    }
                },
                // [invokeHelper]
                //
                // On stack, before: hash, inverse, program, params..., ...
                // On stack, after: result of helper invocation
                //
                // Pops off the helper's parameters, invokes the helper,
                // and pushes the helper's return value onto the stack.
                //
                // If the helper is not found, `helperMissing` is called.
                invokeHelper: function(paramSize, name, isRoot) {
                    this.context.aliases.helperMissing = "helpers.helperMissing";
                    this.useRegister("helper");
                    var helper = this.lastHelper = this.setupHelper(paramSize, name, true);
                    var nonHelper = this.nameLookup("depth" + this.lastContext, name, "context");
                    var lookup = "helper = " + helper.name + " || " + nonHelper;
                    if (helper.paramsInit) {
                        lookup += "," + helper.paramsInit;
                    }
                    this.push("(" + lookup + ",helper " + "? helper.call(" + helper.callParams + ") " + ": helperMissing.call(" + helper.helperMissingParams + "))");
                    // Always flush subexpressions. This is both to prevent the compounding size issue that
                    // occurs when the code has to be duplicated for inlining and also to prevent errors
                    // due to the incorrect options object being passed due to the shared register.
                    if (!isRoot) {
                        this.flushInline();
                    }
                },
                // [invokeKnownHelper]
                //
                // On stack, before: hash, inverse, program, params..., ...
                // On stack, after: result of helper invocation
                //
                // This operation is used when the helper is known to exist,
                // so a `helperMissing` fallback is not required.
                invokeKnownHelper: function(paramSize, name) {
                    var helper = this.setupHelper(paramSize, name);
                    this.push(helper.name + ".call(" + helper.callParams + ")");
                },
                // [invokeAmbiguous]
                //
                // On stack, before: hash, inverse, program, params..., ...
                // On stack, after: result of disambiguation
                //
                // This operation is used when an expression like `{{foo}}`
                // is provided, but we don't know at compile-time whether it
                // is a helper or a path.
                //
                // This operation emits more code than the other options,
                // and can be avoided by passing the `knownHelpers` and
                // `knownHelpersOnly` flags at compile-time.
                invokeAmbiguous: function(name, helperCall) {
                    this.context.aliases.functionType = '"function"';
                    this.useRegister("helper");
                    this.emptyHash();
                    var helper = this.setupHelper(0, name, helperCall);
                    var helperName = this.lastHelper = this.nameLookup("helpers", name, "helper");
                    var nonHelper = this.nameLookup("depth" + this.lastContext, name, "context");
                    var nextStack = this.nextStack();
                    if (helper.paramsInit) {
                        this.pushSource(helper.paramsInit);
                    }
                    this.pushSource("if (helper = " + helperName + ") { " + nextStack + " = helper.call(" + helper.callParams + "); }");
                    this.pushSource("else { helper = " + nonHelper + "; " + nextStack + " = typeof helper === functionType ? helper.call(" + helper.callParams + ") : helper; }");
                },
                // [invokePartial]
                //
                // On stack, before: context, ...
                // On stack after: result of partial invocation
                //
                // This operation pops off a context, invokes a partial with that context,
                // and pushes the result of the invocation back.
                invokePartial: function(name) {
                    var params = [ this.nameLookup("partials", name, "partial"), "'" + name + "'", this.popStack(), "helpers", "partials" ];
                    if (this.options.data) {
                        params.push("data");
                    }
                    this.context.aliases.self = "this";
                    this.push("self.invokePartial(" + params.join(", ") + ")");
                },
                // [assignToHash]
                //
                // On stack, before: value, hash, ...
                // On stack, after: hash, ...
                //
                // Pops a value and hash off the stack, assigns `hash[key] = value`
                // and pushes the hash back onto the stack.
                assignToHash: function(key) {
                    var value = this.popStack(), context, type;
                    if (this.options.stringParams) {
                        type = this.popStack();
                        context = this.popStack();
                    }
                    var hash = this.hash;
                    if (context) {
                        hash.contexts.push("'" + key + "': " + context);
                    }
                    if (type) {
                        hash.types.push("'" + key + "': " + type);
                    }
                    hash.values.push("'" + key + "': (" + value + ")");
                },
                // HELPERS
                compiler: JavaScriptCompiler,
                compileChildren: function(environment, options) {
                    var children = environment.children, child, compiler;
                    for (var i = 0, l = children.length; i < l; i++) {
                        child = children[i];
                        compiler = new this.compiler();
                        var index = this.matchExistingProgram(child);
                        if (index == null) {
                            this.context.programs.push("");
                            // Placeholder to prevent name conflicts for nested children
                            index = this.context.programs.length;
                            child.index = index;
                            child.name = "program" + index;
                            this.context.programs[index] = compiler.compile(child, options, this.context);
                            this.context.environments[index] = child;
                        } else {
                            child.index = index;
                            child.name = "program" + index;
                        }
                    }
                },
                matchExistingProgram: function(child) {
                    for (var i = 0, len = this.context.environments.length; i < len; i++) {
                        var environment = this.context.environments[i];
                        if (environment && environment.equals(child)) {
                            return i;
                        }
                    }
                },
                programExpression: function(guid) {
                    this.context.aliases.self = "this";
                    if (guid == null) {
                        return "self.noop";
                    }
                    var child = this.environment.children[guid], depths = child.depths.list, depth;
                    var programParams = [ child.index, child.name, "data" ];
                    for (var i = 0, l = depths.length; i < l; i++) {
                        depth = depths[i];
                        if (depth === 1) {
                            programParams.push("depth0");
                        } else {
                            programParams.push("depth" + (depth - 1));
                        }
                    }
                    return (depths.length === 0 ? "self.program(" : "self.programWithDepth(") + programParams.join(", ") + ")";
                },
                register: function(name, val) {
                    this.useRegister(name);
                    this.pushSource(name + " = " + val + ";");
                },
                useRegister: function(name) {
                    if (!this.registers[name]) {
                        this.registers[name] = true;
                        this.registers.list.push(name);
                    }
                },
                pushStackLiteral: function(item) {
                    return this.push(new Literal(item));
                },
                pushSource: function(source) {
                    if (this.pendingContent) {
                        this.source.push(this.appendToBuffer(this.quotedString(this.pendingContent)));
                        this.pendingContent = undefined;
                    }
                    if (source) {
                        this.source.push(source);
                    }
                },
                pushStack: function(item) {
                    this.flushInline();
                    var stack = this.incrStack();
                    if (item) {
                        this.pushSource(stack + " = " + item + ";");
                    }
                    this.compileStack.push(stack);
                    return stack;
                },
                replaceStack: function(callback) {
                    var prefix = "", inline = this.isInline(), stack, createdStack, usedLiteral;
                    // If we are currently inline then we want to merge the inline statement into the
                    // replacement statement via ','
                    if (inline) {
                        var top = this.popStack(true);
                        if (top instanceof Literal) {
                            // Literals do not need to be inlined
                            stack = top.value;
                            usedLiteral = true;
                        } else {
                            // Get or create the current stack name for use by the inline
                            createdStack = !this.stackSlot;
                            var name = !createdStack ? this.topStackName() : this.incrStack();
                            prefix = "(" + this.push(name) + " = " + top + "),";
                            stack = this.topStack();
                        }
                    } else {
                        stack = this.topStack();
                    }
                    var item = callback.call(this, stack);
                    if (inline) {
                        if (!usedLiteral) {
                            this.popStack();
                        }
                        if (createdStack) {
                            this.stackSlot--;
                        }
                        this.push("(" + prefix + item + ")");
                    } else {
                        // Prevent modification of the context depth variable. Through replaceStack
                        if (!/^stack/.test(stack)) {
                            stack = this.nextStack();
                        }
                        this.pushSource(stack + " = (" + prefix + item + ");");
                    }
                    return stack;
                },
                nextStack: function() {
                    return this.pushStack();
                },
                incrStack: function() {
                    this.stackSlot++;
                    if (this.stackSlot > this.stackVars.length) {
                        this.stackVars.push("stack" + this.stackSlot);
                    }
                    return this.topStackName();
                },
                topStackName: function() {
                    return "stack" + this.stackSlot;
                },
                flushInline: function() {
                    var inlineStack = this.inlineStack;
                    if (inlineStack.length) {
                        this.inlineStack = [];
                        for (var i = 0, len = inlineStack.length; i < len; i++) {
                            var entry = inlineStack[i];
                            if (entry instanceof Literal) {
                                this.compileStack.push(entry);
                            } else {
                                this.pushStack(entry);
                            }
                        }
                    }
                },
                isInline: function() {
                    return this.inlineStack.length;
                },
                popStack: function(wrapped) {
                    var inline = this.isInline(), item = (inline ? this.inlineStack : this.compileStack).pop();
                    if (!wrapped && item instanceof Literal) {
                        return item.value;
                    } else {
                        if (!inline) {
                            if (!this.stackSlot) {
                                throw new Exception("Invalid stack pop");
                            }
                            this.stackSlot--;
                        }
                        return item;
                    }
                },
                topStack: function(wrapped) {
                    var stack = this.isInline() ? this.inlineStack : this.compileStack, item = stack[stack.length - 1];
                    if (!wrapped && item instanceof Literal) {
                        return item.value;
                    } else {
                        return item;
                    }
                },
                quotedString: function(str) {
                    return '"' + str.replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029") + '"';
                },
                setupHelper: function(paramSize, name, missingParams) {
                    var params = [], paramsInit = this.setupParams(paramSize, params, missingParams);
                    var foundHelper = this.nameLookup("helpers", name, "helper");
                    return {
                        params: params,
                        paramsInit: paramsInit,
                        name: foundHelper,
                        callParams: [ "depth0" ].concat(params).join(", "),
                        helperMissingParams: missingParams && [ "depth0", this.quotedString(name) ].concat(params).join(", ")
                    };
                },
                setupOptions: function(paramSize, params) {
                    var options = [], contexts = [], types = [], param, inverse, program;
                    options.push("hash:" + this.popStack());
                    if (this.options.stringParams) {
                        options.push("hashTypes:" + this.popStack());
                        options.push("hashContexts:" + this.popStack());
                    }
                    inverse = this.popStack();
                    program = this.popStack();
                    // Avoid setting fn and inverse if neither are set. This allows
                    // helpers to do a check for `if (options.fn)`
                    if (program || inverse) {
                        if (!program) {
                            this.context.aliases.self = "this";
                            program = "self.noop";
                        }
                        if (!inverse) {
                            this.context.aliases.self = "this";
                            inverse = "self.noop";
                        }
                        options.push("inverse:" + inverse);
                        options.push("fn:" + program);
                    }
                    for (var i = 0; i < paramSize; i++) {
                        param = this.popStack();
                        params.push(param);
                        if (this.options.stringParams) {
                            types.push(this.popStack());
                            contexts.push(this.popStack());
                        }
                    }
                    if (this.options.stringParams) {
                        options.push("contexts:[" + contexts.join(",") + "]");
                        options.push("types:[" + types.join(",") + "]");
                    }
                    if (this.options.data) {
                        options.push("data:data");
                    }
                    return options;
                },
                // the params and contexts arguments are passed in arrays
                // to fill in
                setupParams: function(paramSize, params, useRegister) {
                    var options = "{" + this.setupOptions(paramSize, params).join(",") + "}";
                    if (useRegister) {
                        this.useRegister("options");
                        params.push("options");
                        return "options=" + options;
                    } else {
                        params.push(options);
                        return "";
                    }
                }
            };
            var reservedWords = ("break else new var" + " case finally return void" + " catch for switch while" + " continue function this with" + " default if throw" + " delete in try" + " do instanceof typeof" + " abstract enum int short" + " boolean export interface static" + " byte extends long super" + " char final native synchronized" + " class float package throws" + " const goto private transient" + " debugger implements protected volatile" + " double import public let yield").split(" ");
            var compilerWords = JavaScriptCompiler.RESERVED_WORDS = {};
            for (var i = 0, l = reservedWords.length; i < l; i++) {
                compilerWords[reservedWords[i]] = true;
            }
            JavaScriptCompiler.isValidJavaScriptVariableName = function(name) {
                if (!JavaScriptCompiler.RESERVED_WORDS[name] && /^[a-zA-Z_$][0-9a-zA-Z_$]*$/.test(name)) {
                    return true;
                }
                return false;
            };
            __exports__ = JavaScriptCompiler;
            return __exports__;
        }(__module2__, __module5__);
        // handlebars.js
        var __module0__ = function(__dependency1__, __dependency2__, __dependency3__, __dependency4__, __dependency5__) {
            "use strict";
            var __exports__;
            /*globals Handlebars: true */
            var Handlebars = __dependency1__;
            // Compiler imports
            var AST = __dependency2__;
            var Parser = __dependency3__.parser;
            var parse = __dependency3__.parse;
            var Compiler = __dependency4__.Compiler;
            var compile = __dependency4__.compile;
            var precompile = __dependency4__.precompile;
            var JavaScriptCompiler = __dependency5__;
            var _create = Handlebars.create;
            var create = function() {
                var hb = _create();
                hb.compile = function(input, options) {
                    return compile(input, options, hb);
                };
                hb.precompile = function(input, options) {
                    return precompile(input, options, hb);
                };
                hb.AST = AST;
                hb.Compiler = Compiler;
                hb.JavaScriptCompiler = JavaScriptCompiler;
                hb.Parser = Parser;
                hb.parse = parse;
                return hb;
            };
            Handlebars = create();
            Handlebars.create = create;
            __exports__ = Handlebars;
            return __exports__;
        }(__module1__, __module7__, __module8__, __module10__, __module11__);
        return __module0__;
    }();
    module.exports = Handlebars;
});

define("torabot/main/0.1.0/moment-debug", [ "torabot/main/0.1.0/moment/moment-debug", "torabot/main/0.1.0/moment/lang/zh-cn-debug" ], function(require) {
    require("torabot/main/0.1.0/moment/moment-debug");
    require("torabot/main/0.1.0/moment/lang/zh-cn-debug");
    $(".momentjs").each(function() {
        $this = $(this);
        $this.text(function() {
            var format = $this.data("format");
            if (format == "fromnow") return moment($this.text()).fromNow();
            if (format == "calendar") return moment($this.text()).calendar();
            return moment($this.text()).format(format);
        }());
    });
});

define("torabot/main/0.1.0/moment/moment-debug", [], function(require) {
    //! moment.js
    //! version : 2.6.0
    //! authors : Tim Wood, Iskren Chernev, Moment.js contributors
    //! license : MIT
    //! momentjs.com
    (function(undefined) {
        /************************************
        Constants
    ************************************/
        var moment, VERSION = "2.6.0", // the global-scope this is NOT the global object in Node.js
        globalScope = typeof global !== "undefined" ? global : this, oldGlobalMoment, round = Math.round, i, YEAR = 0, MONTH = 1, DATE = 2, HOUR = 3, MINUTE = 4, SECOND = 5, MILLISECOND = 6, // internal storage for language config files
        languages = {}, // moment internal properties
        momentProperties = {
            _isAMomentObject: null,
            _i: null,
            _f: null,
            _l: null,
            _strict: null,
            _isUTC: null,
            _offset: null,
            // optional. Combine with _isUTC
            _pf: null,
            _lang: null
        }, // check for nodeJS
        hasModule = typeof module !== "undefined" && module.exports, // ASP.NET json date format regex
        aspNetJsonRegex = /^\/?Date\((\-?\d+)/i, aspNetTimeSpanJsonRegex = /(\-)?(?:(\d*)\.)?(\d+)\:(\d+)(?:\:(\d+)\.?(\d{3})?)?/, // from http://docs.closure-library.googlecode.com/git/closure_goog_date_date.js.source.html
        // somewhat more in line with 4.4.3.2 2004 spec, but allows decimal anywhere
        isoDurationRegex = /^(-)?P(?:(?:([0-9,.]*)Y)?(?:([0-9,.]*)M)?(?:([0-9,.]*)D)?(?:T(?:([0-9,.]*)H)?(?:([0-9,.]*)M)?(?:([0-9,.]*)S)?)?|([0-9,.]*)W)$/, // format tokens
        formattingTokens = /(\[[^\[]*\])|(\\)?(Mo|MM?M?M?|Do|DDDo|DD?D?D?|ddd?d?|do?|w[o|w]?|W[o|W]?|Q|YYYYYY|YYYYY|YYYY|YY|gg(ggg?)?|GG(GGG?)?|e|E|a|A|hh?|HH?|mm?|ss?|S{1,4}|X|zz?|ZZ?|.)/g, localFormattingTokens = /(\[[^\[]*\])|(\\)?(LT|LL?L?L?|l{1,4})/g, // parsing token regexes
        parseTokenOneOrTwoDigits = /\d\d?/, // 0 - 99
        parseTokenOneToThreeDigits = /\d{1,3}/, // 0 - 999
        parseTokenOneToFourDigits = /\d{1,4}/, // 0 - 9999
        parseTokenOneToSixDigits = /[+\-]?\d{1,6}/, // -999,999 - 999,999
        parseTokenDigits = /\d+/, // nonzero number of digits
        parseTokenWord = /[0-9]*['a-z\u00A0-\u05FF\u0700-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+|[\u0600-\u06FF\/]+(\s*?[\u0600-\u06FF]+){1,2}/i, // any word (or two) characters or numbers including two/three word month in arabic.
        parseTokenTimezone = /Z|[\+\-]\d\d:?\d\d/gi, // +00:00 -00:00 +0000 -0000 or Z
        parseTokenT = /T/i, // T (ISO separator)
        parseTokenTimestampMs = /[\+\-]?\d+(\.\d{1,3})?/, // 123456789 123456789.123
        parseTokenOrdinal = /\d{1,2}/, //strict parsing regexes
        parseTokenOneDigit = /\d/, // 0 - 9
        parseTokenTwoDigits = /\d\d/, // 00 - 99
        parseTokenThreeDigits = /\d{3}/, // 000 - 999
        parseTokenFourDigits = /\d{4}/, // 0000 - 9999
        parseTokenSixDigits = /[+-]?\d{6}/, // -999,999 - 999,999
        parseTokenSignedNumber = /[+-]?\d+/, // -inf - inf
        // iso 8601 regex
        // 0000-00-00 0000-W00 or 0000-W00-0 + T + 00 or 00:00 or 00:00:00 or 00:00:00.000 + +00:00 or +0000 or +00)
        isoRegex = /^\s*(?:[+-]\d{6}|\d{4})-(?:(\d\d-\d\d)|(W\d\d$)|(W\d\d-\d)|(\d\d\d))((T| )(\d\d(:\d\d(:\d\d(\.\d+)?)?)?)?([\+\-]\d\d(?::?\d\d)?|\s*Z)?)?$/, isoFormat = "YYYY-MM-DDTHH:mm:ssZ", isoDates = [ [ "YYYYYY-MM-DD", /[+-]\d{6}-\d{2}-\d{2}/ ], [ "YYYY-MM-DD", /\d{4}-\d{2}-\d{2}/ ], [ "GGGG-[W]WW-E", /\d{4}-W\d{2}-\d/ ], [ "GGGG-[W]WW", /\d{4}-W\d{2}/ ], [ "YYYY-DDD", /\d{4}-\d{3}/ ] ], // iso time formats and regexes
        isoTimes = [ [ "HH:mm:ss.SSSS", /(T| )\d\d:\d\d:\d\d\.\d+/ ], [ "HH:mm:ss", /(T| )\d\d:\d\d:\d\d/ ], [ "HH:mm", /(T| )\d\d:\d\d/ ], [ "HH", /(T| )\d\d/ ] ], // timezone chunker "+10:00" > ["10", "00"] or "-1530" > ["-15", "30"]
        parseTimezoneChunker = /([\+\-]|\d\d)/gi, // getter and setter names
        proxyGettersAndSetters = "Date|Hours|Minutes|Seconds|Milliseconds".split("|"), unitMillisecondFactors = {
            Milliseconds: 1,
            Seconds: 1e3,
            Minutes: 6e4,
            Hours: 36e5,
            Days: 864e5,
            Months: 2592e6,
            Years: 31536e6
        }, unitAliases = {
            ms: "millisecond",
            s: "second",
            m: "minute",
            h: "hour",
            d: "day",
            D: "date",
            w: "week",
            W: "isoWeek",
            M: "month",
            Q: "quarter",
            y: "year",
            DDD: "dayOfYear",
            e: "weekday",
            E: "isoWeekday",
            gg: "weekYear",
            GG: "isoWeekYear"
        }, camelFunctions = {
            dayofyear: "dayOfYear",
            isoweekday: "isoWeekday",
            isoweek: "isoWeek",
            weekyear: "weekYear",
            isoweekyear: "isoWeekYear"
        }, // format function strings
        formatFunctions = {}, // tokens to ordinalize and pad
        ordinalizeTokens = "DDD w W M D d".split(" "), paddedTokens = "M D H h m s w W".split(" "), formatTokenFunctions = {
            M: function() {
                return this.month() + 1;
            },
            MMM: function(format) {
                return this.lang().monthsShort(this, format);
            },
            MMMM: function(format) {
                return this.lang().months(this, format);
            },
            D: function() {
                return this.date();
            },
            DDD: function() {
                return this.dayOfYear();
            },
            d: function() {
                return this.day();
            },
            dd: function(format) {
                return this.lang().weekdaysMin(this, format);
            },
            ddd: function(format) {
                return this.lang().weekdaysShort(this, format);
            },
            dddd: function(format) {
                return this.lang().weekdays(this, format);
            },
            w: function() {
                return this.week();
            },
            W: function() {
                return this.isoWeek();
            },
            YY: function() {
                return leftZeroFill(this.year() % 100, 2);
            },
            YYYY: function() {
                return leftZeroFill(this.year(), 4);
            },
            YYYYY: function() {
                return leftZeroFill(this.year(), 5);
            },
            YYYYYY: function() {
                var y = this.year(), sign = y >= 0 ? "+" : "-";
                return sign + leftZeroFill(Math.abs(y), 6);
            },
            gg: function() {
                return leftZeroFill(this.weekYear() % 100, 2);
            },
            gggg: function() {
                return leftZeroFill(this.weekYear(), 4);
            },
            ggggg: function() {
                return leftZeroFill(this.weekYear(), 5);
            },
            GG: function() {
                return leftZeroFill(this.isoWeekYear() % 100, 2);
            },
            GGGG: function() {
                return leftZeroFill(this.isoWeekYear(), 4);
            },
            GGGGG: function() {
                return leftZeroFill(this.isoWeekYear(), 5);
            },
            e: function() {
                return this.weekday();
            },
            E: function() {
                return this.isoWeekday();
            },
            a: function() {
                return this.lang().meridiem(this.hours(), this.minutes(), true);
            },
            A: function() {
                return this.lang().meridiem(this.hours(), this.minutes(), false);
            },
            H: function() {
                return this.hours();
            },
            h: function() {
                return this.hours() % 12 || 12;
            },
            m: function() {
                return this.minutes();
            },
            s: function() {
                return this.seconds();
            },
            S: function() {
                return toInt(this.milliseconds() / 100);
            },
            SS: function() {
                return leftZeroFill(toInt(this.milliseconds() / 10), 2);
            },
            SSS: function() {
                return leftZeroFill(this.milliseconds(), 3);
            },
            SSSS: function() {
                return leftZeroFill(this.milliseconds(), 3);
            },
            Z: function() {
                var a = -this.zone(), b = "+";
                if (a < 0) {
                    a = -a;
                    b = "-";
                }
                return b + leftZeroFill(toInt(a / 60), 2) + ":" + leftZeroFill(toInt(a) % 60, 2);
            },
            ZZ: function() {
                var a = -this.zone(), b = "+";
                if (a < 0) {
                    a = -a;
                    b = "-";
                }
                return b + leftZeroFill(toInt(a / 60), 2) + leftZeroFill(toInt(a) % 60, 2);
            },
            z: function() {
                return this.zoneAbbr();
            },
            zz: function() {
                return this.zoneName();
            },
            X: function() {
                return this.unix();
            },
            Q: function() {
                return this.quarter();
            }
        }, lists = [ "months", "monthsShort", "weekdays", "weekdaysShort", "weekdaysMin" ];
        function defaultParsingFlags() {
            // We need to deep clone this object, and es5 standard is not very
            // helpful.
            return {
                empty: false,
                unusedTokens: [],
                unusedInput: [],
                overflow: -2,
                charsLeftOver: 0,
                nullInput: false,
                invalidMonth: null,
                invalidFormat: false,
                userInvalidated: false,
                iso: false
            };
        }
        function deprecate(msg, fn) {
            var firstTime = true;
            function printMsg() {
                if (moment.suppressDeprecationWarnings === false && typeof console !== "undefined" && console.warn) {
                    console.warn("Deprecation warning: " + msg);
                }
            }
            return extend(function() {
                if (firstTime) {
                    printMsg();
                    firstTime = false;
                }
                return fn.apply(this, arguments);
            }, fn);
        }
        function padToken(func, count) {
            return function(a) {
                return leftZeroFill(func.call(this, a), count);
            };
        }
        function ordinalizeToken(func, period) {
            return function(a) {
                return this.lang().ordinal(func.call(this, a), period);
            };
        }
        while (ordinalizeTokens.length) {
            i = ordinalizeTokens.pop();
            formatTokenFunctions[i + "o"] = ordinalizeToken(formatTokenFunctions[i], i);
        }
        while (paddedTokens.length) {
            i = paddedTokens.pop();
            formatTokenFunctions[i + i] = padToken(formatTokenFunctions[i], 2);
        }
        formatTokenFunctions.DDDD = padToken(formatTokenFunctions.DDD, 3);
        /************************************
        Constructors
    ************************************/
        function Language() {}
        // Moment prototype object
        function Moment(config) {
            checkOverflow(config);
            extend(this, config);
        }
        // Duration Constructor
        function Duration(duration) {
            var normalizedInput = normalizeObjectUnits(duration), years = normalizedInput.year || 0, quarters = normalizedInput.quarter || 0, months = normalizedInput.month || 0, weeks = normalizedInput.week || 0, days = normalizedInput.day || 0, hours = normalizedInput.hour || 0, minutes = normalizedInput.minute || 0, seconds = normalizedInput.second || 0, milliseconds = normalizedInput.millisecond || 0;
            // representation for dateAddRemove
            this._milliseconds = +milliseconds + seconds * 1e3 + // 1000
            minutes * 6e4 + // 1000 * 60
            hours * 36e5;
            // 1000 * 60 * 60
            // Because of dateAddRemove treats 24 hours as different from a
            // day when working around DST, we need to store them separately
            this._days = +days + weeks * 7;
            // It is impossible translate months into days without knowing
            // which months you are are talking about, so we have to store
            // it separately.
            this._months = +months + quarters * 3 + years * 12;
            this._data = {};
            this._bubble();
        }
        /************************************
        Helpers
    ************************************/
        function extend(a, b) {
            for (var i in b) {
                if (b.hasOwnProperty(i)) {
                    a[i] = b[i];
                }
            }
            if (b.hasOwnProperty("toString")) {
                a.toString = b.toString;
            }
            if (b.hasOwnProperty("valueOf")) {
                a.valueOf = b.valueOf;
            }
            return a;
        }
        function cloneMoment(m) {
            var result = {}, i;
            for (i in m) {
                if (m.hasOwnProperty(i) && momentProperties.hasOwnProperty(i)) {
                    result[i] = m[i];
                }
            }
            return result;
        }
        function absRound(number) {
            if (number < 0) {
                return Math.ceil(number);
            } else {
                return Math.floor(number);
            }
        }
        // left zero fill a number
        // see http://jsperf.com/left-zero-filling for performance comparison
        function leftZeroFill(number, targetLength, forceSign) {
            var output = "" + Math.abs(number), sign = number >= 0;
            while (output.length < targetLength) {
                output = "0" + output;
            }
            return (sign ? forceSign ? "+" : "" : "-") + output;
        }
        // helper function for _.addTime and _.subtractTime
        function addOrSubtractDurationFromMoment(mom, duration, isAdding, updateOffset) {
            var milliseconds = duration._milliseconds, days = duration._days, months = duration._months;
            updateOffset = updateOffset == null ? true : updateOffset;
            if (milliseconds) {
                mom._d.setTime(+mom._d + milliseconds * isAdding);
            }
            if (days) {
                rawSetter(mom, "Date", rawGetter(mom, "Date") + days * isAdding);
            }
            if (months) {
                rawMonthSetter(mom, rawGetter(mom, "Month") + months * isAdding);
            }
            if (updateOffset) {
                moment.updateOffset(mom, days || months);
            }
        }
        // check if is an array
        function isArray(input) {
            return Object.prototype.toString.call(input) === "[object Array]";
        }
        function isDate(input) {
            return Object.prototype.toString.call(input) === "[object Date]" || input instanceof Date;
        }
        // compare two arrays, return the number of differences
        function compareArrays(array1, array2, dontConvert) {
            var len = Math.min(array1.length, array2.length), lengthDiff = Math.abs(array1.length - array2.length), diffs = 0, i;
            for (i = 0; i < len; i++) {
                if (dontConvert && array1[i] !== array2[i] || !dontConvert && toInt(array1[i]) !== toInt(array2[i])) {
                    diffs++;
                }
            }
            return diffs + lengthDiff;
        }
        function normalizeUnits(units) {
            if (units) {
                var lowered = units.toLowerCase().replace(/(.)s$/, "$1");
                units = unitAliases[units] || camelFunctions[lowered] || lowered;
            }
            return units;
        }
        function normalizeObjectUnits(inputObject) {
            var normalizedInput = {}, normalizedProp, prop;
            for (prop in inputObject) {
                if (inputObject.hasOwnProperty(prop)) {
                    normalizedProp = normalizeUnits(prop);
                    if (normalizedProp) {
                        normalizedInput[normalizedProp] = inputObject[prop];
                    }
                }
            }
            return normalizedInput;
        }
        function makeList(field) {
            var count, setter;
            if (field.indexOf("week") === 0) {
                count = 7;
                setter = "day";
            } else if (field.indexOf("month") === 0) {
                count = 12;
                setter = "month";
            } else {
                return;
            }
            moment[field] = function(format, index) {
                var i, getter, method = moment.fn._lang[field], results = [];
                if (typeof format === "number") {
                    index = format;
                    format = undefined;
                }
                getter = function(i) {
                    var m = moment().utc().set(setter, i);
                    return method.call(moment.fn._lang, m, format || "");
                };
                if (index != null) {
                    return getter(index);
                } else {
                    for (i = 0; i < count; i++) {
                        results.push(getter(i));
                    }
                    return results;
                }
            };
        }
        function toInt(argumentForCoercion) {
            var coercedNumber = +argumentForCoercion, value = 0;
            if (coercedNumber !== 0 && isFinite(coercedNumber)) {
                if (coercedNumber >= 0) {
                    value = Math.floor(coercedNumber);
                } else {
                    value = Math.ceil(coercedNumber);
                }
            }
            return value;
        }
        function daysInMonth(year, month) {
            return new Date(Date.UTC(year, month + 1, 0)).getUTCDate();
        }
        function weeksInYear(year, dow, doy) {
            return weekOfYear(moment([ year, 11, 31 + dow - doy ]), dow, doy).week;
        }
        function daysInYear(year) {
            return isLeapYear(year) ? 366 : 365;
        }
        function isLeapYear(year) {
            return year % 4 === 0 && year % 100 !== 0 || year % 400 === 0;
        }
        function checkOverflow(m) {
            var overflow;
            if (m._a && m._pf.overflow === -2) {
                overflow = m._a[MONTH] < 0 || m._a[MONTH] > 11 ? MONTH : m._a[DATE] < 1 || m._a[DATE] > daysInMonth(m._a[YEAR], m._a[MONTH]) ? DATE : m._a[HOUR] < 0 || m._a[HOUR] > 23 ? HOUR : m._a[MINUTE] < 0 || m._a[MINUTE] > 59 ? MINUTE : m._a[SECOND] < 0 || m._a[SECOND] > 59 ? SECOND : m._a[MILLISECOND] < 0 || m._a[MILLISECOND] > 999 ? MILLISECOND : -1;
                if (m._pf._overflowDayOfYear && (overflow < YEAR || overflow > DATE)) {
                    overflow = DATE;
                }
                m._pf.overflow = overflow;
            }
        }
        function isValid(m) {
            if (m._isValid == null) {
                m._isValid = !isNaN(m._d.getTime()) && m._pf.overflow < 0 && !m._pf.empty && !m._pf.invalidMonth && !m._pf.nullInput && !m._pf.invalidFormat && !m._pf.userInvalidated;
                if (m._strict) {
                    m._isValid = m._isValid && m._pf.charsLeftOver === 0 && m._pf.unusedTokens.length === 0;
                }
            }
            return m._isValid;
        }
        function normalizeLanguage(key) {
            return key ? key.toLowerCase().replace("_", "-") : key;
        }
        // Return a moment from input, that is local/utc/zone equivalent to model.
        function makeAs(input, model) {
            return model._isUTC ? moment(input).zone(model._offset || 0) : moment(input).local();
        }
        /************************************
        Languages
    ************************************/
        extend(Language.prototype, {
            set: function(config) {
                var prop, i;
                for (i in config) {
                    prop = config[i];
                    if (typeof prop === "function") {
                        this[i] = prop;
                    } else {
                        this["_" + i] = prop;
                    }
                }
            },
            _months: "January_February_March_April_May_June_July_August_September_October_November_December".split("_"),
            months: function(m) {
                return this._months[m.month()];
            },
            _monthsShort: "Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),
            monthsShort: function(m) {
                return this._monthsShort[m.month()];
            },
            monthsParse: function(monthName) {
                var i, mom, regex;
                if (!this._monthsParse) {
                    this._monthsParse = [];
                }
                for (i = 0; i < 12; i++) {
                    // make the regex if we don't have it already
                    if (!this._monthsParse[i]) {
                        mom = moment.utc([ 2e3, i ]);
                        regex = "^" + this.months(mom, "") + "|^" + this.monthsShort(mom, "");
                        this._monthsParse[i] = new RegExp(regex.replace(".", ""), "i");
                    }
                    // test the regex
                    if (this._monthsParse[i].test(monthName)) {
                        return i;
                    }
                }
            },
            _weekdays: "Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),
            weekdays: function(m) {
                return this._weekdays[m.day()];
            },
            _weekdaysShort: "Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),
            weekdaysShort: function(m) {
                return this._weekdaysShort[m.day()];
            },
            _weekdaysMin: "Su_Mo_Tu_We_Th_Fr_Sa".split("_"),
            weekdaysMin: function(m) {
                return this._weekdaysMin[m.day()];
            },
            weekdaysParse: function(weekdayName) {
                var i, mom, regex;
                if (!this._weekdaysParse) {
                    this._weekdaysParse = [];
                }
                for (i = 0; i < 7; i++) {
                    // make the regex if we don't have it already
                    if (!this._weekdaysParse[i]) {
                        mom = moment([ 2e3, 1 ]).day(i);
                        regex = "^" + this.weekdays(mom, "") + "|^" + this.weekdaysShort(mom, "") + "|^" + this.weekdaysMin(mom, "");
                        this._weekdaysParse[i] = new RegExp(regex.replace(".", ""), "i");
                    }
                    // test the regex
                    if (this._weekdaysParse[i].test(weekdayName)) {
                        return i;
                    }
                }
            },
            _longDateFormat: {
                LT: "h:mm A",
                L: "MM/DD/YYYY",
                LL: "MMMM D YYYY",
                LLL: "MMMM D YYYY LT",
                LLLL: "dddd, MMMM D YYYY LT"
            },
            longDateFormat: function(key) {
                var output = this._longDateFormat[key];
                if (!output && this._longDateFormat[key.toUpperCase()]) {
                    output = this._longDateFormat[key.toUpperCase()].replace(/MMMM|MM|DD|dddd/g, function(val) {
                        return val.slice(1);
                    });
                    this._longDateFormat[key] = output;
                }
                return output;
            },
            isPM: function(input) {
                // IE8 Quirks Mode & IE7 Standards Mode do not allow accessing strings like arrays
                // Using charAt should be more compatible.
                return (input + "").toLowerCase().charAt(0) === "p";
            },
            _meridiemParse: /[ap]\.?m?\.?/i,
            meridiem: function(hours, minutes, isLower) {
                if (hours > 11) {
                    return isLower ? "pm" : "PM";
                } else {
                    return isLower ? "am" : "AM";
                }
            },
            _calendar: {
                sameDay: "[Today at] LT",
                nextDay: "[Tomorrow at] LT",
                nextWeek: "dddd [at] LT",
                lastDay: "[Yesterday at] LT",
                lastWeek: "[Last] dddd [at] LT",
                sameElse: "L"
            },
            calendar: function(key, mom) {
                var output = this._calendar[key];
                return typeof output === "function" ? output.apply(mom) : output;
            },
            _relativeTime: {
                future: "in %s",
                past: "%s ago",
                s: "a few seconds",
                m: "a minute",
                mm: "%d minutes",
                h: "an hour",
                hh: "%d hours",
                d: "a day",
                dd: "%d days",
                M: "a month",
                MM: "%d months",
                y: "a year",
                yy: "%d years"
            },
            relativeTime: function(number, withoutSuffix, string, isFuture) {
                var output = this._relativeTime[string];
                return typeof output === "function" ? output(number, withoutSuffix, string, isFuture) : output.replace(/%d/i, number);
            },
            pastFuture: function(diff, output) {
                var format = this._relativeTime[diff > 0 ? "future" : "past"];
                return typeof format === "function" ? format(output) : format.replace(/%s/i, output);
            },
            ordinal: function(number) {
                return this._ordinal.replace("%d", number);
            },
            _ordinal: "%d",
            preparse: function(string) {
                return string;
            },
            postformat: function(string) {
                return string;
            },
            week: function(mom) {
                return weekOfYear(mom, this._week.dow, this._week.doy).week;
            },
            _week: {
                dow: 0,
                // Sunday is the first day of the week.
                doy: 6
            },
            _invalidDate: "Invalid date",
            invalidDate: function() {
                return this._invalidDate;
            }
        });
        // Loads a language definition into the `languages` cache.  The function
        // takes a key and optionally values.  If not in the browser and no values
        // are provided, it will load the language file module.  As a convenience,
        // this function also returns the language values.
        function loadLang(key, values) {
            values.abbr = key;
            if (!languages[key]) {
                languages[key] = new Language();
            }
            languages[key].set(values);
            return languages[key];
        }
        // Remove a language from the `languages` cache. Mostly useful in tests.
        function unloadLang(key) {
            delete languages[key];
        }
        // Determines which language definition to use and returns it.
        //
        // With no parameters, it will return the global language.  If you
        // pass in a language key, such as 'en', it will return the
        // definition for 'en', so long as 'en' has already been loaded using
        // moment.lang.
        function getLangDefinition(key) {
            var i = 0, j, lang, next, split, get = function(k) {
                if (!languages[k] && hasModule) {
                    try {
                        require("./lang/" + k);
                    } catch (e) {}
                }
                return languages[k];
            };
            if (!key) {
                return moment.fn._lang;
            }
            if (!isArray(key)) {
                //short-circuit everything else
                lang = get(key);
                if (lang) {
                    return lang;
                }
                key = [ key ];
            }
            //pick the language from the array
            //try ['en-au', 'en-gb'] as 'en-au', 'en-gb', 'en', as in move through the list trying each
            //substring from most specific to least, but move to the next array item if it's a more specific variant than the current root
            while (i < key.length) {
                split = normalizeLanguage(key[i]).split("-");
                j = split.length;
                next = normalizeLanguage(key[i + 1]);
                next = next ? next.split("-") : null;
                while (j > 0) {
                    lang = get(split.slice(0, j).join("-"));
                    if (lang) {
                        return lang;
                    }
                    if (next && next.length >= j && compareArrays(split, next, true) >= j - 1) {
                        //the next array item is better than a shallower substring of this one
                        break;
                    }
                    j--;
                }
                i++;
            }
            return moment.fn._lang;
        }
        /************************************
        Formatting
    ************************************/
        function removeFormattingTokens(input) {
            if (input.match(/\[[\s\S]/)) {
                return input.replace(/^\[|\]$/g, "");
            }
            return input.replace(/\\/g, "");
        }
        function makeFormatFunction(format) {
            var array = format.match(formattingTokens), i, length;
            for (i = 0, length = array.length; i < length; i++) {
                if (formatTokenFunctions[array[i]]) {
                    array[i] = formatTokenFunctions[array[i]];
                } else {
                    array[i] = removeFormattingTokens(array[i]);
                }
            }
            return function(mom) {
                var output = "";
                for (i = 0; i < length; i++) {
                    output += array[i] instanceof Function ? array[i].call(mom, format) : array[i];
                }
                return output;
            };
        }
        // format date using native date object
        function formatMoment(m, format) {
            if (!m.isValid()) {
                return m.lang().invalidDate();
            }
            format = expandFormat(format, m.lang());
            if (!formatFunctions[format]) {
                formatFunctions[format] = makeFormatFunction(format);
            }
            return formatFunctions[format](m);
        }
        function expandFormat(format, lang) {
            var i = 5;
            function replaceLongDateFormatTokens(input) {
                return lang.longDateFormat(input) || input;
            }
            localFormattingTokens.lastIndex = 0;
            while (i >= 0 && localFormattingTokens.test(format)) {
                format = format.replace(localFormattingTokens, replaceLongDateFormatTokens);
                localFormattingTokens.lastIndex = 0;
                i -= 1;
            }
            return format;
        }
        /************************************
        Parsing
    ************************************/
        // get the regex to find the next token
        function getParseRegexForToken(token, config) {
            var a, strict = config._strict;
            switch (token) {
              case "Q":
                return parseTokenOneDigit;

              case "DDDD":
                return parseTokenThreeDigits;

              case "YYYY":
              case "GGGG":
              case "gggg":
                return strict ? parseTokenFourDigits : parseTokenOneToFourDigits;

              case "Y":
              case "G":
              case "g":
                return parseTokenSignedNumber;

              case "YYYYYY":
              case "YYYYY":
              case "GGGGG":
              case "ggggg":
                return strict ? parseTokenSixDigits : parseTokenOneToSixDigits;

              case "S":
                if (strict) {
                    return parseTokenOneDigit;
                }

              /* falls through */
                case "SS":
                if (strict) {
                    return parseTokenTwoDigits;
                }

              /* falls through */
                case "SSS":
                if (strict) {
                    return parseTokenThreeDigits;
                }

              /* falls through */
                case "DDD":
                return parseTokenOneToThreeDigits;

              case "MMM":
              case "MMMM":
              case "dd":
              case "ddd":
              case "dddd":
                return parseTokenWord;

              case "a":
              case "A":
                return getLangDefinition(config._l)._meridiemParse;

              case "X":
                return parseTokenTimestampMs;

              case "Z":
              case "ZZ":
                return parseTokenTimezone;

              case "T":
                return parseTokenT;

              case "SSSS":
                return parseTokenDigits;

              case "MM":
              case "DD":
              case "YY":
              case "GG":
              case "gg":
              case "HH":
              case "hh":
              case "mm":
              case "ss":
              case "ww":
              case "WW":
                return strict ? parseTokenTwoDigits : parseTokenOneOrTwoDigits;

              case "M":
              case "D":
              case "d":
              case "H":
              case "h":
              case "m":
              case "s":
              case "w":
              case "W":
              case "e":
              case "E":
                return parseTokenOneOrTwoDigits;

              case "Do":
                return parseTokenOrdinal;

              default:
                a = new RegExp(regexpEscape(unescapeFormat(token.replace("\\", "")), "i"));
                return a;
            }
        }
        function timezoneMinutesFromString(string) {
            string = string || "";
            var possibleTzMatches = string.match(parseTokenTimezone) || [], tzChunk = possibleTzMatches[possibleTzMatches.length - 1] || [], parts = (tzChunk + "").match(parseTimezoneChunker) || [ "-", 0, 0 ], minutes = +(parts[1] * 60) + toInt(parts[2]);
            return parts[0] === "+" ? -minutes : minutes;
        }
        // function to convert string input to date
        function addTimeToArrayFromToken(token, input, config) {
            var a, datePartArray = config._a;
            switch (token) {
              // QUARTER
                case "Q":
                if (input != null) {
                    datePartArray[MONTH] = (toInt(input) - 1) * 3;
                }
                break;

              // MONTH
                case "M":
              // fall through to MM
                case "MM":
                if (input != null) {
                    datePartArray[MONTH] = toInt(input) - 1;
                }
                break;

              case "MMM":
              // fall through to MMMM
                case "MMMM":
                a = getLangDefinition(config._l).monthsParse(input);
                // if we didn't find a month name, mark the date as invalid.
                if (a != null) {
                    datePartArray[MONTH] = a;
                } else {
                    config._pf.invalidMonth = input;
                }
                break;

              // DAY OF MONTH
                case "D":
              // fall through to DD
                case "DD":
                if (input != null) {
                    datePartArray[DATE] = toInt(input);
                }
                break;

              case "Do":
                if (input != null) {
                    datePartArray[DATE] = toInt(parseInt(input, 10));
                }
                break;

              // DAY OF YEAR
                case "DDD":
              // fall through to DDDD
                case "DDDD":
                if (input != null) {
                    config._dayOfYear = toInt(input);
                }
                break;

              // YEAR
                case "YY":
                datePartArray[YEAR] = moment.parseTwoDigitYear(input);
                break;

              case "YYYY":
              case "YYYYY":
              case "YYYYYY":
                datePartArray[YEAR] = toInt(input);
                break;

              // AM / PM
                case "a":
              // fall through to A
                case "A":
                config._isPm = getLangDefinition(config._l).isPM(input);
                break;

              // 24 HOUR
                case "H":
              // fall through to hh
                case "HH":
              // fall through to hh
                case "h":
              // fall through to hh
                case "hh":
                datePartArray[HOUR] = toInt(input);
                break;

              // MINUTE
                case "m":
              // fall through to mm
                case "mm":
                datePartArray[MINUTE] = toInt(input);
                break;

              // SECOND
                case "s":
              // fall through to ss
                case "ss":
                datePartArray[SECOND] = toInt(input);
                break;

              // MILLISECOND
                case "S":
              case "SS":
              case "SSS":
              case "SSSS":
                datePartArray[MILLISECOND] = toInt(("0." + input) * 1e3);
                break;

              // UNIX TIMESTAMP WITH MS
                case "X":
                config._d = new Date(parseFloat(input) * 1e3);
                break;

              // TIMEZONE
                case "Z":
              // fall through to ZZ
                case "ZZ":
                config._useUTC = true;
                config._tzm = timezoneMinutesFromString(input);
                break;

              case "w":
              case "ww":
              case "W":
              case "WW":
              case "d":
              case "dd":
              case "ddd":
              case "dddd":
              case "e":
              case "E":
                token = token.substr(0, 1);

              /* falls through */
                case "gg":
              case "gggg":
              case "GG":
              case "GGGG":
              case "GGGGG":
                token = token.substr(0, 2);
                if (input) {
                    config._w = config._w || {};
                    config._w[token] = input;
                }
                break;
            }
        }
        // convert an array to a date.
        // the array should mirror the parameters below
        // note: all values past the year are optional and will default to the lowest possible value.
        // [year, month, day , hour, minute, second, millisecond]
        function dateFromConfig(config) {
            var i, date, input = [], currentDate, yearToUse, fixYear, w, temp, lang, weekday, week;
            if (config._d) {
                return;
            }
            currentDate = currentDateArray(config);
            //compute day of the year from weeks and weekdays
            if (config._w && config._a[DATE] == null && config._a[MONTH] == null) {
                fixYear = function(val) {
                    var intVal = parseInt(val, 10);
                    return val ? val.length < 3 ? intVal > 68 ? 1900 + intVal : 2e3 + intVal : intVal : config._a[YEAR] == null ? moment().weekYear() : config._a[YEAR];
                };
                w = config._w;
                if (w.GG != null || w.W != null || w.E != null) {
                    temp = dayOfYearFromWeeks(fixYear(w.GG), w.W || 1, w.E, 4, 1);
                } else {
                    lang = getLangDefinition(config._l);
                    weekday = w.d != null ? parseWeekday(w.d, lang) : w.e != null ? parseInt(w.e, 10) + lang._week.dow : 0;
                    week = parseInt(w.w, 10) || 1;
                    //if we're parsing 'd', then the low day numbers may be next week
                    if (w.d != null && weekday < lang._week.dow) {
                        week++;
                    }
                    temp = dayOfYearFromWeeks(fixYear(w.gg), week, weekday, lang._week.doy, lang._week.dow);
                }
                config._a[YEAR] = temp.year;
                config._dayOfYear = temp.dayOfYear;
            }
            //if the day of the year is set, figure out what it is
            if (config._dayOfYear) {
                yearToUse = config._a[YEAR] == null ? currentDate[YEAR] : config._a[YEAR];
                if (config._dayOfYear > daysInYear(yearToUse)) {
                    config._pf._overflowDayOfYear = true;
                }
                date = makeUTCDate(yearToUse, 0, config._dayOfYear);
                config._a[MONTH] = date.getUTCMonth();
                config._a[DATE] = date.getUTCDate();
            }
            // Default to current date.
            // * if no year, month, day of month are given, default to today
            // * if day of month is given, default month and year
            // * if month is given, default only year
            // * if year is given, don't default anything
            for (i = 0; i < 3 && config._a[i] == null; ++i) {
                config._a[i] = input[i] = currentDate[i];
            }
            // Zero out whatever was not defaulted, including time
            for (;i < 7; i++) {
                config._a[i] = input[i] = config._a[i] == null ? i === 2 ? 1 : 0 : config._a[i];
            }
            // add the offsets to the time to be parsed so that we can have a clean array for checking isValid
            input[HOUR] += toInt((config._tzm || 0) / 60);
            input[MINUTE] += toInt((config._tzm || 0) % 60);
            config._d = (config._useUTC ? makeUTCDate : makeDate).apply(null, input);
        }
        function dateFromObject(config) {
            var normalizedInput;
            if (config._d) {
                return;
            }
            normalizedInput = normalizeObjectUnits(config._i);
            config._a = [ normalizedInput.year, normalizedInput.month, normalizedInput.day, normalizedInput.hour, normalizedInput.minute, normalizedInput.second, normalizedInput.millisecond ];
            dateFromConfig(config);
        }
        function currentDateArray(config) {
            var now = new Date();
            if (config._useUTC) {
                return [ now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() ];
            } else {
                return [ now.getFullYear(), now.getMonth(), now.getDate() ];
            }
        }
        // date from string and format string
        function makeDateFromStringAndFormat(config) {
            config._a = [];
            config._pf.empty = true;
            // This array is used to make a Date, either with `new Date` or `Date.UTC`
            var lang = getLangDefinition(config._l), string = "" + config._i, i, parsedInput, tokens, token, skipped, stringLength = string.length, totalParsedInputLength = 0;
            tokens = expandFormat(config._f, lang).match(formattingTokens) || [];
            for (i = 0; i < tokens.length; i++) {
                token = tokens[i];
                parsedInput = (string.match(getParseRegexForToken(token, config)) || [])[0];
                if (parsedInput) {
                    skipped = string.substr(0, string.indexOf(parsedInput));
                    if (skipped.length > 0) {
                        config._pf.unusedInput.push(skipped);
                    }
                    string = string.slice(string.indexOf(parsedInput) + parsedInput.length);
                    totalParsedInputLength += parsedInput.length;
                }
                // don't parse if it's not a known token
                if (formatTokenFunctions[token]) {
                    if (parsedInput) {
                        config._pf.empty = false;
                    } else {
                        config._pf.unusedTokens.push(token);
                    }
                    addTimeToArrayFromToken(token, parsedInput, config);
                } else if (config._strict && !parsedInput) {
                    config._pf.unusedTokens.push(token);
                }
            }
            // add remaining unparsed input length to the string
            config._pf.charsLeftOver = stringLength - totalParsedInputLength;
            if (string.length > 0) {
                config._pf.unusedInput.push(string);
            }
            // handle am pm
            if (config._isPm && config._a[HOUR] < 12) {
                config._a[HOUR] += 12;
            }
            // if is 12 am, change hours to 0
            if (config._isPm === false && config._a[HOUR] === 12) {
                config._a[HOUR] = 0;
            }
            dateFromConfig(config);
            checkOverflow(config);
        }
        function unescapeFormat(s) {
            return s.replace(/\\(\[)|\\(\])|\[([^\]\[]*)\]|\\(.)/g, function(matched, p1, p2, p3, p4) {
                return p1 || p2 || p3 || p4;
            });
        }
        // Code from http://stackoverflow.com/questions/3561493/is-there-a-regexp-escape-function-in-javascript
        function regexpEscape(s) {
            return s.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");
        }
        // date from string and array of format strings
        function makeDateFromStringAndArray(config) {
            var tempConfig, bestMoment, scoreToBeat, i, currentScore;
            if (config._f.length === 0) {
                config._pf.invalidFormat = true;
                config._d = new Date(NaN);
                return;
            }
            for (i = 0; i < config._f.length; i++) {
                currentScore = 0;
                tempConfig = extend({}, config);
                tempConfig._pf = defaultParsingFlags();
                tempConfig._f = config._f[i];
                makeDateFromStringAndFormat(tempConfig);
                if (!isValid(tempConfig)) {
                    continue;
                }
                // if there is any input that was not parsed add a penalty for that format
                currentScore += tempConfig._pf.charsLeftOver;
                //or tokens
                currentScore += tempConfig._pf.unusedTokens.length * 10;
                tempConfig._pf.score = currentScore;
                if (scoreToBeat == null || currentScore < scoreToBeat) {
                    scoreToBeat = currentScore;
                    bestMoment = tempConfig;
                }
            }
            extend(config, bestMoment || tempConfig);
        }
        // date from iso format
        function makeDateFromString(config) {
            var i, l, string = config._i, match = isoRegex.exec(string);
            if (match) {
                config._pf.iso = true;
                for (i = 0, l = isoDates.length; i < l; i++) {
                    if (isoDates[i][1].exec(string)) {
                        // match[5] should be "T" or undefined
                        config._f = isoDates[i][0] + (match[6] || " ");
                        break;
                    }
                }
                for (i = 0, l = isoTimes.length; i < l; i++) {
                    if (isoTimes[i][1].exec(string)) {
                        config._f += isoTimes[i][0];
                        break;
                    }
                }
                if (string.match(parseTokenTimezone)) {
                    config._f += "Z";
                }
                makeDateFromStringAndFormat(config);
            } else {
                moment.createFromInputFallback(config);
            }
        }
        function makeDateFromInput(config) {
            var input = config._i, matched = aspNetJsonRegex.exec(input);
            if (input === undefined) {
                config._d = new Date();
            } else if (matched) {
                config._d = new Date(+matched[1]);
            } else if (typeof input === "string") {
                makeDateFromString(config);
            } else if (isArray(input)) {
                config._a = input.slice(0);
                dateFromConfig(config);
            } else if (isDate(input)) {
                config._d = new Date(+input);
            } else if (typeof input === "object") {
                dateFromObject(config);
            } else if (typeof input === "number") {
                // from milliseconds
                config._d = new Date(input);
            } else {
                moment.createFromInputFallback(config);
            }
        }
        function makeDate(y, m, d, h, M, s, ms) {
            //can't just apply() to create a date:
            //http://stackoverflow.com/questions/181348/instantiating-a-javascript-object-by-calling-prototype-constructor-apply
            var date = new Date(y, m, d, h, M, s, ms);
            //the date constructor doesn't accept years < 1970
            if (y < 1970) {
                date.setFullYear(y);
            }
            return date;
        }
        function makeUTCDate(y) {
            var date = new Date(Date.UTC.apply(null, arguments));
            if (y < 1970) {
                date.setUTCFullYear(y);
            }
            return date;
        }
        function parseWeekday(input, language) {
            if (typeof input === "string") {
                if (!isNaN(input)) {
                    input = parseInt(input, 10);
                } else {
                    input = language.weekdaysParse(input);
                    if (typeof input !== "number") {
                        return null;
                    }
                }
            }
            return input;
        }
        /************************************
        Relative Time
    ************************************/
        // helper function for moment.fn.from, moment.fn.fromNow, and moment.duration.fn.humanize
        function substituteTimeAgo(string, number, withoutSuffix, isFuture, lang) {
            return lang.relativeTime(number || 1, !!withoutSuffix, string, isFuture);
        }
        function relativeTime(milliseconds, withoutSuffix, lang) {
            var seconds = round(Math.abs(milliseconds) / 1e3), minutes = round(seconds / 60), hours = round(minutes / 60), days = round(hours / 24), years = round(days / 365), args = seconds < 45 && [ "s", seconds ] || minutes === 1 && [ "m" ] || minutes < 45 && [ "mm", minutes ] || hours === 1 && [ "h" ] || hours < 22 && [ "hh", hours ] || days === 1 && [ "d" ] || days <= 25 && [ "dd", days ] || days <= 45 && [ "M" ] || days < 345 && [ "MM", round(days / 30) ] || years === 1 && [ "y" ] || [ "yy", years ];
            args[2] = withoutSuffix;
            args[3] = milliseconds > 0;
            args[4] = lang;
            return substituteTimeAgo.apply({}, args);
        }
        /************************************
        Week of Year
    ************************************/
        // firstDayOfWeek       0 = sun, 6 = sat
        //                      the day of the week that starts the week
        //                      (usually sunday or monday)
        // firstDayOfWeekOfYear 0 = sun, 6 = sat
        //                      the first week is the week that contains the first
        //                      of this day of the week
        //                      (eg. ISO weeks use thursday (4))
        function weekOfYear(mom, firstDayOfWeek, firstDayOfWeekOfYear) {
            var end = firstDayOfWeekOfYear - firstDayOfWeek, daysToDayOfWeek = firstDayOfWeekOfYear - mom.day(), adjustedMoment;
            if (daysToDayOfWeek > end) {
                daysToDayOfWeek -= 7;
            }
            if (daysToDayOfWeek < end - 7) {
                daysToDayOfWeek += 7;
            }
            adjustedMoment = moment(mom).add("d", daysToDayOfWeek);
            return {
                week: Math.ceil(adjustedMoment.dayOfYear() / 7),
                year: adjustedMoment.year()
            };
        }
        //http://en.wikipedia.org/wiki/ISO_week_date#Calculating_a_date_given_the_year.2C_week_number_and_weekday
        function dayOfYearFromWeeks(year, week, weekday, firstDayOfWeekOfYear, firstDayOfWeek) {
            var d = makeUTCDate(year, 0, 1).getUTCDay(), daysToAdd, dayOfYear;
            weekday = weekday != null ? weekday : firstDayOfWeek;
            daysToAdd = firstDayOfWeek - d + (d > firstDayOfWeekOfYear ? 7 : 0) - (d < firstDayOfWeek ? 7 : 0);
            dayOfYear = 7 * (week - 1) + (weekday - firstDayOfWeek) + daysToAdd + 1;
            return {
                year: dayOfYear > 0 ? year : year - 1,
                dayOfYear: dayOfYear > 0 ? dayOfYear : daysInYear(year - 1) + dayOfYear
            };
        }
        /************************************
        Top Level Functions
    ************************************/
        function makeMoment(config) {
            var input = config._i, format = config._f;
            if (input === null || format === undefined && input === "") {
                return moment.invalid({
                    nullInput: true
                });
            }
            if (typeof input === "string") {
                config._i = input = getLangDefinition().preparse(input);
            }
            if (moment.isMoment(input)) {
                config = cloneMoment(input);
                config._d = new Date(+input._d);
            } else if (format) {
                if (isArray(format)) {
                    makeDateFromStringAndArray(config);
                } else {
                    makeDateFromStringAndFormat(config);
                }
            } else {
                makeDateFromInput(config);
            }
            return new Moment(config);
        }
        moment = function(input, format, lang, strict) {
            var c;
            if (typeof lang === "boolean") {
                strict = lang;
                lang = undefined;
            }
            // object construction must be done this way.
            // https://github.com/moment/moment/issues/1423
            c = {};
            c._isAMomentObject = true;
            c._i = input;
            c._f = format;
            c._l = lang;
            c._strict = strict;
            c._isUTC = false;
            c._pf = defaultParsingFlags();
            return makeMoment(c);
        };
        moment.suppressDeprecationWarnings = false;
        moment.createFromInputFallback = deprecate("moment construction falls back to js Date. This is " + "discouraged and will be removed in upcoming major " + "release. Please refer to " + "https://github.com/moment/moment/issues/1407 for more info.", function(config) {
            config._d = new Date(config._i);
        });
        // creating with utc
        moment.utc = function(input, format, lang, strict) {
            var c;
            if (typeof lang === "boolean") {
                strict = lang;
                lang = undefined;
            }
            // object construction must be done this way.
            // https://github.com/moment/moment/issues/1423
            c = {};
            c._isAMomentObject = true;
            c._useUTC = true;
            c._isUTC = true;
            c._l = lang;
            c._i = input;
            c._f = format;
            c._strict = strict;
            c._pf = defaultParsingFlags();
            return makeMoment(c).utc();
        };
        // creating with unix timestamp (in seconds)
        moment.unix = function(input) {
            return moment(input * 1e3);
        };
        // duration
        moment.duration = function(input, key) {
            var duration = input, // matching against regexp is expensive, do it on demand
            match = null, sign, ret, parseIso;
            if (moment.isDuration(input)) {
                duration = {
                    ms: input._milliseconds,
                    d: input._days,
                    M: input._months
                };
            } else if (typeof input === "number") {
                duration = {};
                if (key) {
                    duration[key] = input;
                } else {
                    duration.milliseconds = input;
                }
            } else if (!!(match = aspNetTimeSpanJsonRegex.exec(input))) {
                sign = match[1] === "-" ? -1 : 1;
                duration = {
                    y: 0,
                    d: toInt(match[DATE]) * sign,
                    h: toInt(match[HOUR]) * sign,
                    m: toInt(match[MINUTE]) * sign,
                    s: toInt(match[SECOND]) * sign,
                    ms: toInt(match[MILLISECOND]) * sign
                };
            } else if (!!(match = isoDurationRegex.exec(input))) {
                sign = match[1] === "-" ? -1 : 1;
                parseIso = function(inp) {
                    // We'd normally use ~~inp for this, but unfortunately it also
                    // converts floats to ints.
                    // inp may be undefined, so careful calling replace on it.
                    var res = inp && parseFloat(inp.replace(",", "."));
                    // apply sign while we're at it
                    return (isNaN(res) ? 0 : res) * sign;
                };
                duration = {
                    y: parseIso(match[2]),
                    M: parseIso(match[3]),
                    d: parseIso(match[4]),
                    h: parseIso(match[5]),
                    m: parseIso(match[6]),
                    s: parseIso(match[7]),
                    w: parseIso(match[8])
                };
            }
            ret = new Duration(duration);
            if (moment.isDuration(input) && input.hasOwnProperty("_lang")) {
                ret._lang = input._lang;
            }
            return ret;
        };
        // version number
        moment.version = VERSION;
        // default format
        moment.defaultFormat = isoFormat;
        // Plugins that add properties should also add the key here (null value),
        // so we can properly clone ourselves.
        moment.momentProperties = momentProperties;
        // This function will be called whenever a moment is mutated.
        // It is intended to keep the offset in sync with the timezone.
        moment.updateOffset = function() {};
        // This function will load languages and then set the global language.  If
        // no arguments are passed in, it will simply return the current global
        // language key.
        moment.lang = function(key, values) {
            var r;
            if (!key) {
                return moment.fn._lang._abbr;
            }
            if (values) {
                loadLang(normalizeLanguage(key), values);
            } else if (values === null) {
                unloadLang(key);
                key = "en";
            } else if (!languages[key]) {
                getLangDefinition(key);
            }
            r = moment.duration.fn._lang = moment.fn._lang = getLangDefinition(key);
            return r._abbr;
        };
        // returns language data
        moment.langData = function(key) {
            if (key && key._lang && key._lang._abbr) {
                key = key._lang._abbr;
            }
            return getLangDefinition(key);
        };
        // compare moment object
        moment.isMoment = function(obj) {
            return obj instanceof Moment || obj != null && obj.hasOwnProperty("_isAMomentObject");
        };
        // for typechecking Duration objects
        moment.isDuration = function(obj) {
            return obj instanceof Duration;
        };
        for (i = lists.length - 1; i >= 0; --i) {
            makeList(lists[i]);
        }
        moment.normalizeUnits = function(units) {
            return normalizeUnits(units);
        };
        moment.invalid = function(flags) {
            var m = moment.utc(NaN);
            if (flags != null) {
                extend(m._pf, flags);
            } else {
                m._pf.userInvalidated = true;
            }
            return m;
        };
        moment.parseZone = function() {
            return moment.apply(null, arguments).parseZone();
        };
        moment.parseTwoDigitYear = function(input) {
            return toInt(input) + (toInt(input) > 68 ? 1900 : 2e3);
        };
        /************************************
        Moment Prototype
    ************************************/
        extend(moment.fn = Moment.prototype, {
            clone: function() {
                return moment(this);
            },
            valueOf: function() {
                return +this._d + (this._offset || 0) * 6e4;
            },
            unix: function() {
                return Math.floor(+this / 1e3);
            },
            toString: function() {
                return this.clone().lang("en").format("ddd MMM DD YYYY HH:mm:ss [GMT]ZZ");
            },
            toDate: function() {
                return this._offset ? new Date(+this) : this._d;
            },
            toISOString: function() {
                var m = moment(this).utc();
                if (0 < m.year() && m.year() <= 9999) {
                    return formatMoment(m, "YYYY-MM-DD[T]HH:mm:ss.SSS[Z]");
                } else {
                    return formatMoment(m, "YYYYYY-MM-DD[T]HH:mm:ss.SSS[Z]");
                }
            },
            toArray: function() {
                var m = this;
                return [ m.year(), m.month(), m.date(), m.hours(), m.minutes(), m.seconds(), m.milliseconds() ];
            },
            isValid: function() {
                return isValid(this);
            },
            isDSTShifted: function() {
                if (this._a) {
                    return this.isValid() && compareArrays(this._a, (this._isUTC ? moment.utc(this._a) : moment(this._a)).toArray()) > 0;
                }
                return false;
            },
            parsingFlags: function() {
                return extend({}, this._pf);
            },
            invalidAt: function() {
                return this._pf.overflow;
            },
            utc: function() {
                return this.zone(0);
            },
            local: function() {
                this.zone(0);
                this._isUTC = false;
                return this;
            },
            format: function(inputString) {
                var output = formatMoment(this, inputString || moment.defaultFormat);
                return this.lang().postformat(output);
            },
            add: function(input, val) {
                var dur;
                // switch args to support add('s', 1) and add(1, 's')
                if (typeof input === "string") {
                    dur = moment.duration(+val, input);
                } else {
                    dur = moment.duration(input, val);
                }
                addOrSubtractDurationFromMoment(this, dur, 1);
                return this;
            },
            subtract: function(input, val) {
                var dur;
                // switch args to support subtract('s', 1) and subtract(1, 's')
                if (typeof input === "string") {
                    dur = moment.duration(+val, input);
                } else {
                    dur = moment.duration(input, val);
                }
                addOrSubtractDurationFromMoment(this, dur, -1);
                return this;
            },
            diff: function(input, units, asFloat) {
                var that = makeAs(input, this), zoneDiff = (this.zone() - that.zone()) * 6e4, diff, output;
                units = normalizeUnits(units);
                if (units === "year" || units === "month") {
                    // average number of days in the months in the given dates
                    diff = (this.daysInMonth() + that.daysInMonth()) * 432e5;
                    // 24 * 60 * 60 * 1000 / 2
                    // difference in months
                    output = (this.year() - that.year()) * 12 + (this.month() - that.month());
                    // adjust by taking difference in days, average number of days
                    // and dst in the given months.
                    output += (this - moment(this).startOf("month") - (that - moment(that).startOf("month"))) / diff;
                    // same as above but with zones, to negate all dst
                    output -= (this.zone() - moment(this).startOf("month").zone() - (that.zone() - moment(that).startOf("month").zone())) * 6e4 / diff;
                    if (units === "year") {
                        output = output / 12;
                    }
                } else {
                    diff = this - that;
                    output = units === "second" ? diff / 1e3 : // 1000
                    units === "minute" ? diff / 6e4 : // 1000 * 60
                    units === "hour" ? diff / 36e5 : // 1000 * 60 * 60
                    units === "day" ? (diff - zoneDiff) / 864e5 : // 1000 * 60 * 60 * 24, negate dst
                    units === "week" ? (diff - zoneDiff) / 6048e5 : // 1000 * 60 * 60 * 24 * 7, negate dst
                    diff;
                }
                return asFloat ? output : absRound(output);
            },
            from: function(time, withoutSuffix) {
                return moment.duration(this.diff(time)).lang(this.lang()._abbr).humanize(!withoutSuffix);
            },
            fromNow: function(withoutSuffix) {
                return this.from(moment(), withoutSuffix);
            },
            calendar: function() {
                // We want to compare the start of today, vs this.
                // Getting start-of-today depends on whether we're zone'd or not.
                var sod = makeAs(moment(), this).startOf("day"), diff = this.diff(sod, "days", true), format = diff < -6 ? "sameElse" : diff < -1 ? "lastWeek" : diff < 0 ? "lastDay" : diff < 1 ? "sameDay" : diff < 2 ? "nextDay" : diff < 7 ? "nextWeek" : "sameElse";
                return this.format(this.lang().calendar(format, this));
            },
            isLeapYear: function() {
                return isLeapYear(this.year());
            },
            isDST: function() {
                return this.zone() < this.clone().month(0).zone() || this.zone() < this.clone().month(5).zone();
            },
            day: function(input) {
                var day = this._isUTC ? this._d.getUTCDay() : this._d.getDay();
                if (input != null) {
                    input = parseWeekday(input, this.lang());
                    return this.add({
                        d: input - day
                    });
                } else {
                    return day;
                }
            },
            month: makeAccessor("Month", true),
            startOf: function(units) {
                units = normalizeUnits(units);
                // the following switch intentionally omits break keywords
                // to utilize falling through the cases.
                switch (units) {
                  case "year":
                    this.month(0);

                  /* falls through */
                    case "quarter":
                  case "month":
                    this.date(1);

                  /* falls through */
                    case "week":
                  case "isoWeek":
                  case "day":
                    this.hours(0);

                  /* falls through */
                    case "hour":
                    this.minutes(0);

                  /* falls through */
                    case "minute":
                    this.seconds(0);

                  /* falls through */
                    case "second":
                    this.milliseconds(0);
                }
                // weeks are a special case
                if (units === "week") {
                    this.weekday(0);
                } else if (units === "isoWeek") {
                    this.isoWeekday(1);
                }
                // quarters are also special
                if (units === "quarter") {
                    this.month(Math.floor(this.month() / 3) * 3);
                }
                return this;
            },
            endOf: function(units) {
                units = normalizeUnits(units);
                return this.startOf(units).add(units === "isoWeek" ? "week" : units, 1).subtract("ms", 1);
            },
            isAfter: function(input, units) {
                units = typeof units !== "undefined" ? units : "millisecond";
                return +this.clone().startOf(units) > +moment(input).startOf(units);
            },
            isBefore: function(input, units) {
                units = typeof units !== "undefined" ? units : "millisecond";
                return +this.clone().startOf(units) < +moment(input).startOf(units);
            },
            isSame: function(input, units) {
                units = units || "ms";
                return +this.clone().startOf(units) === +makeAs(input, this).startOf(units);
            },
            min: function(other) {
                other = moment.apply(null, arguments);
                return other < this ? this : other;
            },
            max: function(other) {
                other = moment.apply(null, arguments);
                return other > this ? this : other;
            },
            // keepTime = true means only change the timezone, without affecting
            // the local hour. So 5:31:26 +0300 --[zone(2, true)]--> 5:31:26 +0200
            // It is possible that 5:31:26 doesn't exist int zone +0200, so we
            // adjust the time as needed, to be valid.
            //
            // Keeping the time actually adds/subtracts (one hour)
            // from the actual represented time. That is why we call updateOffset
            // a second time. In case it wants us to change the offset again
            // _changeInProgress == true case, then we have to adjust, because
            // there is no such time in the given timezone.
            zone: function(input, keepTime) {
                var offset = this._offset || 0;
                if (input != null) {
                    if (typeof input === "string") {
                        input = timezoneMinutesFromString(input);
                    }
                    if (Math.abs(input) < 16) {
                        input = input * 60;
                    }
                    this._offset = input;
                    this._isUTC = true;
                    if (offset !== input) {
                        if (!keepTime || this._changeInProgress) {
                            addOrSubtractDurationFromMoment(this, moment.duration(offset - input, "m"), 1, false);
                        } else if (!this._changeInProgress) {
                            this._changeInProgress = true;
                            moment.updateOffset(this, true);
                            this._changeInProgress = null;
                        }
                    }
                } else {
                    return this._isUTC ? offset : this._d.getTimezoneOffset();
                }
                return this;
            },
            zoneAbbr: function() {
                return this._isUTC ? "UTC" : "";
            },
            zoneName: function() {
                return this._isUTC ? "Coordinated Universal Time" : "";
            },
            parseZone: function() {
                if (this._tzm) {
                    this.zone(this._tzm);
                } else if (typeof this._i === "string") {
                    this.zone(this._i);
                }
                return this;
            },
            hasAlignedHourOffset: function(input) {
                if (!input) {
                    input = 0;
                } else {
                    input = moment(input).zone();
                }
                return (this.zone() - input) % 60 === 0;
            },
            daysInMonth: function() {
                return daysInMonth(this.year(), this.month());
            },
            dayOfYear: function(input) {
                var dayOfYear = round((moment(this).startOf("day") - moment(this).startOf("year")) / 864e5) + 1;
                return input == null ? dayOfYear : this.add("d", input - dayOfYear);
            },
            quarter: function(input) {
                return input == null ? Math.ceil((this.month() + 1) / 3) : this.month((input - 1) * 3 + this.month() % 3);
            },
            weekYear: function(input) {
                var year = weekOfYear(this, this.lang()._week.dow, this.lang()._week.doy).year;
                return input == null ? year : this.add("y", input - year);
            },
            isoWeekYear: function(input) {
                var year = weekOfYear(this, 1, 4).year;
                return input == null ? year : this.add("y", input - year);
            },
            week: function(input) {
                var week = this.lang().week(this);
                return input == null ? week : this.add("d", (input - week) * 7);
            },
            isoWeek: function(input) {
                var week = weekOfYear(this, 1, 4).week;
                return input == null ? week : this.add("d", (input - week) * 7);
            },
            weekday: function(input) {
                var weekday = (this.day() + 7 - this.lang()._week.dow) % 7;
                return input == null ? weekday : this.add("d", input - weekday);
            },
            isoWeekday: function(input) {
                // behaves the same as moment#day except
                // as a getter, returns 7 instead of 0 (1-7 range instead of 0-6)
                // as a setter, sunday should belong to the previous week.
                return input == null ? this.day() || 7 : this.day(this.day() % 7 ? input : input - 7);
            },
            isoWeeksInYear: function() {
                return weeksInYear(this.year(), 1, 4);
            },
            weeksInYear: function() {
                var weekInfo = this._lang._week;
                return weeksInYear(this.year(), weekInfo.dow, weekInfo.doy);
            },
            get: function(units) {
                units = normalizeUnits(units);
                return this[units]();
            },
            set: function(units, value) {
                units = normalizeUnits(units);
                if (typeof this[units] === "function") {
                    this[units](value);
                }
                return this;
            },
            // If passed a language key, it will set the language for this
            // instance.  Otherwise, it will return the language configuration
            // variables for this instance.
            lang: function(key) {
                if (key === undefined) {
                    return this._lang;
                } else {
                    this._lang = getLangDefinition(key);
                    return this;
                }
            }
        });
        function rawMonthSetter(mom, value) {
            var dayOfMonth;
            // TODO: Move this out of here!
            if (typeof value === "string") {
                value = mom.lang().monthsParse(value);
                // TODO: Another silent failure?
                if (typeof value !== "number") {
                    return mom;
                }
            }
            dayOfMonth = Math.min(mom.date(), daysInMonth(mom.year(), value));
            mom._d["set" + (mom._isUTC ? "UTC" : "") + "Month"](value, dayOfMonth);
            return mom;
        }
        function rawGetter(mom, unit) {
            return mom._d["get" + (mom._isUTC ? "UTC" : "") + unit]();
        }
        function rawSetter(mom, unit, value) {
            if (unit === "Month") {
                return rawMonthSetter(mom, value);
            } else {
                return mom._d["set" + (mom._isUTC ? "UTC" : "") + unit](value);
            }
        }
        function makeAccessor(unit, keepTime) {
            return function(value) {
                if (value != null) {
                    rawSetter(this, unit, value);
                    moment.updateOffset(this, keepTime);
                    return this;
                } else {
                    return rawGetter(this, unit);
                }
            };
        }
        moment.fn.millisecond = moment.fn.milliseconds = makeAccessor("Milliseconds", false);
        moment.fn.second = moment.fn.seconds = makeAccessor("Seconds", false);
        moment.fn.minute = moment.fn.minutes = makeAccessor("Minutes", false);
        // Setting the hour should keep the time, because the user explicitly
        // specified which hour he wants. So trying to maintain the same hour (in
        // a new timezone) makes sense. Adding/subtracting hours does not follow
        // this rule.
        moment.fn.hour = moment.fn.hours = makeAccessor("Hours", true);
        // moment.fn.month is defined separately
        moment.fn.date = makeAccessor("Date", true);
        moment.fn.dates = deprecate("dates accessor is deprecated. Use date instead.", makeAccessor("Date", true));
        moment.fn.year = makeAccessor("FullYear", true);
        moment.fn.years = deprecate("years accessor is deprecated. Use year instead.", makeAccessor("FullYear", true));
        // add plural methods
        moment.fn.days = moment.fn.day;
        moment.fn.months = moment.fn.month;
        moment.fn.weeks = moment.fn.week;
        moment.fn.isoWeeks = moment.fn.isoWeek;
        moment.fn.quarters = moment.fn.quarter;
        // add aliased format methods
        moment.fn.toJSON = moment.fn.toISOString;
        /************************************
        Duration Prototype
    ************************************/
        extend(moment.duration.fn = Duration.prototype, {
            _bubble: function() {
                var milliseconds = this._milliseconds, days = this._days, months = this._months, data = this._data, seconds, minutes, hours, years;
                // The following code bubbles up values, see the tests for
                // examples of what that means.
                data.milliseconds = milliseconds % 1e3;
                seconds = absRound(milliseconds / 1e3);
                data.seconds = seconds % 60;
                minutes = absRound(seconds / 60);
                data.minutes = minutes % 60;
                hours = absRound(minutes / 60);
                data.hours = hours % 24;
                days += absRound(hours / 24);
                data.days = days % 30;
                months += absRound(days / 30);
                data.months = months % 12;
                years = absRound(months / 12);
                data.years = years;
            },
            weeks: function() {
                return absRound(this.days() / 7);
            },
            valueOf: function() {
                return this._milliseconds + this._days * 864e5 + this._months % 12 * 2592e6 + toInt(this._months / 12) * 31536e6;
            },
            humanize: function(withSuffix) {
                var difference = +this, output = relativeTime(difference, !withSuffix, this.lang());
                if (withSuffix) {
                    output = this.lang().pastFuture(difference, output);
                }
                return this.lang().postformat(output);
            },
            add: function(input, val) {
                // supports only 2.0-style add(1, 's') or add(moment)
                var dur = moment.duration(input, val);
                this._milliseconds += dur._milliseconds;
                this._days += dur._days;
                this._months += dur._months;
                this._bubble();
                return this;
            },
            subtract: function(input, val) {
                var dur = moment.duration(input, val);
                this._milliseconds -= dur._milliseconds;
                this._days -= dur._days;
                this._months -= dur._months;
                this._bubble();
                return this;
            },
            get: function(units) {
                units = normalizeUnits(units);
                return this[units.toLowerCase() + "s"]();
            },
            as: function(units) {
                units = normalizeUnits(units);
                return this["as" + units.charAt(0).toUpperCase() + units.slice(1) + "s"]();
            },
            lang: moment.fn.lang,
            toIsoString: function() {
                // inspired by https://github.com/dordille/moment-isoduration/blob/master/moment.isoduration.js
                var years = Math.abs(this.years()), months = Math.abs(this.months()), days = Math.abs(this.days()), hours = Math.abs(this.hours()), minutes = Math.abs(this.minutes()), seconds = Math.abs(this.seconds() + this.milliseconds() / 1e3);
                if (!this.asSeconds()) {
                    // this is the same as C#'s (Noda) and python (isodate)...
                    // but not other JS (goog.date)
                    return "P0D";
                }
                return (this.asSeconds() < 0 ? "-" : "") + "P" + (years ? years + "Y" : "") + (months ? months + "M" : "") + (days ? days + "D" : "") + (hours || minutes || seconds ? "T" : "") + (hours ? hours + "H" : "") + (minutes ? minutes + "M" : "") + (seconds ? seconds + "S" : "");
            }
        });
        function makeDurationGetter(name) {
            moment.duration.fn[name] = function() {
                return this._data[name];
            };
        }
        function makeDurationAsGetter(name, factor) {
            moment.duration.fn["as" + name] = function() {
                return +this / factor;
            };
        }
        for (i in unitMillisecondFactors) {
            if (unitMillisecondFactors.hasOwnProperty(i)) {
                makeDurationAsGetter(i, unitMillisecondFactors[i]);
                makeDurationGetter(i.toLowerCase());
            }
        }
        makeDurationAsGetter("Weeks", 6048e5);
        moment.duration.fn.asMonths = function() {
            return (+this - this.years() * 31536e6) / 2592e6 + this.years() * 12;
        };
        /************************************
        Default Lang
    ************************************/
        // Set default language, other languages will inherit from English.
        moment.lang("en", {
            ordinal: function(number) {
                var b = number % 10, output = toInt(number % 100 / 10) === 1 ? "th" : b === 1 ? "st" : b === 2 ? "nd" : b === 3 ? "rd" : "th";
                return number + output;
            }
        });
        /* EMBED_LANGUAGES */
        /************************************
        Exposing Moment
    ************************************/
        function makeGlobal(shouldDeprecate) {
            /*global ender:false */
            if (typeof ender !== "undefined") {
                return;
            }
            oldGlobalMoment = globalScope.moment;
            if (shouldDeprecate) {
                globalScope.moment = deprecate("Accessing Moment through the global scope is " + "deprecated, and will be removed in an upcoming " + "release.", moment);
            } else {
                globalScope.moment = moment;
            }
        }
        // CommonJS module is defined
        if (hasModule) {
            module.exports = moment;
        } else if (typeof define === "function" && define.amd) {
            define("moment", function(require, exports, module) {
                if (module.config && module.config() && module.config().noGlobal === true) {
                    // release the global variable
                    globalScope.moment = oldGlobalMoment;
                }
                return moment;
            });
            makeGlobal(true);
        } else {
            makeGlobal();
        }
    }).call(this);
});

define("torabot/main/0.1.0/moment/lang/zh-cn-debug", [ "torabot/main/0.1.0/moment/moment-debug" ], function(require) {
    // moment.js language configuration
    // language : chinese
    // author : suupic : https://github.com/suupic
    // author : Zeno Zeng : https://github.com/zenozeng
    (function(factory) {
        if (typeof define === "function" && define.amd) {
            define([ "moment" ], factory);
        } else if (typeof exports === "object") {
            module.exports = factory(require("torabot/main/0.1.0/moment/moment-debug"));
        } else {
            factory(window.moment);
        }
    })(function(moment) {
        return moment.lang("zh-cn", {
            months: "一月_二月_三月_四月_五月_六月_七月_八月_九月_十月_十一月_十二月".split("_"),
            monthsShort: "1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月".split("_"),
            weekdays: "星期日_星期一_星期二_星期三_星期四_星期五_星期六".split("_"),
            weekdaysShort: "周日_周一_周二_周三_周四_周五_周六".split("_"),
            weekdaysMin: "日_一_二_三_四_五_六".split("_"),
            longDateFormat: {
                LT: "Ah点mm",
                L: "YYYY-MM-DD",
                LL: "YYYY年MMMD日",
                LLL: "YYYY年MMMD日LT",
                LLLL: "YYYY年MMMD日ddddLT",
                l: "YYYY-MM-DD",
                ll: "YYYY年MMMD日",
                lll: "YYYY年MMMD日LT",
                llll: "YYYY年MMMD日ddddLT"
            },
            meridiem: function(hour, minute, isLower) {
                var hm = hour * 100 + minute;
                if (hm < 600) {
                    return "凌晨";
                } else if (hm < 900) {
                    return "早上";
                } else if (hm < 1130) {
                    return "上午";
                } else if (hm < 1230) {
                    return "中午";
                } else if (hm < 1800) {
                    return "下午";
                } else {
                    return "晚上";
                }
            },
            calendar: {
                sameDay: function() {
                    return this.minutes() === 0 ? "[今天]Ah[点整]" : "[今天]LT";
                },
                nextDay: function() {
                    return this.minutes() === 0 ? "[明天]Ah[点整]" : "[明天]LT";
                },
                lastDay: function() {
                    return this.minutes() === 0 ? "[昨天]Ah[点整]" : "[昨天]LT";
                },
                nextWeek: function() {
                    var startOfWeek, prefix;
                    startOfWeek = moment().startOf("week");
                    prefix = this.unix() - startOfWeek.unix() >= 7 * 24 * 3600 ? "[下]" : "[本]";
                    return this.minutes() === 0 ? prefix + "dddAh点整" : prefix + "dddAh点mm";
                },
                lastWeek: function() {
                    var startOfWeek, prefix;
                    startOfWeek = moment().startOf("week");
                    prefix = this.unix() < startOfWeek.unix() ? "[上]" : "[本]";
                    return this.minutes() === 0 ? prefix + "dddAh点整" : prefix + "dddAh点mm";
                },
                sameElse: "LL"
            },
            ordinal: function(number, period) {
                switch (period) {
                  case "d":
                  case "D":
                  case "DDD":
                    return number + "日";

                  case "M":
                    return number + "月";

                  case "w":
                  case "W":
                    return number + "周";

                  default:
                    return number;
                }
            },
            relativeTime: {
                future: "%s内",
                past: "%s前",
                s: "几秒",
                m: "1分钟",
                mm: "%d分钟",
                h: "1小时",
                hh: "%d小时",
                d: "1天",
                dd: "%d天",
                M: "1个月",
                MM: "%d个月",
                y: "1年",
                yy: "%d年"
            },
            week: {
                // GB/T 7408-1994《数据元和交换格式·信息交换·日期和时间表示法》与ISO 8601:1988等效
                dow: 1,
                // Monday is the first day of the week.
                doy: 4
            }
        });
    });
});

define("torabot/main/0.1.0/pnotify.custom.min-debug", [], function(require) {
    /*
PNotify 2.0.0 sciactive.com/pnotify/
(C) 2014 Hunter Perrin
license GPL/LGPL/MPL
*/
    (function(c) {
        "function" === typeof define && define.amd ? define([ "jquery" ], c) : c(jQuery);
    })(function(c) {
        var n = {
            dir1: "down",
            dir2: "left",
            push: "bottom",
            spacing1: 25,
            spacing2: 25,
            context: c("body")
        }, f, g, h = c(window), m = function() {
            g = c("body");
            PNotify.prototype.options.stack.context = g;
            h = c(window);
            h.bind("resize", function() {
                f && clearTimeout(f);
                f = setTimeout(function() {
                    PNotify.positionAll(!0);
                }, 10);
            });
        };
        PNotify = function(b) {
            this.parseOptions(b);
            this.init();
        };
        c.extend(PNotify.prototype, {
            version: "2.0.0",
            options: {
                title: !1,
                title_escape: !1,
                text: !1,
                text_escape: !1,
                styling: "bootstrap3",
                addclass: "",
                cornerclass: "",
                auto_display: !0,
                width: "300px",
                min_height: "16px",
                type: "notice",
                icon: !0,
                opacity: 1,
                animation: "fade",
                animate_speed: "slow",
                position_animate_speed: 500,
                shadow: !0,
                hide: !0,
                delay: 8e3,
                mouse_reset: !0,
                remove: !0,
                insert_brs: !0,
                destroy: !0,
                stack: n
            },
            modules: {},
            runModules: function(b, a) {
                var c, d;
                for (d in this.modules) if (c = "object" === typeof a && d in a ? a[d] : a, "function" === typeof this.modules[d][b]) this.modules[d][b](this, "object" === typeof this.options[d] ? this.options[d] : {}, c);
            },
            state: "initializing",
            timer: null,
            styles: null,
            elem: null,
            container: null,
            title_container: null,
            text_container: null,
            animating: !1,
            timerHide: !1,
            init: function() {
                var b = this;
                this.modules = {};
                c.extend(!0, this.modules, PNotify.prototype.modules);
                this.styles = "object" === typeof this.options.styling ? this.options.styling : PNotify.styling[this.options.styling];
                this.elem = c("<div />", {
                    "class": "ui-pnotify " + this.options.addclass,
                    css: {
                        display: "none"
                    },
                    mouseenter: function(a) {
                        if (b.options.mouse_reset && "out" === b.animating) {
                            if (!b.timerHide) return;
                            b.elem.stop(!0);
                            b.state = "open";
                            b.animating = "in";
                            b.elem.css("height", "auto").animate({
                                width: b.options.width,
                                opacity: b.options.opacity
                            }, "fast");
                        }
                        b.options.hide && b.options.mouse_reset && b.cancelRemove();
                    },
                    mouseleave: function(a) {
                        b.options.hide && b.options.mouse_reset && b.queueRemove();
                        PNotify.positionAll();
                    }
                });
                this.container = c("<div />", {
                    "class": this.styles.container + " ui-pnotify-container " + ("error" === this.options.type ? this.styles.error : "info" === this.options.type ? this.styles.info : "success" === this.options.type ? this.styles.success : this.styles.notice)
                }).appendTo(this.elem);
                "" !== this.options.cornerclass && this.container.removeClass("ui-corner-all").addClass(this.options.cornerclass);
                this.options.shadow && this.container.addClass("ui-pnotify-shadow");
                !1 !== this.options.icon && c("<div />", {
                    "class": "ui-pnotify-icon"
                }).append(c("<span />", {
                    "class": !0 === this.options.icon ? "error" === this.options.type ? this.styles.error_icon : "info" === this.options.type ? this.styles.info_icon : "success" === this.options.type ? this.styles.success_icon : this.styles.notice_icon : this.options.icon
                })).prependTo(this.container);
                this.title_container = c("<h4 />", {
                    "class": "ui-pnotify-title"
                }).appendTo(this.container);
                !1 === this.options.title ? this.title_container.hide() : this.options.title_escape ? this.title_container.text(this.options.title) : this.title_container.html(this.options.title);
                this.text_container = c("<div />", {
                    "class": "ui-pnotify-text"
                }).appendTo(this.container);
                !1 === this.options.text ? this.text_container.hide() : this.options.text_escape ? this.text_container.text(this.options.text) : this.text_container.html(this.options.insert_brs ? String(this.options.text).replace(/\n/g, "<br />") : this.options.text);
                "string" === typeof this.options.width && this.elem.css("width", this.options.width);
                "string" === typeof this.options.min_height && this.container.css("min-height", this.options.min_height);
                PNotify.notices = "top" === this.options.stack.push ? c.merge([ this ], PNotify.notices) : c.merge(PNotify.notices, [ this ]);
                "top" === this.options.stack.push && this.queuePosition(!1, 1);
                this.options.stack.animation = !1;
                this.runModules("init");
                this.options.auto_display && this.open();
                return this;
            },
            update: function(b) {
                var a = this.options;
                this.parseOptions(a, b);
                this.options.cornerclass !== a.cornerclass && this.container.removeClass("ui-corner-all " + a.cornerclass).addClass(this.options.cornerclass);
                this.options.shadow !== a.shadow && (this.options.shadow ? this.container.addClass("ui-pnotify-shadow") : this.container.removeClass("ui-pnotify-shadow"));
                !1 === this.options.addclass ? this.elem.removeClass(a.addclass) : this.options.addclass !== a.addclass && this.elem.removeClass(a.addclass).addClass(this.options.addclass);
                !1 === this.options.title ? this.title_container.slideUp("fast") : this.options.title !== a.title && (this.options.title_escape ? this.title_container.text(this.options.title) : this.title_container.html(this.options.title), 
                !1 === a.title && this.title_container.slideDown(200));
                !1 === this.options.text ? this.text_container.slideUp("fast") : this.options.text !== a.text && (this.options.text_escape ? this.text_container.text(this.options.text) : this.text_container.html(this.options.insert_brs ? String(this.options.text).replace(/\n/g, "<br />") : this.options.text), 
                !1 === a.text && this.text_container.slideDown(200));
                this.options.type !== a.type && this.container.removeClass(this.styles.error + " " + this.styles.notice + " " + this.styles.success + " " + this.styles.info).addClass("error" === this.options.type ? this.styles.error : "info" === this.options.type ? this.styles.info : "success" === this.options.type ? this.styles.success : this.styles.notice);
                if (this.options.icon !== a.icon || !0 === this.options.icon && this.options.type !== a.type) this.container.find("div.ui-pnotify-icon").remove(), 
                !1 !== this.options.icon && c("<div />", {
                    "class": "ui-pnotify-icon"
                }).append(c("<span />", {
                    "class": !0 === this.options.icon ? "error" === this.options.type ? this.styles.error_icon : "info" === this.options.type ? this.styles.info_icon : "success" === this.options.type ? this.styles.success_icon : this.styles.notice_icon : this.options.icon
                })).prependTo(this.container);
                this.options.width !== a.width && this.elem.animate({
                    width: this.options.width
                });
                this.options.min_height !== a.min_height && this.container.animate({
                    minHeight: this.options.min_height
                });
                this.options.opacity !== a.opacity && this.elem.fadeTo(this.options.animate_speed, this.options.opacity);
                this.options.hide ? a.hide || this.queueRemove() : this.cancelRemove();
                this.queuePosition(!0);
                this.runModules("update", a);
                return this;
            },
            open: function() {
                this.state = "opening";
                this.runModules("beforeOpen");
                var b = this;
                this.elem.parent().length || this.elem.appendTo(this.options.stack.context ? this.options.stack.context : g);
                "top" !== this.options.stack.push && this.position(!0);
                "fade" === this.options.animation || "fade" === this.options.animation.effect_in ? this.elem.show().fadeTo(0, 0).hide() : 1 !== this.options.opacity && this.elem.show().fadeTo(0, this.options.opacity).hide();
                this.animateIn(function() {
                    b.queuePosition(!0);
                    b.options.hide && b.queueRemove();
                    b.state = "open";
                    b.runModules("afterOpen");
                });
                return this;
            },
            remove: function(b) {
                this.state = "closing";
                this.timerHide = !!b;
                this.runModules("beforeClose");
                var a = this;
                this.timer && (window.clearTimeout(this.timer), this.timer = null);
                this.animateOut(function() {
                    a.state = "closed";
                    a.runModules("afterClose");
                    a.queuePosition(!0);
                    a.options.remove && a.elem.detach();
                    a.runModules("beforeDestroy");
                    if (a.options.destroy && null !== PNotify.notices) {
                        var b = c.inArray(a, PNotify.notices);
                        -1 !== b && PNotify.notices.splice(b, 1);
                    }
                    a.runModules("afterDestroy");
                });
                return this;
            },
            get: function() {
                return this.elem;
            },
            parseOptions: function(b, a) {
                this.options = c.extend(!0, {}, PNotify.prototype.options);
                this.options.stack = PNotify.prototype.options.stack;
                var f = [ b, a ], d, e;
                for (e in f) {
                    d = f[e];
                    if ("undefined" == typeof d) break;
                    if ("object" !== typeof d) this.options.text = d; else for (var l in d) this.modules[l] ? c.extend(!0, this.options[l], d[l]) : this.options[l] = d[l];
                }
            },
            animateIn: function(b) {
                this.animating = "in";
                var a;
                a = "undefined" !== typeof this.options.animation.effect_in ? this.options.animation.effect_in : this.options.animation;
                "none" === a ? (this.elem.show(), b()) : "show" === a ? this.elem.show(this.options.animate_speed, b) : "fade" === a ? this.elem.show().fadeTo(this.options.animate_speed, this.options.opacity, b) : "slide" === a ? this.elem.slideDown(this.options.animate_speed, b) : "function" === typeof a ? a("in", b, this.elem) : this.elem.show(a, "object" === typeof this.options.animation.options_in ? this.options.animation.options_in : {}, this.options.animate_speed, b);
            },
            animateOut: function(b) {
                this.animating = "out";
                var a;
                a = "undefined" !== typeof this.options.animation.effect_out ? this.options.animation.effect_out : this.options.animation;
                "none" === a ? (this.elem.hide(), b()) : "show" === a ? this.elem.hide(this.options.animate_speed, b) : "fade" === a ? this.elem.fadeOut(this.options.animate_speed, b) : "slide" === a ? this.elem.slideUp(this.options.animate_speed, b) : "function" === typeof a ? a("out", b, this.elem) : this.elem.hide(a, "object" === typeof this.options.animation.options_out ? this.options.animation.options_out : {}, this.options.animate_speed, b);
            },
            position: function(b) {
                var a = this.options.stack;
                "undefined" === typeof a.context && (a.context = g);
                if (a) {
                    "number" !== typeof a.nextpos1 && (a.nextpos1 = a.firstpos1);
                    "number" !== typeof a.nextpos2 && (a.nextpos2 = a.firstpos2);
                    "number" !== typeof a.addpos2 && (a.addpos2 = 0);
                    var c = "none" === this.elem.css("display");
                    if (!c || b) {
                        var d, e = {}, f;
                        switch (a.dir1) {
                          case "down":
                            f = "top";
                            break;

                          case "up":
                            f = "bottom";
                            break;

                          case "left":
                            f = "right";
                            break;

                          case "right":
                            f = "left";
                        }
                        b = parseInt(this.elem.css(f).replace(/(?:\..*|[^0-9.])/g, ""));
                        isNaN(b) && (b = 0);
                        "undefined" !== typeof a.firstpos1 || c || (a.firstpos1 = b, a.nextpos1 = a.firstpos1);
                        var k;
                        switch (a.dir2) {
                          case "down":
                            k = "top";
                            break;

                          case "up":
                            k = "bottom";
                            break;

                          case "left":
                            k = "right";
                            break;

                          case "right":
                            k = "left";
                        }
                        d = parseInt(this.elem.css(k).replace(/(?:\..*|[^0-9.])/g, ""));
                        isNaN(d) && (d = 0);
                        "undefined" !== typeof a.firstpos2 || c || (a.firstpos2 = d, a.nextpos2 = a.firstpos2);
                        if ("down" === a.dir1 && a.nextpos1 + this.elem.height() > (a.context.is(g) ? h.height() : a.context.prop("scrollHeight")) || "up" === a.dir1 && a.nextpos1 + this.elem.height() > (a.context.is(g) ? h.height() : a.context.prop("scrollHeight")) || "left" === a.dir1 && a.nextpos1 + this.elem.width() > (a.context.is(g) ? h.width() : a.context.prop("scrollWidth")) || "right" === a.dir1 && a.nextpos1 + this.elem.width() > (a.context.is(g) ? h.width() : a.context.prop("scrollWidth"))) a.nextpos1 = a.firstpos1, 
                        a.nextpos2 += a.addpos2 + ("undefined" === typeof a.spacing2 ? 25 : a.spacing2), 
                        a.addpos2 = 0;
                        if (a.animation && a.nextpos2 < d) switch (a.dir2) {
                          case "down":
                            e.top = a.nextpos2 + "px";
                            break;

                          case "up":
                            e.bottom = a.nextpos2 + "px";
                            break;

                          case "left":
                            e.right = a.nextpos2 + "px";
                            break;

                          case "right":
                            e.left = a.nextpos2 + "px";
                        } else "number" === typeof a.nextpos2 && this.elem.css(k, a.nextpos2 + "px");
                        switch (a.dir2) {
                          case "down":
                          case "up":
                            this.elem.outerHeight(!0) > a.addpos2 && (a.addpos2 = this.elem.height());
                            break;

                          case "left":
                          case "right":
                            this.elem.outerWidth(!0) > a.addpos2 && (a.addpos2 = this.elem.width());
                        }
                        if ("number" === typeof a.nextpos1) if (a.animation && (b > a.nextpos1 || e.top || e.bottom || e.right || e.left)) switch (a.dir1) {
                          case "down":
                            e.top = a.nextpos1 + "px";
                            break;

                          case "up":
                            e.bottom = a.nextpos1 + "px";
                            break;

                          case "left":
                            e.right = a.nextpos1 + "px";
                            break;

                          case "right":
                            e.left = a.nextpos1 + "px";
                        } else this.elem.css(f, a.nextpos1 + "px");
                        (e.top || e.bottom || e.right || e.left) && this.elem.animate(e, {
                            duration: this.options.position_animate_speed,
                            queue: !1
                        });
                        switch (a.dir1) {
                          case "down":
                          case "up":
                            a.nextpos1 += this.elem.height() + ("undefined" === typeof a.spacing1 ? 25 : a.spacing1);
                            break;

                          case "left":
                          case "right":
                            a.nextpos1 += this.elem.width() + ("undefined" === typeof a.spacing1 ? 25 : a.spacing1);
                        }
                    }
                    return this;
                }
            },
            queuePosition: function(b, a) {
                f && clearTimeout(f);
                a || (a = 10);
                f = setTimeout(function() {
                    PNotify.positionAll(b);
                }, a);
                return this;
            },
            cancelRemove: function() {
                this.timer && window.clearTimeout(this.timer);
                return this;
            },
            queueRemove: function() {
                var b = this;
                this.cancelRemove();
                this.timer = window.setTimeout(function() {
                    b.remove(!0);
                }, isNaN(this.options.delay) ? 0 : this.options.delay);
                return this;
            }
        });
        c.extend(PNotify, {
            notices: [],
            removeAll: function() {
                c.each(PNotify.notices, function() {
                    this.remove && this.remove();
                });
            },
            positionAll: function(b) {
                f && clearTimeout(f);
                f = null;
                c.each(PNotify.notices, function() {
                    var a = this.options.stack;
                    a && (a.nextpos1 = a.firstpos1, a.nextpos2 = a.firstpos2, a.addpos2 = 0, a.animation = b);
                });
                c.each(PNotify.notices, function() {
                    this.position();
                });
            },
            styling: {
                jqueryui: {
                    container: "ui-widget ui-widget-content ui-corner-all",
                    notice: "ui-state-highlight",
                    notice_icon: "ui-icon ui-icon-info",
                    info: "",
                    info_icon: "ui-icon ui-icon-info",
                    success: "ui-state-default",
                    success_icon: "ui-icon ui-icon-circle-check",
                    error: "ui-state-error",
                    error_icon: "ui-icon ui-icon-alert"
                },
                bootstrap2: {
                    container: "alert",
                    notice: "",
                    notice_icon: "icon-exclamation-sign",
                    info: "alert-info",
                    info_icon: "icon-info-sign",
                    success: "alert-success",
                    success_icon: "icon-ok-sign",
                    error: "alert-error",
                    error_icon: "icon-warning-sign"
                },
                bootstrap3: {
                    container: "alert",
                    notice: "alert-warning",
                    notice_icon: "glyphicon glyphicon-exclamation-sign",
                    info: "alert-info",
                    info_icon: "glyphicon glyphicon-info-sign",
                    success: "alert-success",
                    success_icon: "glyphicon glyphicon-ok-sign",
                    error: "alert-danger",
                    error_icon: "glyphicon glyphicon-warning-sign"
                }
            }
        });
        PNotify.styling.fontawesome = c.extend({}, PNotify.styling.bootstrap3);
        c.extend(PNotify.styling.fontawesome, {
            notice_icon: "fa fa-exclamation-circle",
            info_icon: "fa fa-info",
            success_icon: "fa fa-check",
            error_icon: "fa fa-warning"
        });
        document.body ? m() : c(m);
    });
    (function(c) {
        PNotify.prototype.options.buttons = {
            closer: !0,
            closer_hover: !0,
            sticker: !0,
            sticker_hover: !0,
            labels: {
                close: "Close",
                stick: "Stick"
            }
        };
        PNotify.prototype.modules.buttons = {
            myOptions: null,
            closer: null,
            sticker: null,
            init: function(a, b) {
                var d = this;
                this.myOptions = b;
                a.elem.on({
                    mouseenter: function(b) {
                        !d.myOptions.sticker || a.options.nonblock && a.options.nonblock.nonblock || d.sticker.trigger("pnotify_icon").css("visibility", "visible");
                        !d.myOptions.closer || a.options.nonblock && a.options.nonblock.nonblock || d.closer.css("visibility", "visible");
                    },
                    mouseleave: function(a) {
                        d.myOptions.sticker_hover && d.sticker.css("visibility", "hidden");
                        d.myOptions.closer_hover && d.closer.css("visibility", "hidden");
                    }
                });
                this.sticker = c("<div />", {
                    "class": "ui-pnotify-sticker",
                    css: {
                        cursor: "pointer",
                        visibility: b.sticker_hover ? "hidden" : "visible"
                    },
                    click: function() {
                        a.options.hide = !a.options.hide;
                        a.options.hide ? a.queueRemove() : a.cancelRemove();
                        c(this).trigger("pnotify_icon");
                    }
                }).bind("pnotify_icon", function() {
                    c(this).children().removeClass(a.styles.pin_up + " " + a.styles.pin_down).addClass(a.options.hide ? a.styles.pin_up : a.styles.pin_down);
                }).append(c("<span />", {
                    "class": a.styles.pin_up,
                    title: b.labels.stick
                })).prependTo(a.container);
                (!b.sticker || a.options.nonblock && a.options.nonblock.nonblock) && this.sticker.css("display", "none");
                this.closer = c("<div />", {
                    "class": "ui-pnotify-closer",
                    css: {
                        cursor: "pointer",
                        visibility: b.closer_hover ? "hidden" : "visible"
                    },
                    click: function() {
                        a.remove(!1);
                        d.sticker.css("visibility", "hidden");
                        d.closer.css("visibility", "hidden");
                    }
                }).append(c("<span />", {
                    "class": a.styles.closer,
                    title: b.labels.close
                })).prependTo(a.container);
                (!b.closer || a.options.nonblock && a.options.nonblock.nonblock) && this.closer.css("display", "none");
            },
            update: function(a, b) {
                this.myOptions = b;
                !b.closer || a.options.nonblock && a.options.nonblock.nonblock ? this.closer.css("display", "none") : b.closer && this.closer.css("display", "block");
                !b.sticker || a.options.nonblock && a.options.nonblock.nonblock ? this.sticker.css("display", "none") : b.sticker && this.sticker.css("display", "block");
                this.sticker.trigger("pnotify_icon");
                b.sticker_hover ? this.sticker.css("visibility", "hidden") : a.options.nonblock && a.options.nonblock.nonblock || this.sticker.css("visibility", "visible");
                b.closer_hover ? this.closer.css("visibility", "hidden") : a.options.nonblock && a.options.nonblock.nonblock || this.closer.css("visibility", "visible");
            }
        };
        c.extend(PNotify.styling.jqueryui, {
            closer: "ui-icon ui-icon-close",
            pin_up: "ui-icon ui-icon-pin-w",
            pin_down: "ui-icon ui-icon-pin-s"
        });
        c.extend(PNotify.styling.bootstrap2, {
            closer: "icon-remove",
            pin_up: "icon-pause",
            pin_down: "icon-play"
        });
        c.extend(PNotify.styling.bootstrap3, {
            closer: "glyphicon glyphicon-remove",
            pin_up: "glyphicon glyphicon-pause",
            pin_down: "glyphicon glyphicon-play"
        });
        c.extend(PNotify.styling.fontawesome, {
            closer: "fa fa-times",
            pin_up: "fa fa-pause",
            pin_down: "fa fa-play"
        });
    })(jQuery);
    (function(k) {
        var f = /^on/, l = /^(dbl)?click$|^mouse(move|down|up|over|out|enter|leave)$|^contextmenu$/, m = /^(focus|blur|select|change|reset)$|^key(press|down|up)$/, n = /^(scroll|resize|(un)?load|abort|error)$/, g = function(b, a) {
            var c;
            b = b.toLowerCase();
            document.createEvent && this.dispatchEvent ? (b = b.replace(f, ""), b.match(l) ? (k(this).offset(), 
            c = document.createEvent("MouseEvents"), c.initMouseEvent(b, a.bubbles, a.cancelable, a.view, a.detail, a.screenX, a.screenY, a.clientX, a.clientY, a.ctrlKey, a.altKey, a.shiftKey, a.metaKey, a.button, a.relatedTarget)) : b.match(m) ? (c = document.createEvent("UIEvents"), 
            c.initUIEvent(b, a.bubbles, a.cancelable, a.view, a.detail)) : b.match(n) && (c = document.createEvent("HTMLEvents"), 
            c.initEvent(b, a.bubbles, a.cancelable)), c && this.dispatchEvent(c)) : (b.match(f) || (b = "on" + b), 
            c = document.createEventObject(a), this.fireEvent(b, c));
        }, e, d = function(b, a, c) {
            b.elem.css("display", "none");
            var h = document.elementFromPoint(a.clientX, a.clientY);
            b.elem.css("display", "block");
            var d = k(h), f = d.css("cursor");
            b.elem.css("cursor", "auto" !== f ? f : "default");
            e && e.get(0) == h || (e && (g.call(e.get(0), "mouseleave", a.originalEvent), g.call(e.get(0), "mouseout", a.originalEvent)), 
            g.call(h, "mouseenter", a.originalEvent), g.call(h, "mouseover", a.originalEvent));
            g.call(h, c, a.originalEvent);
            e = d;
        };
        PNotify.prototype.options.nonblock = {
            nonblock: !1,
            nonblock_opacity: .2
        };
        PNotify.prototype.modules.nonblock = {
            myOptions: null,
            init: function(b, a) {
                var c = this;
                this.myOptions = a;
                b.elem.on({
                    mouseenter: function(a) {
                        c.myOptions.nonblock && a.stopPropagation();
                        c.myOptions.nonblock && b.elem.stop().animate({
                            opacity: c.myOptions.nonblock_opacity
                        }, "fast");
                    },
                    mouseleave: function(a) {
                        c.myOptions.nonblock && a.stopPropagation();
                        e = null;
                        b.elem.css("cursor", "auto");
                        c.myOptions.nonblock && "out" !== b.animating && b.elem.stop().animate({
                            opacity: b.options.opacity
                        }, "fast");
                    },
                    mouseover: function(a) {
                        c.myOptions.nonblock && a.stopPropagation();
                    },
                    mouseout: function(a) {
                        c.myOptions.nonblock && a.stopPropagation();
                    },
                    mousemove: function(a) {
                        c.myOptions.nonblock && (a.stopPropagation(), d(b, a, "onmousemove"));
                    },
                    mousedown: function(a) {
                        c.myOptions.nonblock && (a.stopPropagation(), a.preventDefault(), d(b, a, "onmousedown"));
                    },
                    mouseup: function(a) {
                        c.myOptions.nonblock && (a.stopPropagation(), a.preventDefault(), d(b, a, "onmouseup"));
                    },
                    click: function(a) {
                        c.myOptions.nonblock && (a.stopPropagation(), d(b, a, "onclick"));
                    },
                    dblclick: function(a) {
                        c.myOptions.nonblock && (a.stopPropagation(), d(b, a, "ondblclick"));
                    }
                });
            },
            update: function(b, a) {
                this.myOptions = a;
            }
        };
    })(jQuery);
});

define("torabot/main/0.1.0/switch-debug", [ "torabot/main/0.1.0/bootstrap-switch/bootstrap-switch-debug" ], function(require) {
    require("torabot/main/0.1.0/bootstrap-switch/bootstrap-switch-debug");
    $(".dropdown-menu .bootstrap-switch").click(function(e) {
        e.stopPropagation();
    });
});

define("torabot/main/0.1.0/bootstrap-switch/bootstrap-switch-debug", [], function(require) {
    /* ========================================================================
 * bootstrap-switch - v3.0.0
 * http://www.bootstrap-switch.org
 * ========================================================================
 * Copyright 2012-2013 Mattia Larentis
 *
 * ========================================================================
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================================
 */
    (function() {
        var __slice = [].slice;
        (function($, window) {
            "use strict";
            var BootstrapSwitch;
            BootstrapSwitch = function() {
                BootstrapSwitch.prototype.name = "bootstrap-switch";
                function BootstrapSwitch(element, options) {
                    if (options == null) {
                        options = {};
                    }
                    this.$element = $(element);
                    this.options = $.extend({}, $.fn.bootstrapSwitch.defaults, options, {
                        state: this.$element.is(":checked"),
                        size: this.$element.data("size"),
                        animate: this.$element.data("animate"),
                        disabled: this.$element.is(":disabled"),
                        readonly: this.$element.is("[readonly]"),
                        onColor: this.$element.data("on-color"),
                        offColor: this.$element.data("off-color"),
                        onText: this.$element.data("on-text"),
                        offText: this.$element.data("off-text"),
                        labelText: this.$element.data("label-text"),
                        baseClass: this.$element.data("base-class"),
                        wrapperClass: this.$element.data("wrapper-class")
                    });
                    this.$wrapper = $("<div>", {
                        "class": function(_this) {
                            return function() {
                                var classes;
                                classes = [ "" + _this.options.baseClass ].concat(_this._getClasses(_this.options.wrapperClass));
                                classes.push(_this.options.state ? "" + _this.options.baseClass + "-on" : "" + _this.options.baseClass + "-off");
                                if (_this.options.size != null) {
                                    classes.push("" + _this.options.baseClass + "-" + _this.options.size);
                                }
                                if (_this.options.animate) {
                                    classes.push("" + _this.options.baseClass + "-animate");
                                }
                                if (_this.options.disabled) {
                                    classes.push("" + _this.options.baseClass + "-disabled");
                                }
                                if (_this.options.readonly) {
                                    classes.push("" + _this.options.baseClass + "-readonly");
                                }
                                if (_this.$element.attr("id")) {
                                    classes.push("" + _this.options.baseClass + "-id-" + _this.$element.attr("id"));
                                }
                                return classes.join(" ");
                            };
                        }(this)()
                    });
                    this.$container = $("<div>", {
                        "class": "" + this.options.baseClass + "-container"
                    });
                    this.$on = $("<span>", {
                        html: this.options.onText,
                        "class": "" + this.options.baseClass + "-handle-on " + this.options.baseClass + "-" + this.options.onColor
                    });
                    this.$off = $("<span>", {
                        html: this.options.offText,
                        "class": "" + this.options.baseClass + "-handle-off " + this.options.baseClass + "-" + this.options.offColor
                    });
                    this.$label = $("<label>", {
                        "for": this.$element.attr("id"),
                        html: this.options.labelText,
                        "class": "" + this.options.baseClass + "-label"
                    });
                    this.$element.on("init.bootstrapSwitch", function(_this) {
                        return function() {
                            return _this.options.onInit.apply(element, arguments);
                        };
                    }(this));
                    this.$element.on("switchChange.bootstrapSwitch", function(_this) {
                        return function() {
                            return _this.options.onSwitchChange.apply(element, arguments);
                        };
                    }(this));
                    this.$container = this.$element.wrap(this.$container).parent();
                    this.$wrapper = this.$container.wrap(this.$wrapper).parent();
                    this.$element.before(this.$on).before(this.$label).before(this.$off).trigger("init.bootstrapSwitch");
                    this._elementHandlers();
                    this._handleHandlers();
                    this._labelHandlers();
                    this._formHandler();
                }
                BootstrapSwitch.prototype._constructor = BootstrapSwitch;
                BootstrapSwitch.prototype.state = function(value, skip) {
                    if (typeof value === "undefined") {
                        return this.options.state;
                    }
                    if (this.options.disabled || this.options.readonly) {
                        return this.$element;
                    }
                    value = !!value;
                    this.$element.prop("checked", value).trigger("change.bootstrapSwitch", skip);
                    return this.$element;
                };
                BootstrapSwitch.prototype.toggleState = function(skip) {
                    if (this.options.disabled || this.options.readonly) {
                        return this.$element;
                    }
                    return this.$element.prop("checked", !this.options.state).trigger("change.bootstrapSwitch", skip);
                };
                BootstrapSwitch.prototype.size = function(value) {
                    if (typeof value === "undefined") {
                        return this.options.size;
                    }
                    if (this.options.size != null) {
                        this.$wrapper.removeClass("" + this.options.baseClass + "-" + this.options.size);
                    }
                    if (value) {
                        this.$wrapper.addClass("" + this.options.baseClass + "-" + value);
                    }
                    this.options.size = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.animate = function(value) {
                    if (typeof value === "undefined") {
                        return this.options.animate;
                    }
                    value = !!value;
                    this.$wrapper[value ? "addClass" : "removeClass"]("" + this.options.baseClass + "-animate");
                    this.options.animate = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.disabled = function(value) {
                    if (typeof value === "undefined") {
                        return this.options.disabled;
                    }
                    value = !!value;
                    this.$wrapper[value ? "addClass" : "removeClass"]("" + this.options.baseClass + "-disabled");
                    this.$element.prop("disabled", value);
                    this.options.disabled = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.toggleDisabled = function() {
                    this.$element.prop("disabled", !this.options.disabled);
                    this.$wrapper.toggleClass("" + this.options.baseClass + "-disabled");
                    this.options.disabled = !this.options.disabled;
                    return this.$element;
                };
                BootstrapSwitch.prototype.readonly = function(value) {
                    if (typeof value === "undefined") {
                        return this.options.readonly;
                    }
                    value = !!value;
                    this.$wrapper[value ? "addClass" : "removeClass"]("" + this.options.baseClass + "-readonly");
                    this.$element.prop("readonly", value);
                    this.options.readonly = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.toggleReadonly = function() {
                    this.$element.prop("readonly", !this.options.readonly);
                    this.$wrapper.toggleClass("" + this.options.baseClass + "-readonly");
                    this.options.readonly = !this.options.readonly;
                    return this.$element;
                };
                BootstrapSwitch.prototype.onColor = function(value) {
                    var color;
                    color = this.options.onColor;
                    if (typeof value === "undefined") {
                        return color;
                    }
                    if (color != null) {
                        this.$on.removeClass("" + this.options.baseClass + "-" + color);
                    }
                    this.$on.addClass("" + this.options.baseClass + "-" + value);
                    this.options.onColor = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.offColor = function(value) {
                    var color;
                    color = this.options.offColor;
                    if (typeof value === "undefined") {
                        return color;
                    }
                    if (color != null) {
                        this.$off.removeClass("" + this.options.baseClass + "-" + color);
                    }
                    this.$off.addClass("" + this.options.baseClass + "-" + value);
                    this.options.offColor = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.onText = function(value) {
                    if (typeof value === "undefined") {
                        return this.options.onText;
                    }
                    this.$on.html(value);
                    this.options.onText = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.offText = function(value) {
                    if (typeof value === "undefined") {
                        return this.options.offText;
                    }
                    this.$off.html(value);
                    this.options.offText = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.labelText = function(value) {
                    if (typeof value === "undefined") {
                        return this.options.labelText;
                    }
                    this.$label.html(value);
                    this.options.labelText = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.baseClass = function(value) {
                    return this.options.baseClass;
                };
                BootstrapSwitch.prototype.wrapperClass = function(value) {
                    if (typeof value === "undefined") {
                        return this.options.wrapperClass;
                    }
                    if (!value) {
                        value = $.fn.bootstrapSwitch.defaults.wrapperClass;
                    }
                    this.$wrapper.removeClass(this._getClasses(this.options.wrapperClass).join(" "));
                    this.$wrapper.addClass(this._getClasses(value).join(" "));
                    this.options.wrapperClass = value;
                    return this.$element;
                };
                BootstrapSwitch.prototype.destroy = function() {
                    var $form;
                    $form = this.$element.closest("form");
                    if ($form.length) {
                        $form.off("reset.bootstrapSwitch").removeData("bootstrap-switch");
                    }
                    this.$container.children().not(this.$element).remove();
                    this.$element.unwrap().unwrap().off(".bootstrapSwitch").removeData("bootstrap-switch");
                    return this.$element;
                };
                BootstrapSwitch.prototype._elementHandlers = function() {
                    return this.$element.on({
                        "change.bootstrapSwitch": function(_this) {
                            return function(e, skip) {
                                var checked;
                                e.preventDefault();
                                e.stopPropagation();
                                e.stopImmediatePropagation();
                                checked = _this.$element.is(":checked");
                                if (checked === _this.options.state) {
                                    return;
                                }
                                _this.options.state = checked;
                                _this.$wrapper.removeClass(checked ? "" + _this.options.baseClass + "-off" : "" + _this.options.baseClass + "-on").addClass(checked ? "" + _this.options.baseClass + "-on" : "" + _this.options.baseClass + "-off");
                                if (!skip) {
                                    if (_this.$element.is(":radio")) {
                                        $("[name='" + _this.$element.attr("name") + "']").not(_this.$element).prop("checked", false).trigger("change.bootstrapSwitch", true);
                                    }
                                    return _this.$element.trigger("switchChange.bootstrapSwitch", [ checked ]);
                                }
                            };
                        }(this),
                        "focus.bootstrapSwitch": function(_this) {
                            return function(e) {
                                e.preventDefault();
                                e.stopPropagation();
                                e.stopImmediatePropagation();
                                return _this.$wrapper.addClass("" + _this.options.baseClass + "-focused");
                            };
                        }(this),
                        "blur.bootstrapSwitch": function(_this) {
                            return function(e) {
                                e.preventDefault();
                                e.stopPropagation();
                                e.stopImmediatePropagation();
                                return _this.$wrapper.removeClass("" + _this.options.baseClass + "-focused");
                            };
                        }(this),
                        "keydown.bootstrapSwitch": function(_this) {
                            return function(e) {
                                if (!e.which || _this.options.disabled || _this.options.readonly) {
                                    return;
                                }
                                switch (e.which) {
                                  case 32:
                                    e.preventDefault();
                                    e.stopPropagation();
                                    e.stopImmediatePropagation();
                                    return _this.toggleState();

                                  case 37:
                                    e.preventDefault();
                                    e.stopPropagation();
                                    e.stopImmediatePropagation();
                                    return _this.state(false);

                                  case 39:
                                    e.preventDefault();
                                    e.stopPropagation();
                                    e.stopImmediatePropagation();
                                    return _this.state(true);
                                }
                            };
                        }(this)
                    });
                };
                BootstrapSwitch.prototype._handleHandlers = function() {
                    this.$on.on("click.bootstrapSwitch", function(_this) {
                        return function(e) {
                            _this.state(false);
                            return _this.$element.trigger("focus.bootstrapSwitch");
                        };
                    }(this));
                    return this.$off.on("click.bootstrapSwitch", function(_this) {
                        return function(e) {
                            _this.state(true);
                            return _this.$element.trigger("focus.bootstrapSwitch");
                        };
                    }(this));
                };
                BootstrapSwitch.prototype._labelHandlers = function() {
                    return this.$label.on({
                        "mousemove.bootstrapSwitch touchmove.bootstrapSwitch": function(_this) {
                            return function(e) {
                                var left, percent, right;
                                if (!_this.drag) {
                                    return;
                                }
                                e.preventDefault();
                                percent = ((e.pageX || e.originalEvent.touches[0].pageX) - _this.$wrapper.offset().left) / _this.$wrapper.width() * 100;
                                left = 25;
                                right = 75;
                                if (percent < left) {
                                    percent = left;
                                } else if (percent > right) {
                                    percent = right;
                                }
                                _this.$container.css("margin-left", "" + (percent - right) + "%");
                                return _this.$element.trigger("focus.bootstrapSwitch");
                            };
                        }(this),
                        "mousedown.bootstrapSwitch touchstart.bootstrapSwitch": function(_this) {
                            return function(e) {
                                if (_this.drag || _this.options.disabled || _this.options.readonly) {
                                    return;
                                }
                                e.preventDefault();
                                _this.drag = true;
                                if (_this.options.animate) {
                                    _this.$wrapper.removeClass("" + _this.options.baseClass + "-animate");
                                }
                                return _this.$element.trigger("focus.bootstrapSwitch");
                            };
                        }(this),
                        "mouseup.bootstrapSwitch touchend.bootstrapSwitch": function(_this) {
                            return function(e) {
                                if (!_this.drag) {
                                    return;
                                }
                                e.preventDefault();
                                _this.drag = false;
                                _this.$element.prop("checked", parseInt(_this.$container.css("margin-left"), 10) > -(_this.$container.width() / 6)).trigger("change.bootstrapSwitch");
                                _this.$container.css("margin-left", "");
                                if (_this.options.animate) {
                                    return _this.$wrapper.addClass("" + _this.options.baseClass + "-animate");
                                }
                            };
                        }(this),
                        "mouseleave.bootstrapSwitch": function(_this) {
                            return function(e) {
                                return _this.$label.trigger("mouseup.bootstrapSwitch");
                            };
                        }(this)
                    });
                };
                BootstrapSwitch.prototype._formHandler = function() {
                    var $form;
                    $form = this.$element.closest("form");
                    if ($form.data("bootstrap-switch")) {
                        return;
                    }
                    return $form.on("reset.bootstrapSwitch", function() {
                        return window.setTimeout(function() {
                            return $form.find("input").filter(function() {
                                return $(this).data("bootstrap-switch");
                            }).each(function() {
                                return $(this).bootstrapSwitch("state", this.checked);
                            });
                        }, 1);
                    }).data("bootstrap-switch", true);
                };
                BootstrapSwitch.prototype._getClasses = function(classes) {
                    var c, cls, _i, _len;
                    if (!$.isArray(classes)) {
                        return [ "" + this.options.baseClass + "-" + classes ];
                    }
                    cls = [];
                    for (_i = 0, _len = classes.length; _i < _len; _i++) {
                        c = classes[_i];
                        cls.push("" + this.options.baseClass + "-" + c);
                    }
                    return cls;
                };
                return BootstrapSwitch;
            }();
            $.fn.bootstrapSwitch = function() {
                var args, option, ret;
                option = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
                ret = this;
                this.each(function() {
                    var $this, data;
                    $this = $(this);
                    data = $this.data("bootstrap-switch");
                    if (!data) {
                        $this.data("bootstrap-switch", data = new BootstrapSwitch(this, option));
                    }
                    if (typeof option === "string") {
                        return ret = data[option].apply(data, args);
                    }
                });
                return ret;
            };
            $.fn.bootstrapSwitch.Constructor = BootstrapSwitch;
            return $.fn.bootstrapSwitch.defaults = {
                state: true,
                size: null,
                animate: true,
                disabled: false,
                readonly: false,
                onColor: "primary",
                offColor: "default",
                onText: "ON",
                offText: "OFF",
                labelText: "&nbsp;",
                baseClass: "bootstrap-switch",
                wrapperClass: "wrapper",
                onInit: function() {},
                onSwitchChange: function() {}
            };
        })(window.jQuery, window);
    }).call(this);
});

define("torabot/main/0.1.0/xeditable-debug", [ "torabot/main/0.1.0/xeditable/xeditable-debug" ], function(require, exports, module) {
    require("torabot/main/0.1.0/xeditable/xeditable-debug");
    require("torabot/main/0.1.0/xeditable/xeditable-debug.css");
    $.fn.popup_text_edit = function(options) {
        $(this).editable($.extend({}, {
            type: "text",
            mode: "popup",
            url: function(params) {
                var d = $.Deferred();
                var $this = $(this);
                if ($this.data("args")) {
                    var data = $this.data("args");
                } else {
                    var data = {};
                }
                if ($this.data("field")) {
                    var field = $this.data("field");
                } else {
                    var field = "value";
                }
                data[field] = $.torabot.cast($this.data("kind"), params.value);
                $.ajax({
                    url: $this.data("uri"),
                    type: "post",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify(data)
                }).done(d.resolve).fail(d.reject);
                return d;
            },
            error: function(xhr) {
                new PNotify({
                    text: JSON.parse(xhr.responseText).message.html,
                    type: "error",
                    icon: false,
                    buttons: {
                        closer: true,
                        sticker: false
                    }
                });
            }
        }, options || {}));
    };
    $(".editable-field").popup_text_edit();
});

define("torabot/main/0.1.0/xeditable/xeditable-debug", [], function(require) {
    /*! X-editable - v1.5.1 
* In-place editing with Twitter Bootstrap, jQuery UI or pure jQuery
* http://github.com/vitalets/x-editable
* Copyright (c) 2013 Vitaliy Potapov; Licensed MIT */
    /**
Form with single input element, two buttons and two states: normal/loading.
Applied as jQuery method to DIV tag (not to form tag!). This is because form can be in loading state when spinner shown.
Editableform is linked with one of input types, e.g. 'text', 'select' etc.

@class editableform
@uses text
@uses textarea
**/
    (function($) {
        "use strict";
        var EditableForm = function(div, options) {
            this.options = $.extend({}, $.fn.editableform.defaults, options);
            this.$div = $(div);
            //div, containing form. Not form tag. Not editable-element.
            if (!this.options.scope) {
                this.options.scope = this;
            }
        };
        EditableForm.prototype = {
            constructor: EditableForm,
            initInput: function() {
                //called once
                //take input from options (as it is created in editable-element)
                this.input = this.options.input;
                //set initial value
                //todo: may be add check: typeof str === 'string' ? 
                this.value = this.input.str2value(this.options.value);
                //prerender: get input.$input
                this.input.prerender();
            },
            initTemplate: function() {
                this.$form = $($.fn.editableform.template);
            },
            initButtons: function() {
                var $btn = this.$form.find(".editable-buttons");
                $btn.append($.fn.editableform.buttons);
                if (this.options.showbuttons === "bottom") {
                    $btn.addClass("editable-buttons-bottom");
                }
            },
            /**
        Renders editableform

        @method render
        **/
            render: function() {
                //init loader
                this.$loading = $($.fn.editableform.loading);
                this.$div.empty().append(this.$loading);
                //init form template and buttons
                this.initTemplate();
                if (this.options.showbuttons) {
                    this.initButtons();
                } else {
                    this.$form.find(".editable-buttons").remove();
                }
                //show loading state
                this.showLoading();
                //flag showing is form now saving value to server. 
                //It is needed to wait when closing form.
                this.isSaving = false;
                /**        
            Fired when rendering starts
            @event rendering 
            @param {Object} event event object
            **/
                this.$div.triggerHandler("rendering");
                //init input
                this.initInput();
                //append input to form
                this.$form.find("div.editable-input").append(this.input.$tpl);
                //append form to container
                this.$div.append(this.$form);
                //render input
                $.when(this.input.render()).then($.proxy(function() {
                    //setup input to submit automatically when no buttons shown
                    if (!this.options.showbuttons) {
                        this.input.autosubmit();
                    }
                    //attach 'cancel' handler
                    this.$form.find(".editable-cancel").click($.proxy(this.cancel, this));
                    if (this.input.error) {
                        this.error(this.input.error);
                        this.$form.find(".editable-submit").attr("disabled", true);
                        this.input.$input.attr("disabled", true);
                        //prevent form from submitting
                        this.$form.submit(function(e) {
                            e.preventDefault();
                        });
                    } else {
                        this.error(false);
                        this.input.$input.removeAttr("disabled");
                        this.$form.find(".editable-submit").removeAttr("disabled");
                        var value = this.value === null || this.value === undefined || this.value === "" ? this.options.defaultValue : this.value;
                        this.input.value2input(value);
                        //attach submit handler
                        this.$form.submit($.proxy(this.submit, this));
                    }
                    /**        
                Fired when form is rendered
                @event rendered
                @param {Object} event event object
                **/
                    this.$div.triggerHandler("rendered");
                    this.showForm();
                    //call postrender method to perform actions required visibility of form
                    if (this.input.postrender) {
                        this.input.postrender();
                    }
                }, this));
            },
            cancel: function() {
                /**        
            Fired when form was cancelled by user
            @event cancel 
            @param {Object} event event object
            **/
                this.$div.triggerHandler("cancel");
            },
            showLoading: function() {
                var w, h;
                if (this.$form) {
                    //set loading size equal to form
                    w = this.$form.outerWidth();
                    h = this.$form.outerHeight();
                    if (w) {
                        this.$loading.width(w);
                    }
                    if (h) {
                        this.$loading.height(h);
                    }
                    this.$form.hide();
                } else {
                    //stretch loading to fill container width
                    w = this.$loading.parent().width();
                    if (w) {
                        this.$loading.width(w);
                    }
                }
                this.$loading.show();
            },
            showForm: function(activate) {
                this.$loading.hide();
                this.$form.show();
                if (activate !== false) {
                    this.input.activate();
                }
                /**        
            Fired when form is shown
            @event show 
            @param {Object} event event object
            **/
                this.$div.triggerHandler("show");
            },
            error: function(msg) {
                var $group = this.$form.find(".control-group"), $block = this.$form.find(".editable-error-block"), lines;
                if (msg === false) {
                    $group.removeClass($.fn.editableform.errorGroupClass);
                    $block.removeClass($.fn.editableform.errorBlockClass).empty().hide();
                } else {
                    //convert newline to <br> for more pretty error display
                    if (msg) {
                        lines = ("" + msg).split("\n");
                        for (var i = 0; i < lines.length; i++) {
                            lines[i] = $("<div>").text(lines[i]).html();
                        }
                        msg = lines.join("<br>");
                    }
                    $group.addClass($.fn.editableform.errorGroupClass);
                    $block.addClass($.fn.editableform.errorBlockClass).html(msg).show();
                }
            },
            submit: function(e) {
                e.stopPropagation();
                e.preventDefault();
                //get new value from input
                var newValue = this.input.input2value();
                //validation: if validate returns string or truthy value - means error
                //if returns object like {newValue: '...'} => submitted value is reassigned to it
                var error = this.validate(newValue);
                if ($.type(error) === "object" && error.newValue !== undefined) {
                    newValue = error.newValue;
                    this.input.value2input(newValue);
                    if (typeof error.msg === "string") {
                        this.error(error.msg);
                        this.showForm();
                        return;
                    }
                } else if (error) {
                    this.error(error);
                    this.showForm();
                    return;
                }
                //if value not changed --> trigger 'nochange' event and return
                /*jslint eqeq: true*/
                if (!this.options.savenochange && this.input.value2str(newValue) == this.input.value2str(this.value)) {
                    /*jslint eqeq: false*/
                    /**        
                Fired when value not changed but form is submitted. Requires savenochange = false.
                @event nochange 
                @param {Object} event event object
                **/
                    this.$div.triggerHandler("nochange");
                    return;
                }
                //convert value for submitting to server
                var submitValue = this.input.value2submit(newValue);
                this.isSaving = true;
                //sending data to server
                $.when(this.save(submitValue)).done($.proxy(function(response) {
                    this.isSaving = false;
                    //run success callback
                    var res = typeof this.options.success === "function" ? this.options.success.call(this.options.scope, response, newValue) : null;
                    //if success callback returns false --> keep form open and do not activate input
                    if (res === false) {
                        this.error(false);
                        this.showForm(false);
                        return;
                    }
                    //if success callback returns string -->  keep form open, show error and activate input               
                    if (typeof res === "string") {
                        this.error(res);
                        this.showForm();
                        return;
                    }
                    //if success callback returns object like {newValue: <something>} --> use that value instead of submitted
                    //it is usefull if you want to chnage value in url-function
                    if (res && typeof res === "object" && res.hasOwnProperty("newValue")) {
                        newValue = res.newValue;
                    }
                    //clear error message
                    this.error(false);
                    this.value = newValue;
                    /**        
                Fired when form is submitted
                @event save 
                @param {Object} event event object
                @param {Object} params additional params
                @param {mixed} params.newValue raw new value
                @param {mixed} params.submitValue submitted value as string
                @param {Object} params.response ajax response

                @example
                $('#form-div').on('save'), function(e, params){
                    if(params.newValue === 'username') {...}
                });
                **/
                    this.$div.triggerHandler("save", {
                        newValue: newValue,
                        submitValue: submitValue,
                        response: response
                    });
                }, this)).fail($.proxy(function(xhr) {
                    this.isSaving = false;
                    var msg;
                    if (typeof this.options.error === "function") {
                        msg = this.options.error.call(this.options.scope, xhr, newValue);
                    } else {
                        msg = typeof xhr === "string" ? xhr : xhr.responseText || xhr.statusText || "Unknown error!";
                    }
                    this.error(msg);
                    this.showForm();
                }, this));
            },
            save: function(submitValue) {
                //try parse composite pk defined as json string in data-pk 
                this.options.pk = $.fn.editableutils.tryParseJson(this.options.pk, true);
                var pk = typeof this.options.pk === "function" ? this.options.pk.call(this.options.scope) : this.options.pk, /*
              send on server in following cases:
              1. url is function
              2. url is string AND (pk defined OR send option = always) 
            */
                send = !!(typeof this.options.url === "function" || this.options.url && (this.options.send === "always" || this.options.send === "auto" && pk !== null && pk !== undefined)), params;
                if (send) {
                    //send to server
                    this.showLoading();
                    //standard params
                    params = {
                        name: this.options.name || "",
                        value: submitValue,
                        pk: pk
                    };
                    //additional params
                    if (typeof this.options.params === "function") {
                        params = this.options.params.call(this.options.scope, params);
                    } else {
                        //try parse json in single quotes (from data-params attribute)
                        this.options.params = $.fn.editableutils.tryParseJson(this.options.params, true);
                        $.extend(params, this.options.params);
                    }
                    if (typeof this.options.url === "function") {
                        //user's function
                        return this.options.url.call(this.options.scope, params);
                    } else {
                        //send ajax to server and return deferred object
                        return $.ajax($.extend({
                            url: this.options.url,
                            data: params,
                            type: "POST"
                        }, this.options.ajaxOptions));
                    }
                }
            },
            validate: function(value) {
                if (value === undefined) {
                    value = this.value;
                }
                if (typeof this.options.validate === "function") {
                    return this.options.validate.call(this.options.scope, value);
                }
            },
            option: function(key, value) {
                if (key in this.options) {
                    this.options[key] = value;
                }
                if (key === "value") {
                    this.setValue(value);
                }
            },
            setValue: function(value, convertStr) {
                if (convertStr) {
                    this.value = this.input.str2value(value);
                } else {
                    this.value = value;
                }
                //if form is visible, update input
                if (this.$form && this.$form.is(":visible")) {
                    this.input.value2input(this.value);
                }
            }
        };
        /*
    Initialize editableform. Applied to jQuery object.

    @method $().editableform(options)
    @params {Object} options
    @example
    var $form = $('&lt;div&gt;').editableform({
        type: 'text',
        name: 'username',
        url: '/post',
        value: 'vitaliy'
    });

    //to display form you should call 'render' method
    $form.editableform('render');     
    */
        $.fn.editableform = function(option) {
            var args = arguments;
            return this.each(function() {
                var $this = $(this), data = $this.data("editableform"), options = typeof option === "object" && option;
                if (!data) {
                    $this.data("editableform", data = new EditableForm(this, options));
                }
                if (typeof option === "string") {
                    //call method 
                    data[option].apply(data, Array.prototype.slice.call(args, 1));
                }
            });
        };
        //keep link to constructor to allow inheritance
        $.fn.editableform.Constructor = EditableForm;
        //defaults
        $.fn.editableform.defaults = {
            /* see also defaults for input */
            /**
        Type of input. Can be <code>text|textarea|select|date|checklist</code>

        @property type 
        @type string
        @default 'text'
        **/
            type: "text",
            /**
        Url for submit, e.g. <code>'/post'</code>  
        If function - it will be called instead of ajax. Function should return deferred object to run fail/done callbacks.

        @property url 
        @type string|function
        @default null
        @example
        url: function(params) {
            var d = new $.Deferred;
            if(params.value === 'abc') {
                return d.reject('error message'); //returning error via deferred object
            } else {
                //async saving data in js model
                someModel.asyncSaveMethod({
                   ..., 
                   success: function(){
                      d.resolve();
                   }
                }); 
                return d.promise();
            }
        } 
        **/
            url: null,
            /**
        Additional params for submit. If defined as <code>object</code> - it is **appended** to original ajax data (pk, name and value).  
        If defined as <code>function</code> - returned object **overwrites** original ajax data.
        @example
        params: function(params) {
            //originally params contain pk, name and value
            params.a = 1;
            return params;
        }

        @property params 
        @type object|function
        @default null
        **/
            params: null,
            /**
        Name of field. Will be submitted on server. Can be taken from <code>id</code> attribute

        @property name 
        @type string
        @default null
        **/
            name: null,
            /**
        Primary key of editable object (e.g. record id in database). For composite keys use object, e.g. <code>{id: 1, lang: 'en'}</code>.
        Can be calculated dynamically via function.

        @property pk 
        @type string|object|function
        @default null
        **/
            pk: null,
            /**
        Initial value. If not defined - will be taken from element's content.
        For __select__ type should be defined (as it is ID of shown text).

        @property value 
        @type string|object
        @default null
        **/
            value: null,
            /**
        Value that will be displayed in input if original field value is empty (`null|undefined|''`).

        @property defaultValue 
        @type string|object
        @default null
        @since 1.4.6
        **/
            defaultValue: null,
            /**
        Strategy for sending data on server. Can be `auto|always|never`.
        When 'auto' data will be sent on server **only if pk and url defined**, otherwise new value will be stored locally.

        @property send 
        @type string
        @default 'auto'
        **/
            send: "auto",
            /**
        Function for client-side validation. If returns string - means validation not passed and string showed as error.
        Since 1.5.1 you can modify submitted value by returning object from `validate`: 
        `{newValue: '...'}` or `{newValue: '...', msg: '...'}`

        @property validate 
        @type function
        @default null
        @example
        validate: function(value) {
            if($.trim(value) == '') {
                return 'This field is required';
            }
        }
        **/
            validate: null,
            /**
        Success callback. Called when value successfully sent on server and **response status = 200**.  
        Usefull to work with json response. For example, if your backend response can be <code>{success: true}</code>
        or <code>{success: false, msg: "server error"}</code> you can check it inside this callback.  
        If it returns **string** - means error occured and string is shown as error message.  
        If it returns **object like** <code>{newValue: &lt;something&gt;}</code> - it overwrites value, submitted by user.  
        Otherwise newValue simply rendered into element.
        
        @property success 
        @type function
        @default null
        @example
        success: function(response, newValue) {
            if(!response.success) return response.msg;
        }
        **/
            success: null,
            /**
        Error callback. Called when request failed (response status != 200).  
        Usefull when you want to parse error response and display a custom message.
        Must return **string** - the message to be displayed in the error block.
                
        @property error 
        @type function
        @default null
        @since 1.4.4
        @example
        error: function(response, newValue) {
            if(response.status === 500) {
                return 'Service unavailable. Please try later.';
            } else {
                return response.responseText;
            }
        }
        **/
            error: null,
            /**
        Additional options for submit ajax request.
        List of values: http://api.jquery.com/jQuery.ajax
        
        @property ajaxOptions 
        @type object
        @default null
        @since 1.1.1        
        @example 
        ajaxOptions: {
            type: 'put',
            dataType: 'json'
        }        
        **/
            ajaxOptions: null,
            /**
        Where to show buttons: left(true)|bottom|false  
        Form without buttons is auto-submitted.

        @property showbuttons 
        @type boolean|string
        @default true
        @since 1.1.1
        **/
            showbuttons: true,
            /**
        Scope for callback methods (success, validate).  
        If <code>null</code> means editableform instance itself. 

        @property scope 
        @type DOMElement|object
        @default null
        @since 1.2.0
        @private
        **/
            scope: null,
            /**
        Whether to save or cancel value when it was not changed but form was submitted

        @property savenochange 
        @type boolean
        @default false
        @since 1.2.0
        **/
            savenochange: false
        };
        /*
    Note: following params could redefined in engine: bootstrap or jqueryui:
    Classes 'control-group' and 'editable-error-block' must always present!
    */
        $.fn.editableform.template = '<form class="form-inline editableform">' + '<div class="control-group">' + '<div><div class="editable-input"></div><div class="editable-buttons"></div></div>' + '<div class="editable-error-block"></div>' + "</div>" + "</form>";
        //loading div
        $.fn.editableform.loading = '<div class="editableform-loading"></div>';
        //buttons
        $.fn.editableform.buttons = '<button type="submit" class="editable-submit">ok</button>' + '<button type="button" class="editable-cancel">cancel</button>';
        //error class attached to control-group
        $.fn.editableform.errorGroupClass = null;
        //error class attached to editable-error-block
        $.fn.editableform.errorBlockClass = "editable-error";
        //engine
        $.fn.editableform.engine = "jquery";
    })(window.jQuery);
    /**
* EditableForm utilites
*/
    (function($) {
        "use strict";
        //utils
        $.fn.editableutils = {
            /**
        * classic JS inheritance function
        */
            inherit: function(Child, Parent) {
                var F = function() {};
                F.prototype = Parent.prototype;
                Child.prototype = new F();
                Child.prototype.constructor = Child;
                Child.superclass = Parent.prototype;
            },
            /**
        * set caret position in input
        * see http://stackoverflow.com/questions/499126/jquery-set-cursor-position-in-text-area
        */
            setCursorPosition: function(elem, pos) {
                if (elem.setSelectionRange) {
                    elem.setSelectionRange(pos, pos);
                } else if (elem.createTextRange) {
                    var range = elem.createTextRange();
                    range.collapse(true);
                    range.moveEnd("character", pos);
                    range.moveStart("character", pos);
                    range.select();
                }
            },
            /**
        * function to parse JSON in *single* quotes. (jquery automatically parse only double quotes)
        * That allows such code as: <a data-source="{'a': 'b', 'c': 'd'}">
        * safe = true --> means no exception will be thrown
        * for details see http://stackoverflow.com/questions/7410348/how-to-set-json-format-to-html5-data-attributes-in-the-jquery
        */
            tryParseJson: function(s, safe) {
                if (typeof s === "string" && s.length && s.match(/^[\{\[].*[\}\]]$/)) {
                    if (safe) {
                        try {
                            /*jslint evil: true*/
                            s = new Function("return " + s)();
                        } catch (e) {} finally {
                            return s;
                        }
                    } else {
                        /*jslint evil: true*/
                        s = new Function("return " + s)();
                    }
                }
                return s;
            },
            /**
        * slice object by specified keys
        */
            sliceObj: function(obj, keys, caseSensitive) {
                var key, keyLower, newObj = {};
                if (!$.isArray(keys) || !keys.length) {
                    return newObj;
                }
                for (var i = 0; i < keys.length; i++) {
                    key = keys[i];
                    if (obj.hasOwnProperty(key)) {
                        newObj[key] = obj[key];
                    }
                    if (caseSensitive === true) {
                        continue;
                    }
                    //when getting data-* attributes via $.data() it's converted to lowercase.
                    //details: http://stackoverflow.com/questions/7602565/using-data-attributes-with-jquery
                    //workaround is code below.
                    keyLower = key.toLowerCase();
                    if (obj.hasOwnProperty(keyLower)) {
                        newObj[key] = obj[keyLower];
                    }
                }
                return newObj;
            },
            /*
        exclude complex objects from $.data() before pass to config
        */
            getConfigData: function($element) {
                var data = {};
                $.each($element.data(), function(k, v) {
                    if (typeof v !== "object" || v && typeof v === "object" && (v.constructor === Object || v.constructor === Array)) {
                        data[k] = v;
                    }
                });
                return data;
            },
            /*
         returns keys of object
        */
            objectKeys: function(o) {
                if (Object.keys) {
                    return Object.keys(o);
                } else {
                    if (o !== Object(o)) {
                        throw new TypeError("Object.keys called on a non-object");
                    }
                    var k = [], p;
                    for (p in o) {
                        if (Object.prototype.hasOwnProperty.call(o, p)) {
                            k.push(p);
                        }
                    }
                    return k;
                }
            },
            /**
        method to escape html.
       **/
            escape: function(str) {
                return $("<div>").text(str).html();
            },
            /*
        returns array items from sourceData having value property equal or inArray of 'value'
       */
            itemsByValue: function(value, sourceData, valueProp) {
                if (!sourceData || value === null) {
                    return [];
                }
                if (typeof valueProp !== "function") {
                    var idKey = valueProp || "value";
                    valueProp = function(e) {
                        return e[idKey];
                    };
                }
                var isValArray = $.isArray(value), result = [], that = this;
                $.each(sourceData, function(i, o) {
                    if (o.children) {
                        result = result.concat(that.itemsByValue(value, o.children, valueProp));
                    } else {
                        /*jslint eqeq: true*/
                        if (isValArray) {
                            if ($.grep(value, function(v) {
                                return v == (o && typeof o === "object" ? valueProp(o) : o);
                            }).length) {
                                result.push(o);
                            }
                        } else {
                            var itemValue = o && typeof o === "object" ? valueProp(o) : o;
                            if (value == itemValue) {
                                result.push(o);
                            }
                        }
                    }
                });
                return result;
            },
            /*
       Returns input by options: type, mode. 
       */
            createInput: function(options) {
                var TypeConstructor, typeOptions, input, type = options.type;
                //`date` is some kind of virtual type that is transformed to one of exact types
                //depending on mode and core lib
                if (type === "date") {
                    //inline
                    if (options.mode === "inline") {
                        if ($.fn.editabletypes.datefield) {
                            type = "datefield";
                        } else if ($.fn.editabletypes.dateuifield) {
                            type = "dateuifield";
                        }
                    } else {
                        if ($.fn.editabletypes.date) {
                            type = "date";
                        } else if ($.fn.editabletypes.dateui) {
                            type = "dateui";
                        }
                    }
                    //if type still `date` and not exist in types, replace with `combodate` that is base input
                    if (type === "date" && !$.fn.editabletypes.date) {
                        type = "combodate";
                    }
                }
                //`datetime` should be datetimefield in 'inline' mode
                if (type === "datetime" && options.mode === "inline") {
                    type = "datetimefield";
                }
                //change wysihtml5 to textarea for jquery UI and plain versions
                if (type === "wysihtml5" && !$.fn.editabletypes[type]) {
                    type = "textarea";
                }
                //create input of specified type. Input will be used for converting value, not in form
                if (typeof $.fn.editabletypes[type] === "function") {
                    TypeConstructor = $.fn.editabletypes[type];
                    typeOptions = this.sliceObj(options, this.objectKeys(TypeConstructor.defaults));
                    input = new TypeConstructor(typeOptions);
                    return input;
                } else {
                    $.error("Unknown type: " + type);
                    return false;
                }
            },
            //see http://stackoverflow.com/questions/7264899/detect-css-transitions-using-javascript-and-without-modernizr
            supportsTransitions: function() {
                var b = document.body || document.documentElement, s = b.style, p = "transition", v = [ "Moz", "Webkit", "Khtml", "O", "ms" ];
                if (typeof s[p] === "string") {
                    return true;
                }
                // Tests for vendor specific prop
                p = p.charAt(0).toUpperCase() + p.substr(1);
                for (var i = 0; i < v.length; i++) {
                    if (typeof s[v[i] + p] === "string") {
                        return true;
                    }
                }
                return false;
            }
        };
    })(window.jQuery);
    /**
Attaches stand-alone container with editable-form to HTML element. Element is used only for positioning, value is not stored anywhere.<br>
This method applied internally in <code>$().editable()</code>. You should subscribe on it's events (save / cancel) to get profit of it.<br>
Final realization can be different: bootstrap-popover, jqueryui-tooltip, poshytip, inline-div. It depends on which js file you include.<br>
Applied as jQuery method.

@class editableContainer
@uses editableform
**/
    (function($) {
        "use strict";
        var Popup = function(element, options) {
            this.init(element, options);
        };
        var Inline = function(element, options) {
            this.init(element, options);
        };
        //methods
        Popup.prototype = {
            containerName: null,
            //method to call container on element
            containerDataName: null,
            //object name in element's .data()
            innerCss: null,
            //tbd in child class
            containerClass: "editable-container editable-popup",
            //css class applied to container element
            defaults: {},
            //container itself defaults
            init: function(element, options) {
                this.$element = $(element);
                //since 1.4.1 container do not use data-* directly as they already merged into options.
                this.options = $.extend({}, $.fn.editableContainer.defaults, options);
                this.splitOptions();
                //set scope of form callbacks to element
                this.formOptions.scope = this.$element[0];
                this.initContainer();
                //flag to hide container, when saving value will finish
                this.delayedHide = false;
                //bind 'destroyed' listener to destroy container when element is removed from dom
                this.$element.on("destroyed", $.proxy(function() {
                    this.destroy();
                }, this));
                //attach document handler to close containers on click / escape
                if (!$(document).data("editable-handlers-attached")) {
                    //close all on escape
                    $(document).on("keyup.editable", function(e) {
                        if (e.which === 27) {
                            $(".editable-open").editableContainer("hide");
                        }
                    });
                    //close containers when click outside 
                    //(mousedown could be better than click, it closes everything also on drag drop)
                    $(document).on("click.editable", function(e) {
                        var $target = $(e.target), i, exclude_classes = [ ".editable-container", ".ui-datepicker-header", ".datepicker", //in inline mode datepicker is rendered into body
                        ".modal-backdrop", ".bootstrap-wysihtml5-insert-image-modal", ".bootstrap-wysihtml5-insert-link-modal" ];
                        //check if element is detached. It occurs when clicking in bootstrap datepicker
                        if (!$.contains(document.documentElement, e.target)) {
                            return;
                        }
                        //for some reason FF 20 generates extra event (click) in select2 widget with e.target = document
                        //we need to filter it via construction below. See https://github.com/vitalets/x-editable/issues/199
                        //Possibly related to http://stackoverflow.com/questions/10119793/why-does-firefox-react-differently-from-webkit-and-ie-to-click-event-on-selec
                        if ($target.is(document)) {
                            return;
                        }
                        //if click inside one of exclude classes --> no nothing
                        for (i = 0; i < exclude_classes.length; i++) {
                            if ($target.is(exclude_classes[i]) || $target.parents(exclude_classes[i]).length) {
                                return;
                            }
                        }
                        //close all open containers (except one - target)
                        Popup.prototype.closeOthers(e.target);
                    });
                    $(document).data("editable-handlers-attached", true);
                }
            },
            //split options on containerOptions and formOptions
            splitOptions: function() {
                this.containerOptions = {};
                this.formOptions = {};
                if (!$.fn[this.containerName]) {
                    throw new Error(this.containerName + " not found. Have you included corresponding js file?");
                }
                //keys defined in container defaults go to container, others go to form
                for (var k in this.options) {
                    if (k in this.defaults) {
                        this.containerOptions[k] = this.options[k];
                    } else {
                        this.formOptions[k] = this.options[k];
                    }
                }
            },
            /*
        Returns jquery object of container
        @method tip()
        */
            tip: function() {
                return this.container() ? this.container().$tip : null;
            },
            /* returns container object */
            container: function() {
                var container;
                //first, try get it by `containerDataName`
                if (this.containerDataName) {
                    if (container = this.$element.data(this.containerDataName)) {
                        return container;
                    }
                }
                //second, try `containerName`
                container = this.$element.data(this.containerName);
                return container;
            },
            /* call native method of underlying container, e.g. this.$element.popover('method') */
            call: function() {
                this.$element[this.containerName].apply(this.$element, arguments);
            },
            initContainer: function() {
                this.call(this.containerOptions);
            },
            renderForm: function() {
                this.$form.editableform(this.formOptions).on({
                    save: $.proxy(this.save, this),
                    //click on submit button (value changed)
                    nochange: $.proxy(function() {
                        this.hide("nochange");
                    }, this),
                    //click on submit button (value NOT changed)                
                    cancel: $.proxy(function() {
                        this.hide("cancel");
                    }, this),
                    //click on calcel button
                    show: $.proxy(function() {
                        if (this.delayedHide) {
                            this.hide(this.delayedHide.reason);
                            this.delayedHide = false;
                        } else {
                            this.setPosition();
                        }
                    }, this),
                    //re-position container every time form is shown (occurs each time after loading state)
                    rendering: $.proxy(this.setPosition, this),
                    //this allows to place container correctly when loading shown
                    resize: $.proxy(this.setPosition, this),
                    //this allows to re-position container when form size is changed 
                    rendered: $.proxy(function() {
                        /**        
                    Fired when container is shown and form is rendered (for select will wait for loading dropdown options).  
                    **Note:** Bootstrap popover has own `shown` event that now cannot be separated from x-editable's one.
                    The workaround is to check `arguments.length` that is always `2` for x-editable.                     
                    
                    @event shown 
                    @param {Object} event event object
                    @example
                    $('#username').on('shown', function(e, editable) {
                        editable.input.$input.val('overwriting value of input..');
                    });                     
                    **/
                        /*
                     TODO: added second param mainly to distinguish from bootstrap's shown event. It's a hotfix that will be solved in future versions via namespaced events.  
                    */
                        this.$element.triggerHandler("shown", $(this.options.scope).data("editable"));
                    }, this)
                }).editableform("render");
            },
            /**
        Shows container with form
        @method show()
        @param {boolean} closeAll Whether to close all other editable containers when showing this one. Default true.
        **/
            /* Note: poshytip owerwrites this method totally! */
            show: function(closeAll) {
                this.$element.addClass("editable-open");
                if (closeAll !== false) {
                    //close all open containers (except this)
                    this.closeOthers(this.$element[0]);
                }
                //show container itself
                this.innerShow();
                this.tip().addClass(this.containerClass);
                /*
            Currently, form is re-rendered on every show. 
            The main reason is that we dont know, what will container do with content when closed:
            remove(), detach() or just hide() - it depends on container.
            
            Detaching form itself before hide and re-insert before show is good solution, 
            but visually it looks ugly --> container changes size before hide.  
            */
                //if form already exist - delete previous data 
                if (this.$form) {}
                this.$form = $("<div>");
                //insert form into container body
                if (this.tip().is(this.innerCss)) {
                    //for inline container
                    this.tip().append(this.$form);
                } else {
                    this.tip().find(this.innerCss).append(this.$form);
                }
                //render form
                this.renderForm();
            },
            /**
        Hides container with form
        @method hide()
        @param {string} reason Reason caused hiding. Can be <code>save|cancel|onblur|nochange|undefined (=manual)</code>
        **/
            hide: function(reason) {
                if (!this.tip() || !this.tip().is(":visible") || !this.$element.hasClass("editable-open")) {
                    return;
                }
                //if form is saving value, schedule hide
                if (this.$form.data("editableform").isSaving) {
                    this.delayedHide = {
                        reason: reason
                    };
                    return;
                } else {
                    this.delayedHide = false;
                }
                this.$element.removeClass("editable-open");
                this.innerHide();
                /**
            Fired when container was hidden. It occurs on both save or cancel.  
            **Note:** Bootstrap popover has own `hidden` event that now cannot be separated from x-editable's one.
            The workaround is to check `arguments.length` that is always `2` for x-editable. 

            @event hidden 
            @param {object} event event object
            @param {string} reason Reason caused hiding. Can be <code>save|cancel|onblur|nochange|manual</code>
            @example
            $('#username').on('hidden', function(e, reason) {
                if(reason === 'save' || reason === 'cancel') {
                    //auto-open next editable
                    $(this).closest('tr').next().find('.editable').editable('show');
                } 
            });
            **/
                this.$element.triggerHandler("hidden", reason || "manual");
            },
            /* internal show method. To be overwritten in child classes */
            innerShow: function() {},
            /* internal hide method. To be overwritten in child classes */
            innerHide: function() {},
            /**
        Toggles container visibility (show / hide)
        @method toggle()
        @param {boolean} closeAll Whether to close all other editable containers when showing this one. Default true.
        **/
            toggle: function(closeAll) {
                if (this.container() && this.tip() && this.tip().is(":visible")) {
                    this.hide();
                } else {
                    this.show(closeAll);
                }
            },
            /*
        Updates the position of container when content changed.
        @method setPosition()
        */
            setPosition: function() {},
            save: function(e, params) {
                /**        
            Fired when new value was submitted. You can use <code>$(this).data('editableContainer')</code> inside handler to access to editableContainer instance
            
            @event save 
            @param {Object} event event object
            @param {Object} params additional params
            @param {mixed} params.newValue submitted value
            @param {Object} params.response ajax response
            @example
            $('#username').on('save', function(e, params) {
                //assuming server response: '{success: true}'
                var pk = $(this).data('editableContainer').options.pk;
                if(params.response && params.response.success) {
                    alert('value: ' + params.newValue + ' with pk: ' + pk + ' saved!');
                } else {
                    alert('error!'); 
                } 
            });
            **/
                this.$element.triggerHandler("save", params);
                //hide must be after trigger, as saving value may require methods of plugin, applied to input
                this.hide("save");
            },
            /**
        Sets new option
        
        @method option(key, value)
        @param {string} key 
        @param {mixed} value 
        **/
            option: function(key, value) {
                this.options[key] = value;
                if (key in this.containerOptions) {
                    this.containerOptions[key] = value;
                    this.setContainerOption(key, value);
                } else {
                    this.formOptions[key] = value;
                    if (this.$form) {
                        this.$form.editableform("option", key, value);
                    }
                }
            },
            setContainerOption: function(key, value) {
                this.call("option", key, value);
            },
            /**
        Destroys the container instance
        @method destroy()
        **/
            destroy: function() {
                this.hide();
                this.innerDestroy();
                this.$element.off("destroyed");
                this.$element.removeData("editableContainer");
            },
            /* to be overwritten in child classes */
            innerDestroy: function() {},
            /*
        Closes other containers except one related to passed element. 
        Other containers can be cancelled or submitted (depends on onblur option)
        */
            closeOthers: function(element) {
                $(".editable-open").each(function(i, el) {
                    //do nothing with passed element and it's children
                    if (el === element || $(el).find(element).length) {
                        return;
                    }
                    //otherwise cancel or submit all open containers 
                    var $el = $(el), ec = $el.data("editableContainer");
                    if (!ec) {
                        return;
                    }
                    if (ec.options.onblur === "cancel") {
                        $el.data("editableContainer").hide("onblur");
                    } else if (ec.options.onblur === "submit") {
                        $el.data("editableContainer").tip().find("form").submit();
                    }
                });
            },
            /**
        Activates input of visible container (e.g. set focus)
        @method activate()
        **/
            activate: function() {
                if (this.tip && this.tip().is(":visible") && this.$form) {
                    this.$form.data("editableform").input.activate();
                }
            }
        };
        /**
    jQuery method to initialize editableContainer.
    
    @method $().editableContainer(options)
    @params {Object} options
    @example
    $('#edit').editableContainer({
        type: 'text',
        url: '/post',
        pk: 1,
        value: 'hello'
    });
    **/
        $.fn.editableContainer = function(option) {
            var args = arguments;
            return this.each(function() {
                var $this = $(this), dataKey = "editableContainer", data = $this.data(dataKey), options = typeof option === "object" && option, Constructor = options.mode === "inline" ? Inline : Popup;
                if (!data) {
                    $this.data(dataKey, data = new Constructor(this, options));
                }
                if (typeof option === "string") {
                    //call method 
                    data[option].apply(data, Array.prototype.slice.call(args, 1));
                }
            });
        };
        //store constructors
        $.fn.editableContainer.Popup = Popup;
        $.fn.editableContainer.Inline = Inline;
        //defaults
        $.fn.editableContainer.defaults = {
            /**
        Initial value of form input

        @property value 
        @type mixed
        @default null
        @private
        **/
            value: null,
            /**
        Placement of container relative to element. Can be <code>top|right|bottom|left</code>. Not used for inline container.

        @property placement 
        @type string
        @default 'top'
        **/
            placement: "top",
            /**
        Whether to hide container on save/cancel.

        @property autohide 
        @type boolean
        @default true
        @private 
        **/
            autohide: true,
            /**
        Action when user clicks outside the container. Can be <code>cancel|submit|ignore</code>.  
        Setting <code>ignore</code> allows to have several containers open. 

        @property onblur 
        @type string
        @default 'cancel'
        @since 1.1.1
        **/
            onblur: "cancel",
            /**
        Animation speed (inline mode only)
        @property anim 
        @type string
        @default false
        **/
            anim: false,
            /**
        Mode of editable, can be `popup` or `inline` 
        
        @property mode 
        @type string         
        @default 'popup'
        @since 1.4.0        
        **/
            mode: "popup"
        };
        /* 
    * workaround to have 'destroyed' event to destroy popover when element is destroyed
    * see http://stackoverflow.com/questions/2200494/jquery-trigger-event-when-an-element-is-removed-from-the-dom
    */
        jQuery.event.special.destroyed = {
            remove: function(o) {
                if (o.handler) {
                    o.handler();
                }
            }
        };
    })(window.jQuery);
    /**
* Editable Inline 
* ---------------------
*/
    (function($) {
        "use strict";
        //copy prototype from EditableContainer
        //extend methods
        $.extend($.fn.editableContainer.Inline.prototype, $.fn.editableContainer.Popup.prototype, {
            containerName: "editableform",
            innerCss: ".editable-inline",
            containerClass: "editable-container editable-inline",
            //css class applied to container element
            initContainer: function() {
                //container is <span> element
                this.$tip = $("<span></span>");
                //convert anim to miliseconds (int)
                if (!this.options.anim) {
                    this.options.anim = 0;
                }
            },
            splitOptions: function() {
                //all options are passed to form
                this.containerOptions = {};
                this.formOptions = this.options;
            },
            tip: function() {
                return this.$tip;
            },
            innerShow: function() {
                this.$element.hide();
                this.tip().insertAfter(this.$element).show();
            },
            innerHide: function() {
                this.$tip.hide(this.options.anim, $.proxy(function() {
                    this.$element.show();
                    this.innerDestroy();
                }, this));
            },
            innerDestroy: function() {
                if (this.tip()) {
                    this.tip().empty().remove();
                }
            }
        });
    })(window.jQuery);
    /**
Makes editable any HTML element on the page. Applied as jQuery method.

@class editable
@uses editableContainer
**/
    (function($) {
        "use strict";
        var Editable = function(element, options) {
            this.$element = $(element);
            //data-* has more priority over js options: because dynamically created elements may change data-* 
            this.options = $.extend({}, $.fn.editable.defaults, options, $.fn.editableutils.getConfigData(this.$element));
            if (this.options.selector) {
                this.initLive();
            } else {
                this.init();
            }
            //check for transition support
            if (this.options.highlight && !$.fn.editableutils.supportsTransitions()) {
                this.options.highlight = false;
            }
        };
        Editable.prototype = {
            constructor: Editable,
            init: function() {
                var isValueByText = false, doAutotext, finalize;
                //name
                this.options.name = this.options.name || this.$element.attr("id");
                //create input of specified type. Input needed already here to convert value for initial display (e.g. show text by id for select)
                //also we set scope option to have access to element inside input specific callbacks (e. g. source as function)
                this.options.scope = this.$element[0];
                this.input = $.fn.editableutils.createInput(this.options);
                if (!this.input) {
                    return;
                }
                //set value from settings or by element's text
                if (this.options.value === undefined || this.options.value === null) {
                    this.value = this.input.html2value($.trim(this.$element.html()));
                    isValueByText = true;
                } else {
                    /*
                  value can be string when received from 'data-value' attribute
                  for complext objects value can be set as json string in data-value attribute, 
                  e.g. data-value="{city: 'Moscow', street: 'Lenina'}"
                */
                    this.options.value = $.fn.editableutils.tryParseJson(this.options.value, true);
                    if (typeof this.options.value === "string") {
                        this.value = this.input.str2value(this.options.value);
                    } else {
                        this.value = this.options.value;
                    }
                }
                //add 'editable' class to every editable element
                this.$element.addClass("editable");
                //specifically for "textarea" add class .editable-pre-wrapped to keep linebreaks
                if (this.input.type === "textarea") {
                    this.$element.addClass("editable-pre-wrapped");
                }
                //attach handler activating editable. In disabled mode it just prevent default action (useful for links)
                if (this.options.toggle !== "manual") {
                    this.$element.addClass("editable-click");
                    this.$element.on(this.options.toggle + ".editable", $.proxy(function(e) {
                        //prevent following link if editable enabled
                        if (!this.options.disabled) {
                            e.preventDefault();
                        }
                        //stop propagation not required because in document click handler it checks event target
                        //e.stopPropagation();
                        if (this.options.toggle === "mouseenter") {
                            //for hover only show container
                            this.show();
                        } else {
                            //when toggle='click' we should not close all other containers as they will be closed automatically in document click listener
                            var closeAll = this.options.toggle !== "click";
                            this.toggle(closeAll);
                        }
                    }, this));
                } else {
                    this.$element.attr("tabindex", -1);
                }
                //if display is function it's far more convinient to have autotext = always to render correctly on init
                //see https://github.com/vitalets/x-editable-yii/issues/34
                if (typeof this.options.display === "function") {
                    this.options.autotext = "always";
                }
                //check conditions for autotext:
                switch (this.options.autotext) {
                  case "always":
                    doAutotext = true;
                    break;

                  case "auto":
                    //if element text is empty and value is defined and value not generated by text --> run autotext
                    doAutotext = !$.trim(this.$element.text()).length && this.value !== null && this.value !== undefined && !isValueByText;
                    break;

                  default:
                    doAutotext = false;
                }
                //depending on autotext run render() or just finilize init
                $.when(doAutotext ? this.render() : true).then($.proxy(function() {
                    if (this.options.disabled) {
                        this.disable();
                    } else {
                        this.enable();
                    }
                    /**        
               Fired when element was initialized by `$().editable()` method. 
               Please note that you should setup `init` handler **before** applying `editable`. 
                              
               @event init 
               @param {Object} event event object
               @param {Object} editable editable instance (as here it cannot accessed via data('editable'))
               @since 1.2.0
               @example
               $('#username').on('init', function(e, editable) {
                   alert('initialized ' + editable.options.name);
               });
               $('#username').editable();
               **/
                    this.$element.triggerHandler("init", this);
                }, this));
            },
            /*
         Initializes parent element for live editables 
        */
            initLive: function() {
                //store selector 
                var selector = this.options.selector;
                //modify options for child elements
                this.options.selector = false;
                this.options.autotext = "never";
                //listen toggle events
                this.$element.on(this.options.toggle + ".editable", selector, $.proxy(function(e) {
                    var $target = $(e.target);
                    if (!$target.data("editable")) {
                        //if delegated element initially empty, we need to clear it's text (that was manually set to `empty` by user)
                        //see https://github.com/vitalets/x-editable/issues/137 
                        if ($target.hasClass(this.options.emptyclass)) {
                            $target.empty();
                        }
                        $target.editable(this.options).trigger(e);
                    }
                }, this));
            },
            /*
        Renders value into element's text.
        Can call custom display method from options.
        Can return deferred object.
        @method render()
        @param {mixed} response server response (if exist) to pass into display function
        */
            render: function(response) {
                //do not display anything
                if (this.options.display === false) {
                    return;
                }
                //if input has `value2htmlFinal` method, we pass callback in third param to be called when source is loaded
                if (this.input.value2htmlFinal) {
                    return this.input.value2html(this.value, this.$element[0], this.options.display, response);
                } else if (typeof this.options.display === "function") {
                    return this.options.display.call(this.$element[0], this.value, response);
                } else {
                    return this.input.value2html(this.value, this.$element[0]);
                }
            },
            /**
        Enables editable
        @method enable()
        **/
            enable: function() {
                this.options.disabled = false;
                this.$element.removeClass("editable-disabled");
                this.handleEmpty(this.isEmpty);
                if (this.options.toggle !== "manual") {
                    if (this.$element.attr("tabindex") === "-1") {
                        this.$element.removeAttr("tabindex");
                    }
                }
            },
            /**
        Disables editable
        @method disable()
        **/
            disable: function() {
                this.options.disabled = true;
                this.hide();
                this.$element.addClass("editable-disabled");
                this.handleEmpty(this.isEmpty);
                //do not stop focus on this element
                this.$element.attr("tabindex", -1);
            },
            /**
        Toggles enabled / disabled state of editable element
        @method toggleDisabled()
        **/
            toggleDisabled: function() {
                if (this.options.disabled) {
                    this.enable();
                } else {
                    this.disable();
                }
            },
            /**
        Sets new option
        
        @method option(key, value)
        @param {string|object} key option name or object with several options
        @param {mixed} value option new value
        @example
        $('.editable').editable('option', 'pk', 2);
        **/
            option: function(key, value) {
                //set option(s) by object
                if (key && typeof key === "object") {
                    $.each(key, $.proxy(function(k, v) {
                        this.option($.trim(k), v);
                    }, this));
                    return;
                }
                //set option by string             
                this.options[key] = value;
                //disabled
                if (key === "disabled") {
                    return value ? this.disable() : this.enable();
                }
                //value
                if (key === "value") {
                    this.setValue(value);
                }
                //transfer new option to container! 
                if (this.container) {
                    this.container.option(key, value);
                }
                //pass option to input directly (as it points to the same in form)
                if (this.input.option) {
                    this.input.option(key, value);
                }
            },
            /*
        * set emptytext if element is empty
        */
            handleEmpty: function(isEmpty) {
                //do not handle empty if we do not display anything
                if (this.options.display === false) {
                    return;
                }
                /* 
            isEmpty may be set directly as param of method.
            It is required when we enable/disable field and can't rely on content 
            as node content is text: "Empty" that is not empty %)
            */
                if (isEmpty !== undefined) {
                    this.isEmpty = isEmpty;
                } else {
                    //detect empty
                    //for some inputs we need more smart check
                    //e.g. wysihtml5 may have <br>, <p></p>, <img>
                    if (typeof this.input.isEmpty === "function") {
                        this.isEmpty = this.input.isEmpty(this.$element);
                    } else {
                        this.isEmpty = $.trim(this.$element.html()) === "";
                    }
                }
                //emptytext shown only for enabled
                if (!this.options.disabled) {
                    if (this.isEmpty) {
                        this.$element.html(this.options.emptytext);
                        if (this.options.emptyclass) {
                            this.$element.addClass(this.options.emptyclass);
                        }
                    } else if (this.options.emptyclass) {
                        this.$element.removeClass(this.options.emptyclass);
                    }
                } else {
                    //below required if element disable property was changed
                    if (this.isEmpty) {
                        this.$element.empty();
                        if (this.options.emptyclass) {
                            this.$element.removeClass(this.options.emptyclass);
                        }
                    }
                }
            },
            /**
        Shows container with form
        @method show()
        @param {boolean} closeAll Whether to close all other editable containers when showing this one. Default true.
        **/
            show: function(closeAll) {
                if (this.options.disabled) {
                    return;
                }
                //init editableContainer: popover, tooltip, inline, etc..
                if (!this.container) {
                    var containerOptions = $.extend({}, this.options, {
                        value: this.value,
                        input: this.input
                    });
                    this.$element.editableContainer(containerOptions);
                    //listen `save` event 
                    this.$element.on("save.internal", $.proxy(this.save, this));
                    this.container = this.$element.data("editableContainer");
                } else if (this.container.tip().is(":visible")) {
                    return;
                }
                //show container
                this.container.show(closeAll);
            },
            /**
        Hides container with form
        @method hide()
        **/
            hide: function() {
                if (this.container) {
                    this.container.hide();
                }
            },
            /**
        Toggles container visibility (show / hide)
        @method toggle()
        @param {boolean} closeAll Whether to close all other editable containers when showing this one. Default true.
        **/
            toggle: function(closeAll) {
                if (this.container && this.container.tip().is(":visible")) {
                    this.hide();
                } else {
                    this.show(closeAll);
                }
            },
            /*
        * called when form was submitted
        */
            save: function(e, params) {
                //mark element with unsaved class if needed
                if (this.options.unsavedclass) {
                    /*
                 Add unsaved css to element if:
                  - url is not user's function 
                  - value was not sent to server
                  - params.response === undefined, that means data was not sent
                  - value changed 
                */
                    var sent = false;
                    sent = sent || typeof this.options.url === "function";
                    sent = sent || this.options.display === false;
                    sent = sent || params.response !== undefined;
                    sent = sent || this.options.savenochange && this.input.value2str(this.value) !== this.input.value2str(params.newValue);
                    if (sent) {
                        this.$element.removeClass(this.options.unsavedclass);
                    } else {
                        this.$element.addClass(this.options.unsavedclass);
                    }
                }
                //highlight when saving
                if (this.options.highlight) {
                    var $e = this.$element, bgColor = $e.css("background-color");
                    $e.css("background-color", this.options.highlight);
                    setTimeout(function() {
                        if (bgColor === "transparent") {
                            bgColor = "";
                        }
                        $e.css("background-color", bgColor);
                        $e.addClass("editable-bg-transition");
                        setTimeout(function() {
                            $e.removeClass("editable-bg-transition");
                        }, 1700);
                    }, 10);
                }
                //set new value
                this.setValue(params.newValue, false, params.response);
            },
            validate: function() {
                if (typeof this.options.validate === "function") {
                    return this.options.validate.call(this, this.value);
                }
            },
            /**
        Sets new value of editable
        @method setValue(value, convertStr)
        @param {mixed} value new value 
        @param {boolean} convertStr whether to convert value from string to internal format
        **/
            setValue: function(value, convertStr, response) {
                if (convertStr) {
                    this.value = this.input.str2value(value);
                } else {
                    this.value = value;
                }
                if (this.container) {
                    this.container.option("value", this.value);
                }
                $.when(this.render(response)).then($.proxy(function() {
                    this.handleEmpty();
                }, this));
            },
            /**
        Activates input of visible container (e.g. set focus)
        @method activate()
        **/
            activate: function() {
                if (this.container) {
                    this.container.activate();
                }
            },
            /**
        Removes editable feature from element
        @method destroy()
        **/
            destroy: function() {
                this.disable();
                if (this.container) {
                    this.container.destroy();
                }
                this.input.destroy();
                if (this.options.toggle !== "manual") {
                    this.$element.removeClass("editable-click");
                    this.$element.off(this.options.toggle + ".editable");
                }
                this.$element.off("save.internal");
                this.$element.removeClass("editable editable-open editable-disabled");
                this.$element.removeData("editable");
            }
        };
        /* EDITABLE PLUGIN DEFINITION
    * ======================= */
        /**
    jQuery method to initialize editable element.
    
    @method $().editable(options)
    @params {Object} options
    @example
    $('#username').editable({
        type: 'text',
        url: '/post',
        pk: 1
    });
    **/
        $.fn.editable = function(option) {
            //special API methods returning non-jquery object
            var result = {}, args = arguments, datakey = "editable";
            switch (option) {
              /**
            Runs client-side validation for all matched editables
            
            @method validate()
            @returns {Object} validation errors map
            @example
            $('#username, #fullname').editable('validate');
            // possible result:
            {
              username: "username is required",
              fullname: "fullname should be minimum 3 letters length"
            }
            **/
                case "validate":
                this.each(function() {
                    var $this = $(this), data = $this.data(datakey), error;
                    if (data && (error = data.validate())) {
                        result[data.options.name] = error;
                    }
                });
                return result;

              /**
            Returns current values of editable elements.   
            Note that it returns an **object** with name-value pairs, not a value itself. It allows to get data from several elements.    
            If value of some editable is `null` or `undefined` it is excluded from result object.
            When param `isSingle` is set to **true** - it is supposed you have single element and will return value of editable instead of object.   
             
            @method getValue()
            @param {bool} isSingle whether to return just value of single element
            @returns {Object} object of element names and values
            @example
            $('#username, #fullname').editable('getValue');
            //result:
            {
            username: "superuser",
            fullname: "John"
            }
            //isSingle = true
            $('#username').editable('getValue', true);
            //result "superuser" 
            **/
                case "getValue":
                if (arguments.length === 2 && arguments[1] === true) {
                    //isSingle = true
                    result = this.eq(0).data(datakey).value;
                } else {
                    this.each(function() {
                        var $this = $(this), data = $this.data(datakey);
                        if (data && data.value !== undefined && data.value !== null) {
                            result[data.options.name] = data.input.value2submit(data.value);
                        }
                    });
                }
                return result;

              /**
            This method collects values from several editable elements and submit them all to server.   
            Internally it runs client-side validation for all fields and submits only in case of success.  
            See <a href="#newrecord">creating new records</a> for details.  
            Since 1.5.1 `submit` can be applied to single element to send data programmatically. In that case
            `url`, `success` and `error` is taken from initial options and you can just call `$('#username').editable('submit')`. 
            
            @method submit(options)
            @param {object} options 
            @param {object} options.url url to submit data 
            @param {object} options.data additional data to submit
            @param {object} options.ajaxOptions additional ajax options
            @param {function} options.error(obj) error handler 
            @param {function} options.success(obj,config) success handler
            @returns {Object} jQuery object
            **/
                case "submit":
                //collects value, validate and submit to server for creating new record
                var config = arguments[1] || {}, $elems = this, errors = this.editable("validate");
                // validation ok
                if ($.isEmptyObject(errors)) {
                    var ajaxOptions = {};
                    // for single element use url, success etc from options
                    if ($elems.length === 1) {
                        var editable = $elems.data("editable");
                        //standard params
                        var params = {
                            name: editable.options.name || "",
                            value: editable.input.value2submit(editable.value),
                            pk: typeof editable.options.pk === "function" ? editable.options.pk.call(editable.options.scope) : editable.options.pk
                        };
                        //additional params
                        if (typeof editable.options.params === "function") {
                            params = editable.options.params.call(editable.options.scope, params);
                        } else {
                            //try parse json in single quotes (from data-params attribute)
                            editable.options.params = $.fn.editableutils.tryParseJson(editable.options.params, true);
                            $.extend(params, editable.options.params);
                        }
                        ajaxOptions = {
                            url: editable.options.url,
                            data: params,
                            type: "POST"
                        };
                        // use success / error from options 
                        config.success = config.success || editable.options.success;
                        config.error = config.error || editable.options.error;
                    } else {
                        var values = this.editable("getValue");
                        ajaxOptions = {
                            url: config.url,
                            data: values,
                            type: "POST"
                        };
                    }
                    // ajax success callabck (response 200 OK)
                    ajaxOptions.success = typeof config.success === "function" ? function(response) {
                        config.success.call($elems, response, config);
                    } : $.noop;
                    // ajax error callabck
                    ajaxOptions.error = typeof config.error === "function" ? function() {
                        config.error.apply($elems, arguments);
                    } : $.noop;
                    // extend ajaxOptions    
                    if (config.ajaxOptions) {
                        $.extend(ajaxOptions, config.ajaxOptions);
                    }
                    // extra data 
                    if (config.data) {
                        $.extend(ajaxOptions.data, config.data);
                    }
                    // perform ajax request
                    $.ajax(ajaxOptions);
                } else {
                    //client-side validation error
                    if (typeof config.error === "function") {
                        config.error.call($elems, errors);
                    }
                }
                return this;
            }
            //return jquery object
            return this.each(function() {
                var $this = $(this), data = $this.data(datakey), options = typeof option === "object" && option;
                //for delegated targets do not store `editable` object for element
                //it's allows several different selectors.
                //see: https://github.com/vitalets/x-editable/issues/312    
                if (options && options.selector) {
                    data = new Editable(this, options);
                    return;
                }
                if (!data) {
                    $this.data(datakey, data = new Editable(this, options));
                }
                if (typeof option === "string") {
                    //call method 
                    data[option].apply(data, Array.prototype.slice.call(args, 1));
                }
            });
        };
        $.fn.editable.defaults = {
            /**
        Type of input. Can be <code>text|textarea|select|date|checklist</code> and more

        @property type 
        @type string
        @default 'text'
        **/
            type: "text",
            /**
        Sets disabled state of editable

        @property disabled 
        @type boolean
        @default false
        **/
            disabled: false,
            /**
        How to toggle editable. Can be <code>click|dblclick|mouseenter|manual</code>.   
        When set to <code>manual</code> you should manually call <code>show/hide</code> methods of editable.    
        **Note**: if you call <code>show</code> or <code>toggle</code> inside **click** handler of some DOM element, 
        you need to apply <code>e.stopPropagation()</code> because containers are being closed on any click on document.
        
        @example
        $('#edit-button').click(function(e) {
            e.stopPropagation();
            $('#username').editable('toggle');
        });

        @property toggle 
        @type string
        @default 'click'
        **/
            toggle: "click",
            /**
        Text shown when element is empty.

        @property emptytext 
        @type string
        @default 'Empty'
        **/
            emptytext: "Empty",
            /**
        Allows to automatically set element's text based on it's value. Can be <code>auto|always|never</code>. Useful for select and date.
        For example, if dropdown list is <code>{1: 'a', 2: 'b'}</code> and element's value set to <code>1</code>, it's html will be automatically set to <code>'a'</code>.  
        <code>auto</code> - text will be automatically set only if element is empty.  
        <code>always|never</code> - always(never) try to set element's text.

        @property autotext 
        @type string
        @default 'auto'
        **/
            autotext: "auto",
            /**
        Initial value of input. If not set, taken from element's text.  
        Note, that if element's text is empty - text is automatically generated from value and can be customized (see `autotext` option).  
        For example, to display currency sign:
        @example
        <a id="price" data-type="text" data-value="100"></a>
        <script>
        $('#price').editable({
            ...
            display: function(value) {
              $(this).text(value + '$');
            } 
        }) 
        </script>
                
        @property value 
        @type mixed
        @default element's text
        **/
            value: null,
            /**
        Callback to perform custom displaying of value in element's text.  
        If `null`, default input's display used.  
        If `false`, no displaying methods will be called, element's text will never change.  
        Runs under element's scope.  
        _**Parameters:**_  
        
        * `value` current value to be displayed
        * `response` server response (if display called after ajax submit), since 1.4.0
         
        For _inputs with source_ (select, checklist) parameters are different:  
          
        * `value` current value to be displayed
        * `sourceData` array of items for current input (e.g. dropdown items) 
        * `response` server response (if display called after ajax submit), since 1.4.0
                  
        To get currently selected items use `$.fn.editableutils.itemsByValue(value, sourceData)`.
        
        @property display 
        @type function|boolean
        @default null
        @since 1.2.0
        @example
        display: function(value, sourceData) {
           //display checklist as comma-separated values
           var html = [],
               checked = $.fn.editableutils.itemsByValue(value, sourceData);
               
           if(checked.length) {
               $.each(checked, function(i, v) { html.push($.fn.editableutils.escape(v.text)); });
               $(this).html(html.join(', '));
           } else {
               $(this).empty(); 
           }
        }
        **/
            display: null,
            /**
        Css class applied when editable text is empty.

        @property emptyclass 
        @type string
        @since 1.4.1        
        @default editable-empty
        **/
            emptyclass: "editable-empty",
            /**
        Css class applied when value was stored but not sent to server (`pk` is empty or `send = 'never'`).  
        You may set it to `null` if you work with editables locally and submit them together.  

        @property unsavedclass 
        @type string
        @since 1.4.1        
        @default editable-unsaved
        **/
            unsavedclass: "editable-unsaved",
            /**
        If selector is provided, editable will be delegated to the specified targets.  
        Usefull for dynamically generated DOM elements.  
        **Please note**, that delegated targets can't be initialized with `emptytext` and `autotext` options, 
        as they actually become editable only after first click.  
        You should manually set class `editable-click` to these elements.  
        Also, if element originally empty you should add class `editable-empty`, set `data-value=""` and write emptytext into element:

        @property selector 
        @type string
        @since 1.4.1        
        @default null
        @example
        <div id="user">
          <!-- empty -->
          <a href="#" data-name="username" data-type="text" class="editable-click editable-empty" data-value="" title="Username">Empty</a>
          <!-- non-empty -->
          <a href="#" data-name="group" data-type="select" data-source="/groups" data-value="1" class="editable-click" title="Group">Operator</a>
        </div>     
        
        <script>
        $('#user').editable({
            selector: 'a',
            url: '/post',
            pk: 1
        });
        </script>
        **/
            selector: null,
            /**
        Color used to highlight element after update. Implemented via CSS3 transition, works in modern browsers.
        
        @property highlight 
        @type string|boolean
        @since 1.4.5        
        @default #FFFF80 
        **/
            highlight: "#FFFF80"
        };
    })(window.jQuery);
    /**
AbstractInput - base class for all editable inputs.
It defines interface to be implemented by any input type.
To create your own input you can inherit from this class.

@class abstractinput
**/
    (function($) {
        "use strict";
        //types
        $.fn.editabletypes = {};
        var AbstractInput = function() {};
        AbstractInput.prototype = {
            /**
        Initializes input

        @method init() 
        **/
            init: function(type, options, defaults) {
                this.type = type;
                this.options = $.extend({}, defaults, options);
            },
            /*
       this method called before render to init $tpl that is inserted in DOM
       */
            prerender: function() {
                this.$tpl = $(this.options.tpl);
                //whole tpl as jquery object    
                this.$input = this.$tpl;
                //control itself, can be changed in render method
                this.$clear = null;
                //clear button
                this.error = null;
            },
            /**
        Renders input from tpl. Can return jQuery deferred object.
        Can be overwritten in child objects

        @method render()
       **/
            render: function() {},
            /**
        Sets element's html by value. 

        @method value2html(value, element)
        @param {mixed} value
        @param {DOMElement} element
       **/
            value2html: function(value, element) {
                $(element)[this.options.escape ? "text" : "html"]($.trim(value));
            },
            /**
        Converts element's html to value

        @method html2value(html)
        @param {string} html
        @returns {mixed}
       **/
            html2value: function(html) {
                return $("<div>").html(html).text();
            },
            /**
        Converts value to string (for internal compare). For submitting to server used value2submit().

        @method value2str(value) 
        @param {mixed} value
        @returns {string}
       **/
            value2str: function(value) {
                return value;
            },
            /**
        Converts string received from server into value. Usually from `data-value` attribute.

        @method str2value(str)
        @param {string} str
        @returns {mixed}
       **/
            str2value: function(str) {
                return str;
            },
            /**
        Converts value for submitting to server. Result can be string or object.

        @method value2submit(value) 
        @param {mixed} value
        @returns {mixed}
       **/
            value2submit: function(value) {
                return value;
            },
            /**
        Sets value of input.

        @method value2input(value) 
        @param {mixed} value
       **/
            value2input: function(value) {
                this.$input.val(value);
            },
            /**
        Returns value of input. Value can be object (e.g. datepicker)

        @method input2value() 
       **/
            input2value: function() {
                return this.$input.val();
            },
            /**
        Activates input. For text it sets focus.

        @method activate() 
       **/
            activate: function() {
                if (this.$input.is(":visible")) {
                    this.$input.focus();
                }
            },
            /**
        Creates input.

        @method clear() 
       **/
            clear: function() {
                this.$input.val(null);
            },
            /**
        method to escape html.
       **/
            escape: function(str) {
                return $("<div>").text(str).html();
            },
            /**
        attach handler to automatically submit form when value changed (useful when buttons not shown)
       **/
            autosubmit: function() {},
            /**
       Additional actions when destroying element 
       **/
            destroy: function() {},
            // -------- helper functions --------
            setClass: function() {
                if (this.options.inputclass) {
                    this.$input.addClass(this.options.inputclass);
                }
            },
            setAttr: function(attr) {
                if (this.options[attr] !== undefined && this.options[attr] !== null) {
                    this.$input.attr(attr, this.options[attr]);
                }
            },
            option: function(key, value) {
                this.options[key] = value;
            }
        };
        AbstractInput.defaults = {
            /**
        HTML template of input. Normally you should not change it.

        @property tpl 
        @type string
        @default ''
        **/
            tpl: "",
            /**
        CSS class automatically applied to input
        
        @property inputclass 
        @type string
        @default null
        **/
            inputclass: null,
            /**
        If `true` - html will be escaped in content of element via $.text() method.  
        If `false` - html will not be escaped, $.html() used.  
        When you use own `display` function, this option obviosly has no effect.
        
        @property escape 
        @type boolean
        @since 1.5.0
        @default true
        **/
            escape: true,
            //scope for external methods (e.g. source defined as function)
            //for internal use only
            scope: null,
            //need to re-declare showbuttons here to get it's value from common config (passed only options existing in defaults)
            showbuttons: true
        };
        $.extend($.fn.editabletypes, {
            abstractinput: AbstractInput
        });
    })(window.jQuery);
    /**
List - abstract class for inputs that have source option loaded from js array or via ajax

@class list
@extends abstractinput
**/
    (function($) {
        "use strict";
        var List = function(options) {};
        $.fn.editableutils.inherit(List, $.fn.editabletypes.abstractinput);
        $.extend(List.prototype, {
            render: function() {
                var deferred = $.Deferred();
                this.error = null;
                this.onSourceReady(function() {
                    this.renderList();
                    deferred.resolve();
                }, function() {
                    this.error = this.options.sourceError;
                    deferred.resolve();
                });
                return deferred.promise();
            },
            html2value: function(html) {
                return null;
            },
            value2html: function(value, element, display, response) {
                var deferred = $.Deferred(), success = function() {
                    if (typeof display === "function") {
                        //custom display method
                        display.call(element, value, this.sourceData, response);
                    } else {
                        this.value2htmlFinal(value, element);
                    }
                    deferred.resolve();
                };
                //for null value just call success without loading source
                if (value === null) {
                    success.call(this);
                } else {
                    this.onSourceReady(success, function() {
                        deferred.resolve();
                    });
                }
                return deferred.promise();
            },
            // ------------- additional functions ------------
            onSourceReady: function(success, error) {
                //run source if it function
                var source;
                if ($.isFunction(this.options.source)) {
                    source = this.options.source.call(this.options.scope);
                    this.sourceData = null;
                } else {
                    source = this.options.source;
                }
                //if allready loaded just call success
                if (this.options.sourceCache && $.isArray(this.sourceData)) {
                    success.call(this);
                    return;
                }
                //try parse json in single quotes (for double quotes jquery does automatically)
                try {
                    source = $.fn.editableutils.tryParseJson(source, false);
                } catch (e) {
                    error.call(this);
                    return;
                }
                //loading from url
                if (typeof source === "string") {
                    //try to get sourceData from cache
                    if (this.options.sourceCache) {
                        var cacheID = source, cache;
                        if (!$(document).data(cacheID)) {
                            $(document).data(cacheID, {});
                        }
                        cache = $(document).data(cacheID);
                        //check for cached data
                        if (cache.loading === false && cache.sourceData) {
                            //take source from cache
                            this.sourceData = cache.sourceData;
                            this.doPrepend();
                            success.call(this);
                            return;
                        } else if (cache.loading === true) {
                            //cache is loading, put callback in stack to be called later
                            cache.callbacks.push($.proxy(function() {
                                this.sourceData = cache.sourceData;
                                this.doPrepend();
                                success.call(this);
                            }, this));
                            //also collecting error callbacks
                            cache.err_callbacks.push($.proxy(error, this));
                            return;
                        } else {
                            //no cache yet, activate it
                            cache.loading = true;
                            cache.callbacks = [];
                            cache.err_callbacks = [];
                        }
                    }
                    //ajaxOptions for source. Can be overwritten bt options.sourceOptions
                    var ajaxOptions = $.extend({
                        url: source,
                        type: "get",
                        cache: false,
                        dataType: "json",
                        success: $.proxy(function(data) {
                            if (cache) {
                                cache.loading = false;
                            }
                            this.sourceData = this.makeArray(data);
                            if ($.isArray(this.sourceData)) {
                                if (cache) {
                                    //store result in cache
                                    cache.sourceData = this.sourceData;
                                    //run success callbacks for other fields waiting for this source
                                    $.each(cache.callbacks, function() {
                                        this.call();
                                    });
                                }
                                this.doPrepend();
                                success.call(this);
                            } else {
                                error.call(this);
                                if (cache) {
                                    //run error callbacks for other fields waiting for this source
                                    $.each(cache.err_callbacks, function() {
                                        this.call();
                                    });
                                }
                            }
                        }, this),
                        error: $.proxy(function() {
                            error.call(this);
                            if (cache) {
                                cache.loading = false;
                                //run error callbacks for other fields
                                $.each(cache.err_callbacks, function() {
                                    this.call();
                                });
                            }
                        }, this)
                    }, this.options.sourceOptions);
                    //loading sourceData from server
                    $.ajax(ajaxOptions);
                } else {
                    //options as json/array
                    this.sourceData = this.makeArray(source);
                    if ($.isArray(this.sourceData)) {
                        this.doPrepend();
                        success.call(this);
                    } else {
                        error.call(this);
                    }
                }
            },
            doPrepend: function() {
                if (this.options.prepend === null || this.options.prepend === undefined) {
                    return;
                }
                if (!$.isArray(this.prependData)) {
                    //run prepend if it is function (once)
                    if ($.isFunction(this.options.prepend)) {
                        this.options.prepend = this.options.prepend.call(this.options.scope);
                    }
                    //try parse json in single quotes
                    this.options.prepend = $.fn.editableutils.tryParseJson(this.options.prepend, true);
                    //convert prepend from string to object
                    if (typeof this.options.prepend === "string") {
                        this.options.prepend = {
                            "": this.options.prepend
                        };
                    }
                    this.prependData = this.makeArray(this.options.prepend);
                }
                if ($.isArray(this.prependData) && $.isArray(this.sourceData)) {
                    this.sourceData = this.prependData.concat(this.sourceData);
                }
            },
            /*
         renders input list
        */
            renderList: function() {},
            /*
         set element's html by value
        */
            value2htmlFinal: function(value, element) {},
            /**
        * convert data to array suitable for sourceData, e.g. [{value: 1, text: 'abc'}, {...}]
        */
            makeArray: function(data) {
                var count, obj, result = [], item, iterateItem;
                if (!data || typeof data === "string") {
                    return null;
                }
                if ($.isArray(data)) {
                    //array
                    /* 
                   function to iterate inside item of array if item is object.
                   Caclulates count of keys in item and store in obj. 
                */
                    iterateItem = function(k, v) {
                        obj = {
                            value: k,
                            text: v
                        };
                        if (count++ >= 2) {
                            return false;
                        }
                    };
                    for (var i = 0; i < data.length; i++) {
                        item = data[i];
                        if (typeof item === "object") {
                            count = 0;
                            //count of keys inside item
                            $.each(item, iterateItem);
                            //case: [{val1: 'text1'}, {val2: 'text2} ...]
                            if (count === 1) {
                                result.push(obj);
                            } else if (count > 1) {
                                //removed check of existance: item.hasOwnProperty('value') && item.hasOwnProperty('text')
                                if (item.children) {
                                    item.children = this.makeArray(item.children);
                                }
                                result.push(item);
                            }
                        } else {
                            //case: ['text1', 'text2' ...]
                            result.push({
                                value: item,
                                text: item
                            });
                        }
                    }
                } else {
                    //case: {val1: 'text1', val2: 'text2, ...}
                    $.each(data, function(k, v) {
                        result.push({
                            value: k,
                            text: v
                        });
                    });
                }
                return result;
            },
            option: function(key, value) {
                this.options[key] = value;
                if (key === "source") {
                    this.sourceData = null;
                }
                if (key === "prepend") {
                    this.prependData = null;
                }
            }
        });
        List.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
            /**
        Source data for list.  
        If **array** - it should be in format: `[{value: 1, text: "text1"}, {value: 2, text: "text2"}, ...]`  
        For compability, object format is also supported: `{"1": "text1", "2": "text2" ...}` but it does not guarantee elements order.
        
        If **string** - considered ajax url to load items. In that case results will be cached for fields with the same source and name. See also `sourceCache` option.
          
        If **function**, it should return data in format above (since 1.4.0).
        
        Since 1.4.1 key `children` supported to render OPTGROUP (for **select** input only).  
        `[{text: "group1", children: [{value: 1, text: "text1"}, {value: 2, text: "text2"}]}, ...]` 

		
        @property source 
        @type string | array | object | function
        @default null
        **/
            source: null,
            /**
        Data automatically prepended to the beginning of dropdown list.
        
        @property prepend 
        @type string | array | object | function
        @default false
        **/
            prepend: false,
            /**
        Error message when list cannot be loaded (e.g. ajax error)
        
        @property sourceError 
        @type string
        @default Error when loading list
        **/
            sourceError: "Error when loading list",
            /**
        if <code>true</code> and source is **string url** - results will be cached for fields with the same source.    
        Usefull for editable column in grid to prevent extra requests.
        
        @property sourceCache 
        @type boolean
        @default true
        @since 1.2.0
        **/
            sourceCache: true,
            /**
        Additional ajax options to be used in $.ajax() when loading list from server.
        Useful to send extra parameters (`data` key) or change request method (`type` key).
        
        @property sourceOptions 
        @type object|function
        @default null
        @since 1.5.0
        **/
            sourceOptions: null
        });
        $.fn.editabletypes.list = List;
    })(window.jQuery);
    /**
Text input

@class text
@extends abstractinput
@final
@example
<a href="#" id="username" data-type="text" data-pk="1">awesome</a>
<script>
$(function(){
    $('#username').editable({
        url: '/post',
        title: 'Enter username'
    });
});
</script>
**/
    (function($) {
        "use strict";
        var Text = function(options) {
            this.init("text", options, Text.defaults);
        };
        $.fn.editableutils.inherit(Text, $.fn.editabletypes.abstractinput);
        $.extend(Text.prototype, {
            render: function() {
                this.renderClear();
                this.setClass();
                this.setAttr("placeholder");
            },
            activate: function() {
                if (this.$input.is(":visible")) {
                    this.$input.focus();
                    $.fn.editableutils.setCursorPosition(this.$input.get(0), this.$input.val().length);
                    if (this.toggleClear) {
                        this.toggleClear();
                    }
                }
            },
            //render clear button
            renderClear: function() {
                if (this.options.clear) {
                    this.$clear = $('<span class="editable-clear-x"></span>');
                    this.$input.after(this.$clear).css("padding-right", 24).keyup($.proxy(function(e) {
                        //arrows, enter, tab, etc
                        if (~$.inArray(e.keyCode, [ 40, 38, 9, 13, 27 ])) {
                            return;
                        }
                        clearTimeout(this.t);
                        var that = this;
                        this.t = setTimeout(function() {
                            that.toggleClear(e);
                        }, 100);
                    }, this)).parent().css("position", "relative");
                    this.$clear.click($.proxy(this.clear, this));
                }
            },
            postrender: function() {},
            //show / hide clear button
            toggleClear: function(e) {
                if (!this.$clear) {
                    return;
                }
                var len = this.$input.val().length, visible = this.$clear.is(":visible");
                if (len && !visible) {
                    this.$clear.show();
                }
                if (!len && visible) {
                    this.$clear.hide();
                }
            },
            clear: function() {
                this.$clear.hide();
                this.$input.val("").focus();
            }
        });
        Text.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
            /**
        @property tpl 
        @default <input type="text">
        **/
            tpl: '<input type="text">',
            /**
        Placeholder attribute of input. Shown when input is empty.

        @property placeholder 
        @type string
        @default null
        **/
            placeholder: null,
            /**
        Whether to show `clear` button 
        
        @property clear 
        @type boolean
        @default true        
        **/
            clear: true
        });
        $.fn.editabletypes.text = Text;
    })(window.jQuery);
    /**
Textarea input

@class textarea
@extends abstractinput
@final
@example
<a href="#" id="comments" data-type="textarea" data-pk="1">awesome comment!</a>
<script>
$(function(){
    $('#comments').editable({
        url: '/post',
        title: 'Enter comments',
        rows: 10
    });
});
</script>
**/
    (function($) {
        "use strict";
        var Textarea = function(options) {
            this.init("textarea", options, Textarea.defaults);
        };
        $.fn.editableutils.inherit(Textarea, $.fn.editabletypes.abstractinput);
        $.extend(Textarea.prototype, {
            render: function() {
                this.setClass();
                this.setAttr("placeholder");
                this.setAttr("rows");
                //ctrl + enter
                this.$input.keydown(function(e) {
                    if (e.ctrlKey && e.which === 13) {
                        $(this).closest("form").submit();
                    }
                });
            },
            //using `white-space: pre-wrap` solves \n  <--> BR conversion very elegant!
            /* 
       value2html: function(value, element) {
            var html = '', lines;
            if(value) {
                lines = value.split("\n");
                for (var i = 0; i < lines.length; i++) {
                    lines[i] = $('<div>').text(lines[i]).html();
                }
                html = lines.join('<br>');
            }
            $(element).html(html);
        },
       
        html2value: function(html) {
            if(!html) {
                return '';
            }

            var regex = new RegExp(String.fromCharCode(10), 'g');
            var lines = html.split(/<br\s*\/?>/i);
            for (var i = 0; i < lines.length; i++) {
                var text = $('<div>').html(lines[i]).text();

                // Remove newline characters (\n) to avoid them being converted by value2html() method
                // thus adding extra <br> tags
                text = text.replace(regex, '');

                lines[i] = text;
            }
            return lines.join("\n");
        },
         */
            activate: function() {
                $.fn.editabletypes.text.prototype.activate.call(this);
            }
        });
        Textarea.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
            /**
        @property tpl
        @default <textarea></textarea>
        **/
            tpl: "<textarea></textarea>",
            /**
        @property inputclass
        @default input-large
        **/
            inputclass: "input-large",
            /**
        Placeholder attribute of input. Shown when input is empty.

        @property placeholder
        @type string
        @default null
        **/
            placeholder: null,
            /**
        Number of rows in textarea

        @property rows
        @type integer
        @default 7
        **/
            rows: 7
        });
        $.fn.editabletypes.textarea = Textarea;
    })(window.jQuery);
    /**
Select (dropdown)

@class select
@extends list
@final
@example
<a href="#" id="status" data-type="select" data-pk="1" data-url="/post" data-title="Select status"></a>
<script>
$(function(){
    $('#status').editable({
        value: 2,    
        source: [
              {value: 1, text: 'Active'},
              {value: 2, text: 'Blocked'},
              {value: 3, text: 'Deleted'}
           ]
    });
});
</script>
**/
    (function($) {
        "use strict";
        var Select = function(options) {
            this.init("select", options, Select.defaults);
        };
        $.fn.editableutils.inherit(Select, $.fn.editabletypes.list);
        $.extend(Select.prototype, {
            renderList: function() {
                this.$input.empty();
                var fillItems = function($el, data) {
                    var attr;
                    if ($.isArray(data)) {
                        for (var i = 0; i < data.length; i++) {
                            attr = {};
                            if (data[i].children) {
                                attr.label = data[i].text;
                                $el.append(fillItems($("<optgroup>", attr), data[i].children));
                            } else {
                                attr.value = data[i].value;
                                if (data[i].disabled) {
                                    attr.disabled = true;
                                }
                                $el.append($("<option>", attr).text(data[i].text));
                            }
                        }
                    }
                    return $el;
                };
                fillItems(this.$input, this.sourceData);
                this.setClass();
                //enter submit
                this.$input.on("keydown.editable", function(e) {
                    if (e.which === 13) {
                        $(this).closest("form").submit();
                    }
                });
            },
            value2htmlFinal: function(value, element) {
                var text = "", items = $.fn.editableutils.itemsByValue(value, this.sourceData);
                if (items.length) {
                    text = items[0].text;
                }
                //$(element).text(text);
                $.fn.editabletypes.abstractinput.prototype.value2html.call(this, text, element);
            },
            autosubmit: function() {
                this.$input.off("keydown.editable").on("change.editable", function() {
                    $(this).closest("form").submit();
                });
            }
        });
        Select.defaults = $.extend({}, $.fn.editabletypes.list.defaults, {
            /**
        @property tpl 
        @default <select></select>
        **/
            tpl: "<select></select>"
        });
        $.fn.editabletypes.select = Select;
    })(window.jQuery);
    /**
List of checkboxes. 
Internally value stored as javascript array of values.

@class checklist
@extends list
@final
@example
<a href="#" id="options" data-type="checklist" data-pk="1" data-url="/post" data-title="Select options"></a>
<script>
$(function(){
    $('#options').editable({
        value: [2, 3],    
        source: [
              {value: 1, text: 'option1'},
              {value: 2, text: 'option2'},
              {value: 3, text: 'option3'}
           ]
    });
});
</script>
**/
    (function($) {
        "use strict";
        var Checklist = function(options) {
            this.init("checklist", options, Checklist.defaults);
        };
        $.fn.editableutils.inherit(Checklist, $.fn.editabletypes.list);
        $.extend(Checklist.prototype, {
            renderList: function() {
                var $label, $div;
                this.$tpl.empty();
                if (!$.isArray(this.sourceData)) {
                    return;
                }
                for (var i = 0; i < this.sourceData.length; i++) {
                    $label = $("<label>").append($("<input>", {
                        type: "checkbox",
                        value: this.sourceData[i].value
                    })).append($("<span>").text(" " + this.sourceData[i].text));
                    $("<div>").append($label).appendTo(this.$tpl);
                }
                this.$input = this.$tpl.find('input[type="checkbox"]');
                this.setClass();
            },
            value2str: function(value) {
                return $.isArray(value) ? value.sort().join($.trim(this.options.separator)) : "";
            },
            //parse separated string
            str2value: function(str) {
                var reg, value = null;
                if (typeof str === "string" && str.length) {
                    reg = new RegExp("\\s*" + $.trim(this.options.separator) + "\\s*");
                    value = str.split(reg);
                } else if ($.isArray(str)) {
                    value = str;
                } else {
                    value = [ str ];
                }
                return value;
            },
            //set checked on required checkboxes
            value2input: function(value) {
                this.$input.prop("checked", false);
                if ($.isArray(value) && value.length) {
                    this.$input.each(function(i, el) {
                        var $el = $(el);
                        // cannot use $.inArray as it performs strict comparison
                        $.each(value, function(j, val) {
                            /*jslint eqeq: true*/
                            if ($el.val() == val) {
                                /*jslint eqeq: false*/
                                $el.prop("checked", true);
                            }
                        });
                    });
                }
            },
            input2value: function() {
                var checked = [];
                this.$input.filter(":checked").each(function(i, el) {
                    checked.push($(el).val());
                });
                return checked;
            },
            //collect text of checked boxes
            value2htmlFinal: function(value, element) {
                var html = [], checked = $.fn.editableutils.itemsByValue(value, this.sourceData), escape = this.options.escape;
                if (checked.length) {
                    $.each(checked, function(i, v) {
                        var text = escape ? $.fn.editableutils.escape(v.text) : v.text;
                        html.push(text);
                    });
                    $(element).html(html.join("<br>"));
                } else {
                    $(element).empty();
                }
            },
            activate: function() {
                this.$input.first().focus();
            },
            autosubmit: function() {
                this.$input.on("keydown", function(e) {
                    if (e.which === 13) {
                        $(this).closest("form").submit();
                    }
                });
            }
        });
        Checklist.defaults = $.extend({}, $.fn.editabletypes.list.defaults, {
            /**
        @property tpl 
        @default <div></div>
        **/
            tpl: '<div class="editable-checklist"></div>',
            /**
        @property inputclass 
        @type string
        @default null
        **/
            inputclass: null,
            /**
        Separator of values when reading from `data-value` attribute

        @property separator 
        @type string
        @default ','
        **/
            separator: ","
        });
        $.fn.editabletypes.checklist = Checklist;
    })(window.jQuery);
    /**
HTML5 input types.
Following types are supported:

* password
* email
* url
* tel
* number
* range
* time

Learn more about html5 inputs:  
http://www.w3.org/wiki/HTML5_form_additions  
To check browser compatibility please see:  
https://developer.mozilla.org/en-US/docs/HTML/Element/Input
            
@class html5types 
@extends text
@final
@since 1.3.0
@example
<a href="#" id="email" data-type="email" data-pk="1">admin@example.com</a>
<script>
$(function(){
    $('#email').editable({
        url: '/post',
        title: 'Enter email'
    });
});
</script>
**/
    /**
@property tpl 
@default depends on type
**/
    /*
Password
*/
    (function($) {
        "use strict";
        var Password = function(options) {
            this.init("password", options, Password.defaults);
        };
        $.fn.editableutils.inherit(Password, $.fn.editabletypes.text);
        $.extend(Password.prototype, {
            //do not display password, show '[hidden]' instead
            value2html: function(value, element) {
                if (value) {
                    $(element).text("[hidden]");
                } else {
                    $(element).empty();
                }
            },
            //as password not displayed, should not set value by html
            html2value: function(html) {
                return null;
            }
        });
        Password.defaults = $.extend({}, $.fn.editabletypes.text.defaults, {
            tpl: '<input type="password">'
        });
        $.fn.editabletypes.password = Password;
    })(window.jQuery);
    /*
Email
*/
    (function($) {
        "use strict";
        var Email = function(options) {
            this.init("email", options, Email.defaults);
        };
        $.fn.editableutils.inherit(Email, $.fn.editabletypes.text);
        Email.defaults = $.extend({}, $.fn.editabletypes.text.defaults, {
            tpl: '<input type="email">'
        });
        $.fn.editabletypes.email = Email;
    })(window.jQuery);
    /*
Url
*/
    (function($) {
        "use strict";
        var Url = function(options) {
            this.init("url", options, Url.defaults);
        };
        $.fn.editableutils.inherit(Url, $.fn.editabletypes.text);
        Url.defaults = $.extend({}, $.fn.editabletypes.text.defaults, {
            tpl: '<input type="url">'
        });
        $.fn.editabletypes.url = Url;
    })(window.jQuery);
    /*
Tel
*/
    (function($) {
        "use strict";
        var Tel = function(options) {
            this.init("tel", options, Tel.defaults);
        };
        $.fn.editableutils.inherit(Tel, $.fn.editabletypes.text);
        Tel.defaults = $.extend({}, $.fn.editabletypes.text.defaults, {
            tpl: '<input type="tel">'
        });
        $.fn.editabletypes.tel = Tel;
    })(window.jQuery);
    /*
Number
*/
    (function($) {
        "use strict";
        var NumberInput = function(options) {
            this.init("number", options, NumberInput.defaults);
        };
        $.fn.editableutils.inherit(NumberInput, $.fn.editabletypes.text);
        $.extend(NumberInput.prototype, {
            render: function() {
                NumberInput.superclass.render.call(this);
                this.setAttr("min");
                this.setAttr("max");
                this.setAttr("step");
            },
            postrender: function() {
                if (this.$clear) {
                    //increase right ffset  for up/down arrows
                    this.$clear.css({
                        right: 24
                    });
                }
            }
        });
        NumberInput.defaults = $.extend({}, $.fn.editabletypes.text.defaults, {
            tpl: '<input type="number">',
            inputclass: "input-mini",
            min: null,
            max: null,
            step: null
        });
        $.fn.editabletypes.number = NumberInput;
    })(window.jQuery);
    /*
Range (inherit from number)
*/
    (function($) {
        "use strict";
        var Range = function(options) {
            this.init("range", options, Range.defaults);
        };
        $.fn.editableutils.inherit(Range, $.fn.editabletypes.number);
        $.extend(Range.prototype, {
            render: function() {
                this.$input = this.$tpl.filter("input");
                this.setClass();
                this.setAttr("min");
                this.setAttr("max");
                this.setAttr("step");
                this.$input.on("input", function() {
                    $(this).siblings("output").text($(this).val());
                });
            },
            activate: function() {
                this.$input.focus();
            }
        });
        Range.defaults = $.extend({}, $.fn.editabletypes.number.defaults, {
            tpl: '<input type="range"><output style="width: 30px; display: inline-block"></output>',
            inputclass: "input-medium"
        });
        $.fn.editabletypes.range = Range;
    })(window.jQuery);
    /*
Time
*/
    (function($) {
        "use strict";
        var Time = function(options) {
            this.init("time", options, Time.defaults);
        };
        //inherit from abstract, as inheritance from text gives selection error.
        $.fn.editableutils.inherit(Time, $.fn.editabletypes.abstractinput);
        $.extend(Time.prototype, {
            render: function() {
                this.setClass();
            }
        });
        Time.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
            tpl: '<input type="time">'
        });
        $.fn.editabletypes.time = Time;
    })(window.jQuery);
    /**
Select2 input. Based on amazing work of Igor Vaynberg https://github.com/ivaynberg/select2.  
Please see [original select2 docs](http://ivaynberg.github.com/select2) for detailed description and options.  
 
You should manually download and include select2 distributive:  

    <link href="select2/select2.css" rel="stylesheet" type="text/css"></link>  
    <script src="select2/select2.js"></script>  
    
To make it **bootstrap-styled** you can use css from [here](https://github.com/t0m/select2-bootstrap-css): 

    <link href="select2-bootstrap.css" rel="stylesheet" type="text/css"></link>    
    
**Note:** currently `autotext` feature does not work for select2 with `ajax` remote source.    
You need initially put both `data-value` and element's text youself:    

    <a href="#" data-type="select2" data-value="1">Text1</a>
    
    
@class select2
@extends abstractinput
@since 1.4.1
@final
@example
<a href="#" id="country" data-type="select2" data-pk="1" data-value="ru" data-url="/post" data-title="Select country"></a>
<script>
$(function(){
    //local source
    $('#country').editable({
        source: [
              {id: 'gb', text: 'Great Britain'},
              {id: 'us', text: 'United States'},
              {id: 'ru', text: 'Russia'}
           ],
        select2: {
           multiple: true
        }
    });
    //remote source (simple)
    $('#country').editable({
        source: '/getCountries',
        select2: {
            placeholder: 'Select Country',
            minimumInputLength: 1
        }
    });
    //remote source (advanced)
    $('#country').editable({
        select2: {
            placeholder: 'Select Country',
            allowClear: true,
            minimumInputLength: 3,
            id: function (item) {
                return item.CountryId;
            },
            ajax: {
                url: '/getCountries',
                dataType: 'json',
                data: function (term, page) {
                    return { query: term };
                },
                results: function (data, page) {
                    return { results: data };
                }
            },
            formatResult: function (item) {
                return item.CountryName;
            },
            formatSelection: function (item) {
                return item.CountryName;
            },
            initSelection: function (element, callback) {
                return $.get('/getCountryById', { query: element.val() }, function (data) {
                    callback(data);
                });
            } 
        }  
    });
});
</script>
**/
    (function($) {
        "use strict";
        var Constructor = function(options) {
            this.init("select2", options, Constructor.defaults);
            options.select2 = options.select2 || {};
            this.sourceData = null;
            //placeholder
            if (options.placeholder) {
                options.select2.placeholder = options.placeholder;
            }
            //if not `tags` mode, use source
            if (!options.select2.tags && options.source) {
                var source = options.source;
                //if source is function, call it (once!)
                if ($.isFunction(options.source)) {
                    source = options.source.call(options.scope);
                }
                if (typeof source === "string") {
                    options.select2.ajax = options.select2.ajax || {};
                    //some default ajax params
                    if (!options.select2.ajax.data) {
                        options.select2.ajax.data = function(term) {
                            return {
                                query: term
                            };
                        };
                    }
                    if (!options.select2.ajax.results) {
                        options.select2.ajax.results = function(data) {
                            return {
                                results: data
                            };
                        };
                    }
                    options.select2.ajax.url = source;
                } else {
                    //check format and convert x-editable format to select2 format (if needed)
                    this.sourceData = this.convertSource(source);
                    options.select2.data = this.sourceData;
                }
            }
            //overriding objects in config (as by default jQuery extend() is not recursive)
            this.options.select2 = $.extend({}, Constructor.defaults.select2, options.select2);
            //detect whether it is multi-valued
            this.isMultiple = this.options.select2.tags || this.options.select2.multiple;
            this.isRemote = "ajax" in this.options.select2;
            //store function returning ID of item
            //should be here as used inautotext for local source
            this.idFunc = this.options.select2.id;
            if (typeof this.idFunc !== "function") {
                var idKey = this.idFunc || "id";
                this.idFunc = function(e) {
                    return e[idKey];
                };
            }
            //store function that renders text in select2
            this.formatSelection = this.options.select2.formatSelection;
            if (typeof this.formatSelection !== "function") {
                this.formatSelection = function(e) {
                    return e.text;
                };
            }
        };
        $.fn.editableutils.inherit(Constructor, $.fn.editabletypes.abstractinput);
        $.extend(Constructor.prototype, {
            render: function() {
                this.setClass();
                //can not apply select2 here as it calls initSelection 
                //over input that does not have correct value yet.
                //apply select2 only in value2input
                //this.$input.select2(this.options.select2);
                //when data is loaded via ajax, we need to know when it's done to populate listData
                if (this.isRemote) {
                    //listen to loaded event to populate data
                    this.$input.on("select2-loaded", $.proxy(function(e) {
                        this.sourceData = e.items.results;
                    }, this));
                }
                //trigger resize of editableform to re-position container in multi-valued mode
                if (this.isMultiple) {
                    this.$input.on("change", function() {
                        $(this).closest("form").parent().triggerHandler("resize");
                    });
                }
            },
            value2html: function(value, element) {
                var text = "", data, that = this;
                if (this.options.select2.tags) {
                    //in tags mode just assign value
                    data = value;
                } else if (this.sourceData) {
                    data = $.fn.editableutils.itemsByValue(value, this.sourceData, this.idFunc);
                } else {}
                //data may be array (when multiple values allowed)
                if ($.isArray(data)) {
                    //collect selected data and show with separator
                    text = [];
                    $.each(data, function(k, v) {
                        text.push(v && typeof v === "object" ? that.formatSelection(v) : v);
                    });
                } else if (data) {
                    text = that.formatSelection(data);
                }
                text = $.isArray(text) ? text.join(this.options.viewseparator) : text;
                //$(element).text(text);
                Constructor.superclass.value2html.call(this, text, element);
            },
            html2value: function(html) {
                return this.options.select2.tags ? this.str2value(html, this.options.viewseparator) : null;
            },
            value2input: function(value) {
                // if value array => join it anyway
                if ($.isArray(value)) {
                    value = value.join(this.getSeparator());
                }
                //for remote source just set value, text is updated by initSelection
                if (!this.$input.data("select2")) {
                    this.$input.val(value);
                    this.$input.select2(this.options.select2);
                } else {
                    //second argument needed to separate initial change from user's click (for autosubmit)   
                    this.$input.val(value).trigger("change", true);
                }
                // if defined remote source AND no multiple mode AND no user's initSelection provided --> 
                // we should somehow get text for provided id.
                // The solution is to use element's text as text for that id (exclude empty)
                if (this.isRemote && !this.isMultiple && !this.options.select2.initSelection) {
                    // customId and customText are methods to extract `id` and `text` from data object
                    // we can use this workaround only if user did not define these methods
                    // otherwise we cant construct data object
                    var customId = this.options.select2.id, customText = this.options.select2.formatSelection;
                    if (!customId && !customText) {
                        var $el = $(this.options.scope);
                        if (!$el.data("editable").isEmpty) {
                            var data = {
                                id: value,
                                text: $el.text()
                            };
                            this.$input.select2("data", data);
                        }
                    }
                }
            },
            input2value: function() {
                return this.$input.select2("val");
            },
            str2value: function(str, separator) {
                if (typeof str !== "string" || !this.isMultiple) {
                    return str;
                }
                separator = separator || this.getSeparator();
                var val, i, l;
                if (str === null || str.length < 1) {
                    return null;
                }
                val = str.split(separator);
                for (i = 0, l = val.length; i < l; i = i + 1) {
                    val[i] = $.trim(val[i]);
                }
                return val;
            },
            autosubmit: function() {
                this.$input.on("change", function(e, isInitial) {
                    if (!isInitial) {
                        $(this).closest("form").submit();
                    }
                });
            },
            getSeparator: function() {
                return this.options.select2.separator || $.fn.select2.defaults.separator;
            },
            /*
        Converts source from x-editable format: {value: 1, text: "1"} to
        select2 format: {id: 1, text: "1"}
        */
            convertSource: function(source) {
                if ($.isArray(source) && source.length && source[0].value !== undefined) {
                    for (var i = 0; i < source.length; i++) {
                        if (source[i].value !== undefined) {
                            source[i].id = source[i].value;
                            delete source[i].value;
                        }
                    }
                }
                return source;
            },
            destroy: function() {
                if (this.$input.data("select2")) {
                    this.$input.select2("destroy");
                }
            }
        });
        Constructor.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
            /**
        @property tpl 
        @default <input type="hidden">
        **/
            tpl: '<input type="hidden">',
            /**
        Configuration of select2. [Full list of options](http://ivaynberg.github.com/select2).

        @property select2 
        @type object
        @default null
        **/
            select2: null,
            /**
        Placeholder attribute of select

        @property placeholder 
        @type string
        @default null
        **/
            placeholder: null,
            /**
        Source data for select. It will be assigned to select2 `data` property and kept here just for convenience.
        Please note, that format is different from simple `select` input: use 'id' instead of 'value'.
        E.g. `[{id: 1, text: "text1"}, {id: 2, text: "text2"}, ...]`.

        @property source 
        @type array|string|function
        @default null        
        **/
            source: null,
            /**
        Separator used to display tags.

        @property viewseparator 
        @type string
        @default ', '        
        **/
            viewseparator: ", "
        });
        $.fn.editabletypes.select2 = Constructor;
    })(window.jQuery);
    /**
* Combodate - 1.0.5
* Dropdown date and time picker.
* Converts text input into dropdowns to pick day, month, year, hour, minute and second.
* Uses momentjs as datetime library http://momentjs.com.
* For i18n include corresponding file from https://github.com/timrwood/moment/tree/master/lang 
*
* Confusion at noon and midnight - see http://en.wikipedia.org/wiki/12-hour_clock#Confusion_at_noon_and_midnight
* In combodate: 
* 12:00 pm --> 12:00 (24-h format, midday)
* 12:00 am --> 00:00 (24-h format, midnight, start of day)
* 
* Differs from momentjs parse rules:
* 00:00 pm, 12:00 pm --> 12:00 (24-h format, day not change)
* 00:00 am, 12:00 am --> 00:00 (24-h format, day not change)
* 
* 
* Author: Vitaliy Potapov
* Project page: http://github.com/vitalets/combodate
* Copyright (c) 2012 Vitaliy Potapov. Released under MIT License.
**/
    (function($) {
        var Combodate = function(element, options) {
            this.$element = $(element);
            if (!this.$element.is("input")) {
                $.error("Combodate should be applied to INPUT element");
                return;
            }
            this.options = $.extend({}, $.fn.combodate.defaults, options, this.$element.data());
            this.init();
        };
        Combodate.prototype = {
            constructor: Combodate,
            init: function() {
                this.map = {
                    //key   regexp    moment.method
                    day: [ "D", "date" ],
                    month: [ "M", "month" ],
                    year: [ "Y", "year" ],
                    hour: [ "[Hh]", "hours" ],
                    minute: [ "m", "minutes" ],
                    second: [ "s", "seconds" ],
                    ampm: [ "[Aa]", "" ]
                };
                this.$widget = $('<span class="combodate"></span>').html(this.getTemplate());
                this.initCombos();
                //update original input on change 
                this.$widget.on("change", "select", $.proxy(function(e) {
                    this.$element.val(this.getValue()).change();
                    // update days count if month or year changes
                    if (this.options.smartDays) {
                        if ($(e.target).is(".month") || $(e.target).is(".year")) {
                            this.fillCombo("day");
                        }
                    }
                }, this));
                this.$widget.find("select").css("width", "auto");
                // hide original input and insert widget                                       
                this.$element.hide().after(this.$widget);
                // set initial value
                this.setValue(this.$element.val() || this.options.value);
            },
            /*
         Replace tokens in template with <select> elements 
        */
            getTemplate: function() {
                var tpl = this.options.template;
                //first pass
                $.each(this.map, function(k, v) {
                    v = v[0];
                    var r = new RegExp(v + "+"), token = v.length > 1 ? v.substring(1, 2) : v;
                    tpl = tpl.replace(r, "{" + token + "}");
                });
                //replace spaces with &nbsp;
                tpl = tpl.replace(/ /g, "&nbsp;");
                //second pass
                $.each(this.map, function(k, v) {
                    v = v[0];
                    var token = v.length > 1 ? v.substring(1, 2) : v;
                    tpl = tpl.replace("{" + token + "}", '<select class="' + k + '"></select>');
                });
                return tpl;
            },
            /*
         Initialize combos that presents in template 
        */
            initCombos: function() {
                for (var k in this.map) {
                    var $c = this.$widget.find("." + k);
                    // set properties like this.$day, this.$month etc.
                    this["$" + k] = $c.length ? $c : null;
                    // fill with items
                    this.fillCombo(k);
                }
            },
            /*
         Fill combo with items 
        */
            fillCombo: function(k) {
                var $combo = this["$" + k];
                if (!$combo) {
                    return;
                }
                // define method name to fill items, e.g `fillDays`
                var f = "fill" + k.charAt(0).toUpperCase() + k.slice(1);
                var items = this[f]();
                var value = $combo.val();
                $combo.empty();
                for (var i = 0; i < items.length; i++) {
                    $combo.append('<option value="' + items[i][0] + '">' + items[i][1] + "</option>");
                }
                $combo.val(value);
            },
            /*
         Initialize items of combos. Handles `firstItem` option 
        */
            fillCommon: function(key) {
                var values = [], relTime;
                if (this.options.firstItem === "name") {
                    //need both to support moment ver < 2 and  >= 2
                    relTime = moment.relativeTime || moment.langData()._relativeTime;
                    var header = typeof relTime[key] === "function" ? relTime[key](1, true, key, false) : relTime[key];
                    //take last entry (see momentjs lang files structure) 
                    header = header.split(" ").reverse()[0];
                    values.push([ "", header ]);
                } else if (this.options.firstItem === "empty") {
                    values.push([ "", "" ]);
                }
                return values;
            },
            /*
        fill day
        */
            fillDay: function() {
                var items = this.fillCommon("d"), name, i, twoDigit = this.options.template.indexOf("DD") !== -1, daysCount = 31;
                // detect days count (depends on month and year)
                // originally https://github.com/vitalets/combodate/pull/7
                if (this.options.smartDays && this.$month && this.$year) {
                    var month = parseInt(this.$month.val(), 10);
                    var year = parseInt(this.$year.val(), 10);
                    if (!isNaN(month) && !isNaN(year)) {
                        daysCount = moment([ year, month ]).daysInMonth();
                    }
                }
                for (i = 1; i <= daysCount; i++) {
                    name = twoDigit ? this.leadZero(i) : i;
                    items.push([ i, name ]);
                }
                return items;
            },
            /*
        fill month
        */
            fillMonth: function() {
                var items = this.fillCommon("M"), name, i, longNames = this.options.template.indexOf("MMMM") !== -1, shortNames = this.options.template.indexOf("MMM") !== -1, twoDigit = this.options.template.indexOf("MM") !== -1;
                for (i = 0; i <= 11; i++) {
                    if (longNames) {
                        //see https://github.com/timrwood/momentjs.com/pull/36
                        name = moment().date(1).month(i).format("MMMM");
                    } else if (shortNames) {
                        name = moment().date(1).month(i).format("MMM");
                    } else if (twoDigit) {
                        name = this.leadZero(i + 1);
                    } else {
                        name = i + 1;
                    }
                    items.push([ i, name ]);
                }
                return items;
            },
            /*
        fill year
        */
            fillYear: function() {
                var items = [], name, i, longNames = this.options.template.indexOf("YYYY") !== -1;
                for (i = this.options.maxYear; i >= this.options.minYear; i--) {
                    name = longNames ? i : (i + "").substring(2);
                    items[this.options.yearDescending ? "push" : "unshift"]([ i, name ]);
                }
                items = this.fillCommon("y").concat(items);
                return items;
            },
            /*
        fill hour
        */
            fillHour: function() {
                var items = this.fillCommon("h"), name, i, h12 = this.options.template.indexOf("h") !== -1, h24 = this.options.template.indexOf("H") !== -1, twoDigit = this.options.template.toLowerCase().indexOf("hh") !== -1, min = h12 ? 1 : 0, max = h12 ? 12 : 23;
                for (i = min; i <= max; i++) {
                    name = twoDigit ? this.leadZero(i) : i;
                    items.push([ i, name ]);
                }
                return items;
            },
            /*
        fill minute
        */
            fillMinute: function() {
                var items = this.fillCommon("m"), name, i, twoDigit = this.options.template.indexOf("mm") !== -1;
                for (i = 0; i <= 59; i += this.options.minuteStep) {
                    name = twoDigit ? this.leadZero(i) : i;
                    items.push([ i, name ]);
                }
                return items;
            },
            /*
        fill second
        */
            fillSecond: function() {
                var items = this.fillCommon("s"), name, i, twoDigit = this.options.template.indexOf("ss") !== -1;
                for (i = 0; i <= 59; i += this.options.secondStep) {
                    name = twoDigit ? this.leadZero(i) : i;
                    items.push([ i, name ]);
                }
                return items;
            },
            /*
        fill ampm
        */
            fillAmpm: function() {
                var ampmL = this.options.template.indexOf("a") !== -1, ampmU = this.options.template.indexOf("A") !== -1, items = [ [ "am", ampmL ? "am" : "AM" ], [ "pm", ampmL ? "pm" : "PM" ] ];
                return items;
            },
            /*
         Returns current date value from combos. 
         If format not specified - `options.format` used.
         If format = `null` - Moment object returned.
        */
            getValue: function(format) {
                var dt, values = {}, that = this, notSelected = false;
                //getting selected values    
                $.each(this.map, function(k, v) {
                    if (k === "ampm") {
                        return;
                    }
                    var def = k === "day" ? 1 : 0;
                    values[k] = that["$" + k] ? parseInt(that["$" + k].val(), 10) : def;
                    if (isNaN(values[k])) {
                        notSelected = true;
                        return false;
                    }
                });
                //if at least one visible combo not selected - return empty string
                if (notSelected) {
                    return "";
                }
                //convert hours 12h --> 24h 
                if (this.$ampm) {
                    //12:00 pm --> 12:00 (24-h format, midday), 12:00 am --> 00:00 (24-h format, midnight, start of day)
                    if (values.hour === 12) {
                        values.hour = this.$ampm.val() === "am" ? 0 : 12;
                    } else {
                        values.hour = this.$ampm.val() === "am" ? values.hour : values.hour + 12;
                    }
                }
                dt = moment([ values.year, values.month, values.day, values.hour, values.minute, values.second ]);
                //highlight invalid date
                this.highlight(dt);
                format = format === undefined ? this.options.format : format;
                if (format === null) {
                    return dt.isValid() ? dt : null;
                } else {
                    return dt.isValid() ? dt.format(format) : "";
                }
            },
            setValue: function(value) {
                if (!value) {
                    return;
                }
                var dt = typeof value === "string" ? moment(value, this.options.format) : moment(value), that = this, values = {};
                //function to find nearest value in select options
                function getNearest($select, value) {
                    var delta = {};
                    $select.children("option").each(function(i, opt) {
                        var optValue = $(opt).attr("value"), distance;
                        if (optValue === "") return;
                        distance = Math.abs(optValue - value);
                        if (typeof delta.distance === "undefined" || distance < delta.distance) {
                            delta = {
                                value: optValue,
                                distance: distance
                            };
                        }
                    });
                    return delta.value;
                }
                if (dt.isValid()) {
                    //read values from date object
                    $.each(this.map, function(k, v) {
                        if (k === "ampm") {
                            return;
                        }
                        values[k] = dt[v[1]]();
                    });
                    if (this.$ampm) {
                        //12:00 pm --> 12:00 (24-h format, midday), 12:00 am --> 00:00 (24-h format, midnight, start of day)
                        if (values.hour >= 12) {
                            values.ampm = "pm";
                            if (values.hour > 12) {
                                values.hour -= 12;
                            }
                        } else {
                            values.ampm = "am";
                            if (values.hour === 0) {
                                values.hour = 12;
                            }
                        }
                    }
                    $.each(values, function(k, v) {
                        //call val() for each existing combo, e.g. this.$hour.val()
                        if (that["$" + k]) {
                            if (k === "minute" && that.options.minuteStep > 1 && that.options.roundTime) {
                                v = getNearest(that["$" + k], v);
                            }
                            if (k === "second" && that.options.secondStep > 1 && that.options.roundTime) {
                                v = getNearest(that["$" + k], v);
                            }
                            that["$" + k].val(v);
                        }
                    });
                    // update days count
                    if (this.options.smartDays) {
                        this.fillCombo("day");
                    }
                    this.$element.val(dt.format(this.options.format)).change();
                }
            },
            /*
         highlight combos if date is invalid
        */
            highlight: function(dt) {
                if (!dt.isValid()) {
                    if (this.options.errorClass) {
                        this.$widget.addClass(this.options.errorClass);
                    } else {
                        //store original border color
                        if (!this.borderColor) {
                            this.borderColor = this.$widget.find("select").css("border-color");
                        }
                        this.$widget.find("select").css("border-color", "red");
                    }
                } else {
                    if (this.options.errorClass) {
                        this.$widget.removeClass(this.options.errorClass);
                    } else {
                        this.$widget.find("select").css("border-color", this.borderColor);
                    }
                }
            },
            leadZero: function(v) {
                return v <= 9 ? "0" + v : v;
            },
            destroy: function() {
                this.$widget.remove();
                this.$element.removeData("combodate").show();
            }
        };
        $.fn.combodate = function(option) {
            var d, args = Array.apply(null, arguments);
            args.shift();
            //getValue returns date as string / object (not jQuery object)
            if (option === "getValue" && this.length && (d = this.eq(0).data("combodate"))) {
                return d.getValue.apply(d, args);
            }
            return this.each(function() {
                var $this = $(this), data = $this.data("combodate"), options = typeof option == "object" && option;
                if (!data) {
                    $this.data("combodate", data = new Combodate(this, options));
                }
                if (typeof option == "string" && typeof data[option] == "function") {
                    data[option].apply(data, args);
                }
            });
        };
        $.fn.combodate.defaults = {
            //in this format value stored in original input
            format: "DD-MM-YYYY HH:mm",
            //in this format items in dropdowns are displayed
            template: "D / MMM / YYYY   H : mm",
            //initial value, can be `new Date()`    
            value: null,
            minYear: 1970,
            maxYear: 2015,
            yearDescending: true,
            minuteStep: 5,
            secondStep: 1,
            firstItem: "empty",
            //'name', 'empty', 'none'
            errorClass: null,
            roundTime: true,
            // whether to round minutes and seconds if step > 1
            smartDays: false
        };
    })(window.jQuery);
    /**
Combodate input - dropdown date and time picker.    
Based on [combodate](http://vitalets.github.com/combodate) plugin (included). To use it you should manually include [momentjs](http://momentjs.com).

    <script src="js/moment.min.js"></script>
   
Allows to input:

* only date
* only time 
* both date and time  

Please note, that format is taken from momentjs and **not compatible** with bootstrap-datepicker / jquery UI datepicker.  
Internally value stored as `momentjs` object. 

@class combodate
@extends abstractinput
@final
@since 1.4.0
@example
<a href="#" id="dob" data-type="combodate" data-pk="1" data-url="/post" data-value="1984-05-15" data-title="Select date"></a>
<script>
$(function(){
    $('#dob').editable({
        format: 'YYYY-MM-DD',    
        viewformat: 'DD.MM.YYYY',    
        template: 'D / MMMM / YYYY',    
        combodate: {
                minYear: 2000,
                maxYear: 2015,
                minuteStep: 1
           }
        }
    });
});
</script>
**/
    /*global moment*/
    (function($) {
        "use strict";
        var Constructor = function(options) {
            this.init("combodate", options, Constructor.defaults);
            //by default viewformat equals to format
            if (!this.options.viewformat) {
                this.options.viewformat = this.options.format;
            }
            //try parse combodate config defined as json string in data-combodate
            options.combodate = $.fn.editableutils.tryParseJson(options.combodate, true);
            //overriding combodate config (as by default jQuery extend() is not recursive)
            this.options.combodate = $.extend({}, Constructor.defaults.combodate, options.combodate, {
                format: this.options.format,
                template: this.options.template
            });
        };
        $.fn.editableutils.inherit(Constructor, $.fn.editabletypes.abstractinput);
        $.extend(Constructor.prototype, {
            render: function() {
                this.$input.combodate(this.options.combodate);
                if ($.fn.editableform.engine === "bs3") {
                    this.$input.siblings().find("select").addClass("form-control");
                }
                if (this.options.inputclass) {
                    this.$input.siblings().find("select").addClass(this.options.inputclass);
                }
            },
            value2html: function(value, element) {
                var text = value ? value.format(this.options.viewformat) : "";
                //$(element).text(text);
                Constructor.superclass.value2html.call(this, text, element);
            },
            html2value: function(html) {
                return html ? moment(html, this.options.viewformat) : null;
            },
            value2str: function(value) {
                return value ? value.format(this.options.format) : "";
            },
            str2value: function(str) {
                return str ? moment(str, this.options.format) : null;
            },
            value2submit: function(value) {
                return this.value2str(value);
            },
            value2input: function(value) {
                this.$input.combodate("setValue", value);
            },
            input2value: function() {
                return this.$input.combodate("getValue", null);
            },
            activate: function() {
                this.$input.siblings(".combodate").find("select").eq(0).focus();
            },
            /*
       clear:  function() {
          this.$input.data('datepicker').date = null;
          this.$input.find('.active').removeClass('active');
       },
       */
            autosubmit: function() {}
        });
        Constructor.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
            /**
        @property tpl 
        @default <input type="text">
        **/
            tpl: '<input type="text">',
            /**
        @property inputclass 
        @default null
        **/
            inputclass: null,
            /**
        Format used for sending value to server. Also applied when converting date from <code>data-value</code> attribute.<br>
        See list of tokens in [momentjs docs](http://momentjs.com/docs/#/parsing/string-format)  
        
        @property format 
        @type string
        @default YYYY-MM-DD
        **/
            format: "YYYY-MM-DD",
            /**
        Format used for displaying date. Also applied when converting date from element's text on init.   
        If not specified equals to `format`.
        
        @property viewformat 
        @type string
        @default null
        **/
            viewformat: null,
            /**
        Template used for displaying dropdowns.
        
        @property template 
        @type string
        @default D / MMM / YYYY
        **/
            template: "D / MMM / YYYY",
            /**
        Configuration of combodate.
        Full list of options: http://vitalets.github.com/combodate/#docs
        
        @property combodate 
        @type object
        @default null
        **/
            combodate: null
        });
        $.fn.editabletypes.combodate = Constructor;
    })(window.jQuery);
    /*
Editableform based on Twitter Bootstrap 3
*/
    (function($) {
        "use strict";
        //store parent methods
        var pInitInput = $.fn.editableform.Constructor.prototype.initInput;
        $.extend($.fn.editableform.Constructor.prototype, {
            initTemplate: function() {
                this.$form = $($.fn.editableform.template);
                this.$form.find(".control-group").addClass("form-group");
                this.$form.find(".editable-error-block").addClass("help-block");
            },
            initInput: function() {
                pInitInput.apply(this);
                //for bs3 set default class `input-sm` to standard inputs
                var emptyInputClass = this.input.options.inputclass === null || this.input.options.inputclass === false;
                var defaultClass = "input-sm";
                //bs3 add `form-control` class to standard inputs
                var stdtypes = "text,select,textarea,password,email,url,tel,number,range,time,typeaheadjs".split(",");
                if (~$.inArray(this.input.type, stdtypes)) {
                    this.input.$input.addClass("form-control");
                    if (emptyInputClass) {
                        this.input.options.inputclass = defaultClass;
                        this.input.$input.addClass(defaultClass);
                    }
                }
                //apply bs3 size class also to buttons (to fit size of control)
                var $btn = this.$form.find(".editable-buttons");
                var classes = emptyInputClass ? [ defaultClass ] : this.input.options.inputclass.split(" ");
                for (var i = 0; i < classes.length; i++) {
                    // `btn-sm` is default now
                    /*
                if(classes[i].toLowerCase() === 'input-sm') { 
                    $btn.find('button').addClass('btn-sm');  
                }
                */
                    if (classes[i].toLowerCase() === "input-lg") {
                        $btn.find("button").removeClass("btn-sm").addClass("btn-lg");
                    }
                }
            }
        });
        //buttons
        $.fn.editableform.buttons = '<button type="submit" class="btn btn-primary btn-sm editable-submit">' + '<i class="glyphicon glyphicon-ok"></i>' + "</button>" + '<button type="button" class="btn btn-default btn-sm editable-cancel">' + '<i class="glyphicon glyphicon-remove"></i>' + "</button>";
        //error classes
        $.fn.editableform.errorGroupClass = "has-error";
        $.fn.editableform.errorBlockClass = null;
        //engine
        $.fn.editableform.engine = "bs3";
    })(window.jQuery);
    /**
* Editable Popover3 (for Bootstrap 3) 
* ---------------------
* requires bootstrap-popover.js
*/
    (function($) {
        "use strict";
        //extend methods
        $.extend($.fn.editableContainer.Popup.prototype, {
            containerName: "popover",
            containerDataName: "bs.popover",
            innerCss: ".popover-content",
            defaults: $.fn.popover.Constructor.DEFAULTS,
            initContainer: function() {
                $.extend(this.containerOptions, {
                    trigger: "manual",
                    selector: false,
                    content: " ",
                    template: this.defaults.template
                });
                //as template property is used in inputs, hide it from popover
                var t;
                if (this.$element.data("template")) {
                    t = this.$element.data("template");
                    this.$element.removeData("template");
                }
                this.call(this.containerOptions);
                if (t) {
                    //restore data('template')
                    this.$element.data("template", t);
                }
            },
            /* show */
            innerShow: function() {
                this.call("show");
            },
            /* hide */
            innerHide: function() {
                this.call("hide");
            },
            /* destroy */
            innerDestroy: function() {
                this.call("destroy");
            },
            setContainerOption: function(key, value) {
                this.container().options[key] = value;
            },
            /**
        * move popover to new position. This function mainly copied from bootstrap-popover.
        */
            /*jshint laxcomma: true, eqeqeq: false*/
            setPosition: function() {
                (function() {
                    /*    
                var $tip = this.tip()
                , inside
                , pos
                , actualWidth
                , actualHeight
                , placement
                , tp
                , tpt
                , tpb
                , tpl
                , tpr;

                placement = typeof this.options.placement === 'function' ?
                this.options.placement.call(this, $tip[0], this.$element[0]) :
                this.options.placement;

                inside = /in/.test(placement);
               
                $tip
              //  .detach()
              //vitalets: remove any placement class because otherwise they dont influence on re-positioning of visible popover
                .removeClass('top right bottom left')
                .css({ top: 0, left: 0, display: 'block' });
              //  .insertAfter(this.$element);
               
                pos = this.getPosition(inside);

                actualWidth = $tip[0].offsetWidth;
                actualHeight = $tip[0].offsetHeight;

                placement = inside ? placement.split(' ')[1] : placement;

                tpb = {top: pos.top + pos.height, left: pos.left + pos.width / 2 - actualWidth / 2};
                tpt = {top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2};
                tpl = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth};
                tpr = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width};

                switch (placement) {
                    case 'bottom':
                        if ((tpb.top + actualHeight) > ($(window).scrollTop() + $(window).height())) {
                            if (tpt.top > $(window).scrollTop()) {
                                placement = 'top';
                            } else if ((tpr.left + actualWidth) < ($(window).scrollLeft() + $(window).width())) {
                                placement = 'right';
                            } else if (tpl.left > $(window).scrollLeft()) {
                                placement = 'left';
                            } else {
                                placement = 'right';
                            }
                        }
                        break;
                    case 'top':
                        if (tpt.top < $(window).scrollTop()) {
                            if ((tpb.top + actualHeight) < ($(window).scrollTop() + $(window).height())) {
                                placement = 'bottom';
                            } else if ((tpr.left + actualWidth) < ($(window).scrollLeft() + $(window).width())) {
                                placement = 'right';
                            } else if (tpl.left > $(window).scrollLeft()) {
                                placement = 'left';
                            } else {
                                placement = 'right';
                            }
                        }
                        break;
                    case 'left':
                        if (tpl.left < $(window).scrollLeft()) {
                            if ((tpr.left + actualWidth) < ($(window).scrollLeft() + $(window).width())) {
                                placement = 'right';
                            } else if (tpt.top > $(window).scrollTop()) {
                                placement = 'top';
                            } else if (tpt.top > $(window).scrollTop()) {
                                placement = 'bottom';
                            } else {
                                placement = 'right';
                            }
                        }
                        break;
                    case 'right':
                        if ((tpr.left + actualWidth) > ($(window).scrollLeft() + $(window).width())) {
                            if (tpl.left > $(window).scrollLeft()) {
                                placement = 'left';
                            } else if (tpt.top > $(window).scrollTop()) {
                                placement = 'top';
                            } else if (tpt.top > $(window).scrollTop()) {
                                placement = 'bottom';
                            }
                        }
                        break;
                }

                switch (placement) {
                    case 'bottom':
                        tp = tpb;
                        break;
                    case 'top':
                        tp = tpt;
                        break;
                    case 'left':
                        tp = tpl;
                        break;
                    case 'right':
                        tp = tpr;
                        break;
                }

                $tip
                .offset(tp)
                .addClass(placement)
                .addClass('in');
           */
                    var $tip = this.tip();
                    var placement = typeof this.options.placement == "function" ? this.options.placement.call(this, $tip[0], this.$element[0]) : this.options.placement;
                    var autoToken = /\s?auto?\s?/i;
                    var autoPlace = autoToken.test(placement);
                    if (autoPlace) {
                        placement = placement.replace(autoToken, "") || "top";
                    }
                    var pos = this.getPosition();
                    var actualWidth = $tip[0].offsetWidth;
                    var actualHeight = $tip[0].offsetHeight;
                    if (autoPlace) {
                        var $parent = this.$element.parent();
                        var orgPlacement = placement;
                        var docScroll = document.documentElement.scrollTop || document.body.scrollTop;
                        var parentWidth = this.options.container == "body" ? window.innerWidth : $parent.outerWidth();
                        var parentHeight = this.options.container == "body" ? window.innerHeight : $parent.outerHeight();
                        var parentLeft = this.options.container == "body" ? 0 : $parent.offset().left;
                        placement = placement == "bottom" && pos.top + pos.height + actualHeight - docScroll > parentHeight ? "top" : placement == "top" && pos.top - docScroll - actualHeight < 0 ? "bottom" : placement == "right" && pos.right + actualWidth > parentWidth ? "left" : placement == "left" && pos.left - actualWidth < parentLeft ? "right" : placement;
                        $tip.removeClass(orgPlacement).addClass(placement);
                    }
                    var calculatedOffset = this.getCalculatedOffset(placement, pos, actualWidth, actualHeight);
                    this.applyPlacement(calculatedOffset, placement);
                }).call(this.container());
            }
        });
    })(window.jQuery);
    /* =========================================================
 * bootstrap-datepicker.js
 * http://www.eyecon.ro/bootstrap-datepicker
 * =========================================================
 * Copyright 2012 Stefan Petre
 * Improvements by Andrew Rowls
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================= */
    (function($) {
        function UTCDate() {
            return new Date(Date.UTC.apply(Date, arguments));
        }
        function UTCToday() {
            var today = new Date();
            return UTCDate(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate());
        }
        // Picker object
        var Datepicker = function(element, options) {
            var that = this;
            this._process_options(options);
            this.element = $(element);
            this.isInline = false;
            this.isInput = this.element.is("input");
            this.component = this.element.is(".date") ? this.element.find(".add-on, .btn") : false;
            this.hasInput = this.component && this.element.find("input").length;
            if (this.component && this.component.length === 0) this.component = false;
            this.picker = $(DPGlobal.template);
            this._buildEvents();
            this._attachEvents();
            if (this.isInline) {
                this.picker.addClass("datepicker-inline").appendTo(this.element);
            } else {
                this.picker.addClass("datepicker-dropdown dropdown-menu");
            }
            if (this.o.rtl) {
                this.picker.addClass("datepicker-rtl");
                this.picker.find(".prev i, .next i").toggleClass("icon-arrow-left icon-arrow-right");
            }
            this.viewMode = this.o.startView;
            if (this.o.calendarWeeks) this.picker.find("tfoot th.today").attr("colspan", function(i, val) {
                return parseInt(val) + 1;
            });
            this._allow_update = false;
            this.setStartDate(this.o.startDate);
            this.setEndDate(this.o.endDate);
            this.setDaysOfWeekDisabled(this.o.daysOfWeekDisabled);
            this.fillDow();
            this.fillMonths();
            this._allow_update = true;
            this.update();
            this.showMode();
            if (this.isInline) {
                this.show();
            }
        };
        Datepicker.prototype = {
            constructor: Datepicker,
            _process_options: function(opts) {
                // Store raw options for reference
                this._o = $.extend({}, this._o, opts);
                // Processed options
                var o = this.o = $.extend({}, this._o);
                // Check if "de-DE" style date is available, if not language should
                // fallback to 2 letter code eg "de"
                var lang = o.language;
                if (!dates[lang]) {
                    lang = lang.split("-")[0];
                    if (!dates[lang]) lang = defaults.language;
                }
                o.language = lang;
                switch (o.startView) {
                  case 2:
                  case "decade":
                    o.startView = 2;
                    break;

                  case 1:
                  case "year":
                    o.startView = 1;
                    break;

                  default:
                    o.startView = 0;
                }
                switch (o.minViewMode) {
                  case 1:
                  case "months":
                    o.minViewMode = 1;
                    break;

                  case 2:
                  case "years":
                    o.minViewMode = 2;
                    break;

                  default:
                    o.minViewMode = 0;
                }
                o.startView = Math.max(o.startView, o.minViewMode);
                o.weekStart %= 7;
                o.weekEnd = (o.weekStart + 6) % 7;
                var format = DPGlobal.parseFormat(o.format);
                if (o.startDate !== -Infinity) {
                    o.startDate = DPGlobal.parseDate(o.startDate, format, o.language);
                }
                if (o.endDate !== Infinity) {
                    o.endDate = DPGlobal.parseDate(o.endDate, format, o.language);
                }
                o.daysOfWeekDisabled = o.daysOfWeekDisabled || [];
                if (!$.isArray(o.daysOfWeekDisabled)) o.daysOfWeekDisabled = o.daysOfWeekDisabled.split(/[,\s]*/);
                o.daysOfWeekDisabled = $.map(o.daysOfWeekDisabled, function(d) {
                    return parseInt(d, 10);
                });
            },
            _events: [],
            _secondaryEvents: [],
            _applyEvents: function(evs) {
                for (var i = 0, el, ev; i < evs.length; i++) {
                    el = evs[i][0];
                    ev = evs[i][1];
                    el.on(ev);
                }
            },
            _unapplyEvents: function(evs) {
                for (var i = 0, el, ev; i < evs.length; i++) {
                    el = evs[i][0];
                    ev = evs[i][1];
                    el.off(ev);
                }
            },
            _buildEvents: function() {
                if (this.isInput) {
                    // single input
                    this._events = [ [ this.element, {
                        focus: $.proxy(this.show, this),
                        keyup: $.proxy(this.update, this),
                        keydown: $.proxy(this.keydown, this)
                    } ] ];
                } else if (this.component && this.hasInput) {
                    // component: input + button
                    this._events = [ // For components that are not readonly, allow keyboard nav
                    [ this.element.find("input"), {
                        focus: $.proxy(this.show, this),
                        keyup: $.proxy(this.update, this),
                        keydown: $.proxy(this.keydown, this)
                    } ], [ this.component, {
                        click: $.proxy(this.show, this)
                    } ] ];
                } else if (this.element.is("div")) {
                    // inline datepicker
                    this.isInline = true;
                } else {
                    this._events = [ [ this.element, {
                        click: $.proxy(this.show, this)
                    } ] ];
                }
                this._secondaryEvents = [ [ this.picker, {
                    click: $.proxy(this.click, this)
                } ], [ $(window), {
                    resize: $.proxy(this.place, this)
                } ], [ $(document), {
                    mousedown: $.proxy(function(e) {
                        // Clicked outside the datepicker, hide it
                        if (!(this.element.is(e.target) || this.element.find(e.target).size() || this.picker.is(e.target) || this.picker.find(e.target).size())) {
                            this.hide();
                        }
                    }, this)
                } ] ];
            },
            _attachEvents: function() {
                this._detachEvents();
                this._applyEvents(this._events);
            },
            _detachEvents: function() {
                this._unapplyEvents(this._events);
            },
            _attachSecondaryEvents: function() {
                this._detachSecondaryEvents();
                this._applyEvents(this._secondaryEvents);
            },
            _detachSecondaryEvents: function() {
                this._unapplyEvents(this._secondaryEvents);
            },
            _trigger: function(event, altdate) {
                var date = altdate || this.date, local_date = new Date(date.getTime() + date.getTimezoneOffset() * 6e4);
                this.element.trigger({
                    type: event,
                    date: local_date,
                    format: $.proxy(function(altformat) {
                        var format = altformat || this.o.format;
                        return DPGlobal.formatDate(date, format, this.o.language);
                    }, this)
                });
            },
            show: function(e) {
                if (!this.isInline) this.picker.appendTo("body");
                this.picker.show();
                this.height = this.component ? this.component.outerHeight() : this.element.outerHeight();
                this.place();
                this._attachSecondaryEvents();
                if (e) {
                    e.preventDefault();
                }
                this._trigger("show");
            },
            hide: function(e) {
                if (this.isInline) return;
                if (!this.picker.is(":visible")) return;
                this.picker.hide().detach();
                this._detachSecondaryEvents();
                this.viewMode = this.o.startView;
                this.showMode();
                if (this.o.forceParse && (this.isInput && this.element.val() || this.hasInput && this.element.find("input").val())) this.setValue();
                this._trigger("hide");
            },
            remove: function() {
                this.hide();
                this._detachEvents();
                this._detachSecondaryEvents();
                this.picker.remove();
                delete this.element.data().datepicker;
                if (!this.isInput) {
                    delete this.element.data().date;
                }
            },
            getDate: function() {
                var d = this.getUTCDate();
                return new Date(d.getTime() + d.getTimezoneOffset() * 6e4);
            },
            getUTCDate: function() {
                return this.date;
            },
            setDate: function(d) {
                this.setUTCDate(new Date(d.getTime() - d.getTimezoneOffset() * 6e4));
            },
            setUTCDate: function(d) {
                this.date = d;
                this.setValue();
            },
            setValue: function() {
                var formatted = this.getFormattedDate();
                if (!this.isInput) {
                    if (this.component) {
                        this.element.find("input").val(formatted);
                    }
                } else {
                    this.element.val(formatted);
                }
            },
            getFormattedDate: function(format) {
                if (format === undefined) format = this.o.format;
                return DPGlobal.formatDate(this.date, format, this.o.language);
            },
            setStartDate: function(startDate) {
                this._process_options({
                    startDate: startDate
                });
                this.update();
                this.updateNavArrows();
            },
            setEndDate: function(endDate) {
                this._process_options({
                    endDate: endDate
                });
                this.update();
                this.updateNavArrows();
            },
            setDaysOfWeekDisabled: function(daysOfWeekDisabled) {
                this._process_options({
                    daysOfWeekDisabled: daysOfWeekDisabled
                });
                this.update();
                this.updateNavArrows();
            },
            place: function() {
                if (this.isInline) return;
                var zIndex = parseInt(this.element.parents().filter(function() {
                    return $(this).css("z-index") != "auto";
                }).first().css("z-index")) + 10;
                var offset = this.component ? this.component.parent().offset() : this.element.offset();
                var height = this.component ? this.component.outerHeight(true) : this.element.outerHeight(true);
                this.picker.css({
                    top: offset.top + height,
                    left: offset.left,
                    zIndex: zIndex
                });
            },
            _allow_update: true,
            update: function() {
                if (!this._allow_update) return;
                var date, fromArgs = false;
                if (arguments && arguments.length && (typeof arguments[0] === "string" || arguments[0] instanceof Date)) {
                    date = arguments[0];
                    fromArgs = true;
                } else {
                    date = this.isInput ? this.element.val() : this.element.data("date") || this.element.find("input").val();
                    delete this.element.data().date;
                }
                this.date = DPGlobal.parseDate(date, this.o.format, this.o.language);
                if (fromArgs) this.setValue();
                if (this.date < this.o.startDate) {
                    this.viewDate = new Date(this.o.startDate);
                } else if (this.date > this.o.endDate) {
                    this.viewDate = new Date(this.o.endDate);
                } else {
                    this.viewDate = new Date(this.date);
                }
                this.fill();
            },
            fillDow: function() {
                var dowCnt = this.o.weekStart, html = "<tr>";
                if (this.o.calendarWeeks) {
                    var cell = '<th class="cw">&nbsp;</th>';
                    html += cell;
                    this.picker.find(".datepicker-days thead tr:first-child").prepend(cell);
                }
                while (dowCnt < this.o.weekStart + 7) {
                    html += '<th class="dow">' + dates[this.o.language].daysMin[dowCnt++ % 7] + "</th>";
                }
                html += "</tr>";
                this.picker.find(".datepicker-days thead").append(html);
            },
            fillMonths: function() {
                var html = "", i = 0;
                while (i < 12) {
                    html += '<span class="month">' + dates[this.o.language].monthsShort[i++] + "</span>";
                }
                this.picker.find(".datepicker-months td").html(html);
            },
            setRange: function(range) {
                if (!range || !range.length) delete this.range; else this.range = $.map(range, function(d) {
                    return d.valueOf();
                });
                this.fill();
            },
            getClassNames: function(date) {
                var cls = [], year = this.viewDate.getUTCFullYear(), month = this.viewDate.getUTCMonth(), currentDate = this.date.valueOf(), today = new Date();
                if (date.getUTCFullYear() < year || date.getUTCFullYear() == year && date.getUTCMonth() < month) {
                    cls.push("old");
                } else if (date.getUTCFullYear() > year || date.getUTCFullYear() == year && date.getUTCMonth() > month) {
                    cls.push("new");
                }
                // Compare internal UTC date with local today, not UTC today
                if (this.o.todayHighlight && date.getUTCFullYear() == today.getFullYear() && date.getUTCMonth() == today.getMonth() && date.getUTCDate() == today.getDate()) {
                    cls.push("today");
                }
                if (currentDate && date.valueOf() == currentDate) {
                    cls.push("active");
                }
                if (date.valueOf() < this.o.startDate || date.valueOf() > this.o.endDate || $.inArray(date.getUTCDay(), this.o.daysOfWeekDisabled) !== -1) {
                    cls.push("disabled");
                }
                if (this.range) {
                    if (date > this.range[0] && date < this.range[this.range.length - 1]) {
                        cls.push("range");
                    }
                    if ($.inArray(date.valueOf(), this.range) != -1) {
                        cls.push("selected");
                    }
                }
                return cls;
            },
            fill: function() {
                var d = new Date(this.viewDate), year = d.getUTCFullYear(), month = d.getUTCMonth(), startYear = this.o.startDate !== -Infinity ? this.o.startDate.getUTCFullYear() : -Infinity, startMonth = this.o.startDate !== -Infinity ? this.o.startDate.getUTCMonth() : -Infinity, endYear = this.o.endDate !== Infinity ? this.o.endDate.getUTCFullYear() : Infinity, endMonth = this.o.endDate !== Infinity ? this.o.endDate.getUTCMonth() : Infinity, currentDate = this.date && this.date.valueOf(), tooltip;
                this.picker.find(".datepicker-days thead th.datepicker-switch").text(dates[this.o.language].months[month] + " " + year);
                this.picker.find("tfoot th.today").text(dates[this.o.language].today).toggle(this.o.todayBtn !== false);
                this.picker.find("tfoot th.clear").text(dates[this.o.language].clear).toggle(this.o.clearBtn !== false);
                this.updateNavArrows();
                this.fillMonths();
                var prevMonth = UTCDate(year, month - 1, 28, 0, 0, 0, 0), day = DPGlobal.getDaysInMonth(prevMonth.getUTCFullYear(), prevMonth.getUTCMonth());
                prevMonth.setUTCDate(day);
                prevMonth.setUTCDate(day - (prevMonth.getUTCDay() - this.o.weekStart + 7) % 7);
                var nextMonth = new Date(prevMonth);
                nextMonth.setUTCDate(nextMonth.getUTCDate() + 42);
                nextMonth = nextMonth.valueOf();
                var html = [];
                var clsName;
                while (prevMonth.valueOf() < nextMonth) {
                    if (prevMonth.getUTCDay() == this.o.weekStart) {
                        html.push("<tr>");
                        if (this.o.calendarWeeks) {
                            // ISO 8601: First week contains first thursday.
                            // ISO also states week starts on Monday, but we can be more abstract here.
                            var // Start of current week: based on weekstart/current date
                            ws = new Date(+prevMonth + (this.o.weekStart - prevMonth.getUTCDay() - 7) % 7 * 864e5), // Thursday of this week
                            th = new Date(+ws + (7 + 4 - ws.getUTCDay()) % 7 * 864e5), // First Thursday of year, year from thursday
                            yth = new Date(+(yth = UTCDate(th.getUTCFullYear(), 0, 1)) + (7 + 4 - yth.getUTCDay()) % 7 * 864e5), // Calendar week: ms between thursdays, div ms per day, div 7 days
                            calWeek = (th - yth) / 864e5 / 7 + 1;
                            html.push('<td class="cw">' + calWeek + "</td>");
                        }
                    }
                    clsName = this.getClassNames(prevMonth);
                    clsName.push("day");
                    var before = this.o.beforeShowDay(prevMonth);
                    if (before === undefined) before = {}; else if (typeof before === "boolean") before = {
                        enabled: before
                    }; else if (typeof before === "string") before = {
                        classes: before
                    };
                    if (before.enabled === false) clsName.push("disabled");
                    if (before.classes) clsName = clsName.concat(before.classes.split(/\s+/));
                    if (before.tooltip) tooltip = before.tooltip;
                    clsName = $.unique(clsName);
                    html.push('<td class="' + clsName.join(" ") + '"' + (tooltip ? ' title="' + tooltip + '"' : "") + ">" + prevMonth.getUTCDate() + "</td>");
                    if (prevMonth.getUTCDay() == this.o.weekEnd) {
                        html.push("</tr>");
                    }
                    prevMonth.setUTCDate(prevMonth.getUTCDate() + 1);
                }
                this.picker.find(".datepicker-days tbody").empty().append(html.join(""));
                var currentYear = this.date && this.date.getUTCFullYear();
                var months = this.picker.find(".datepicker-months").find("th:eq(1)").text(year).end().find("span").removeClass("active");
                if (currentYear && currentYear == year) {
                    months.eq(this.date.getUTCMonth()).addClass("active");
                }
                if (year < startYear || year > endYear) {
                    months.addClass("disabled");
                }
                if (year == startYear) {
                    months.slice(0, startMonth).addClass("disabled");
                }
                if (year == endYear) {
                    months.slice(endMonth + 1).addClass("disabled");
                }
                html = "";
                year = parseInt(year / 10, 10) * 10;
                var yearCont = this.picker.find(".datepicker-years").find("th:eq(1)").text(year + "-" + (year + 9)).end().find("td");
                year -= 1;
                for (var i = -1; i < 11; i++) {
                    html += '<span class="year' + (i == -1 ? " old" : i == 10 ? " new" : "") + (currentYear == year ? " active" : "") + (year < startYear || year > endYear ? " disabled" : "") + '">' + year + "</span>";
                    year += 1;
                }
                yearCont.html(html);
            },
            updateNavArrows: function() {
                if (!this._allow_update) return;
                var d = new Date(this.viewDate), year = d.getUTCFullYear(), month = d.getUTCMonth();
                switch (this.viewMode) {
                  case 0:
                    if (this.o.startDate !== -Infinity && year <= this.o.startDate.getUTCFullYear() && month <= this.o.startDate.getUTCMonth()) {
                        this.picker.find(".prev").css({
                            visibility: "hidden"
                        });
                    } else {
                        this.picker.find(".prev").css({
                            visibility: "visible"
                        });
                    }
                    if (this.o.endDate !== Infinity && year >= this.o.endDate.getUTCFullYear() && month >= this.o.endDate.getUTCMonth()) {
                        this.picker.find(".next").css({
                            visibility: "hidden"
                        });
                    } else {
                        this.picker.find(".next").css({
                            visibility: "visible"
                        });
                    }
                    break;

                  case 1:
                  case 2:
                    if (this.o.startDate !== -Infinity && year <= this.o.startDate.getUTCFullYear()) {
                        this.picker.find(".prev").css({
                            visibility: "hidden"
                        });
                    } else {
                        this.picker.find(".prev").css({
                            visibility: "visible"
                        });
                    }
                    if (this.o.endDate !== Infinity && year >= this.o.endDate.getUTCFullYear()) {
                        this.picker.find(".next").css({
                            visibility: "hidden"
                        });
                    } else {
                        this.picker.find(".next").css({
                            visibility: "visible"
                        });
                    }
                    break;
                }
            },
            click: function(e) {
                e.preventDefault();
                var target = $(e.target).closest("span, td, th");
                if (target.length == 1) {
                    switch (target[0].nodeName.toLowerCase()) {
                      case "th":
                        switch (target[0].className) {
                          case "datepicker-switch":
                            this.showMode(1);
                            break;

                          case "prev":
                          case "next":
                            var dir = DPGlobal.modes[this.viewMode].navStep * (target[0].className == "prev" ? -1 : 1);
                            switch (this.viewMode) {
                              case 0:
                                this.viewDate = this.moveMonth(this.viewDate, dir);
                                break;

                              case 1:
                              case 2:
                                this.viewDate = this.moveYear(this.viewDate, dir);
                                break;
                            }
                            this.fill();
                            break;

                          case "today":
                            var date = new Date();
                            date = UTCDate(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0);
                            this.showMode(-2);
                            var which = this.o.todayBtn == "linked" ? null : "view";
                            this._setDate(date, which);
                            break;

                          case "clear":
                            var element;
                            if (this.isInput) element = this.element; else if (this.component) element = this.element.find("input");
                            if (element) element.val("").change();
                            this._trigger("changeDate");
                            this.update();
                            if (this.o.autoclose) this.hide();
                            break;
                        }
                        break;

                      case "span":
                        if (!target.is(".disabled")) {
                            this.viewDate.setUTCDate(1);
                            if (target.is(".month")) {
                                var day = 1;
                                var month = target.parent().find("span").index(target);
                                var year = this.viewDate.getUTCFullYear();
                                this.viewDate.setUTCMonth(month);
                                this._trigger("changeMonth", this.viewDate);
                                if (this.o.minViewMode === 1) {
                                    this._setDate(UTCDate(year, month, day, 0, 0, 0, 0));
                                }
                            } else {
                                var year = parseInt(target.text(), 10) || 0;
                                var day = 1;
                                var month = 0;
                                this.viewDate.setUTCFullYear(year);
                                this._trigger("changeYear", this.viewDate);
                                if (this.o.minViewMode === 2) {
                                    this._setDate(UTCDate(year, month, day, 0, 0, 0, 0));
                                }
                            }
                            this.showMode(-1);
                            this.fill();
                        }
                        break;

                      case "td":
                        if (target.is(".day") && !target.is(".disabled")) {
                            var day = parseInt(target.text(), 10) || 1;
                            var year = this.viewDate.getUTCFullYear(), month = this.viewDate.getUTCMonth();
                            if (target.is(".old")) {
                                if (month === 0) {
                                    month = 11;
                                    year -= 1;
                                } else {
                                    month -= 1;
                                }
                            } else if (target.is(".new")) {
                                if (month == 11) {
                                    month = 0;
                                    year += 1;
                                } else {
                                    month += 1;
                                }
                            }
                            this._setDate(UTCDate(year, month, day, 0, 0, 0, 0));
                        }
                        break;
                    }
                }
            },
            _setDate: function(date, which) {
                if (!which || which == "date") this.date = new Date(date);
                if (!which || which == "view") this.viewDate = new Date(date);
                this.fill();
                this.setValue();
                this._trigger("changeDate");
                var element;
                if (this.isInput) {
                    element = this.element;
                } else if (this.component) {
                    element = this.element.find("input");
                }
                if (element) {
                    element.change();
                    if (this.o.autoclose && (!which || which == "date")) {
                        this.hide();
                    }
                }
            },
            moveMonth: function(date, dir) {
                if (!dir) return date;
                var new_date = new Date(date.valueOf()), day = new_date.getUTCDate(), month = new_date.getUTCMonth(), mag = Math.abs(dir), new_month, test;
                dir = dir > 0 ? 1 : -1;
                if (mag == 1) {
                    test = dir == -1 ? function() {
                        return new_date.getUTCMonth() == month;
                    } : function() {
                        return new_date.getUTCMonth() != new_month;
                    };
                    new_month = month + dir;
                    new_date.setUTCMonth(new_month);
                    // Dec -> Jan (12) or Jan -> Dec (-1) -- limit expected date to 0-11
                    if (new_month < 0 || new_month > 11) new_month = (new_month + 12) % 12;
                } else {
                    // For magnitudes >1, move one month at a time...
                    for (var i = 0; i < mag; i++) // ...which might decrease the day (eg, Jan 31 to Feb 28, etc)...
                    new_date = this.moveMonth(new_date, dir);
                    // ...then reset the day, keeping it in the new month
                    new_month = new_date.getUTCMonth();
                    new_date.setUTCDate(day);
                    test = function() {
                        return new_month != new_date.getUTCMonth();
                    };
                }
                // Common date-resetting loop -- if date is beyond end of month, make it
                // end of month
                while (test()) {
                    new_date.setUTCDate(--day);
                    new_date.setUTCMonth(new_month);
                }
                return new_date;
            },
            moveYear: function(date, dir) {
                return this.moveMonth(date, dir * 12);
            },
            dateWithinRange: function(date) {
                return date >= this.o.startDate && date <= this.o.endDate;
            },
            keydown: function(e) {
                if (this.picker.is(":not(:visible)")) {
                    if (e.keyCode == 27) // allow escape to hide and re-show picker
                    this.show();
                    return;
                }
                var dateChanged = false, dir, day, month, newDate, newViewDate;
                switch (e.keyCode) {
                  case 27:
                    // escape
                    this.hide();
                    e.preventDefault();
                    break;

                  case 37:
                  // left
                    case 39:
                    // right
                    if (!this.o.keyboardNavigation) break;
                    dir = e.keyCode == 37 ? -1 : 1;
                    if (e.ctrlKey) {
                        newDate = this.moveYear(this.date, dir);
                        newViewDate = this.moveYear(this.viewDate, dir);
                    } else if (e.shiftKey) {
                        newDate = this.moveMonth(this.date, dir);
                        newViewDate = this.moveMonth(this.viewDate, dir);
                    } else {
                        newDate = new Date(this.date);
                        newDate.setUTCDate(this.date.getUTCDate() + dir);
                        newViewDate = new Date(this.viewDate);
                        newViewDate.setUTCDate(this.viewDate.getUTCDate() + dir);
                    }
                    if (this.dateWithinRange(newDate)) {
                        this.date = newDate;
                        this.viewDate = newViewDate;
                        this.setValue();
                        this.update();
                        e.preventDefault();
                        dateChanged = true;
                    }
                    break;

                  case 38:
                  // up
                    case 40:
                    // down
                    if (!this.o.keyboardNavigation) break;
                    dir = e.keyCode == 38 ? -1 : 1;
                    if (e.ctrlKey) {
                        newDate = this.moveYear(this.date, dir);
                        newViewDate = this.moveYear(this.viewDate, dir);
                    } else if (e.shiftKey) {
                        newDate = this.moveMonth(this.date, dir);
                        newViewDate = this.moveMonth(this.viewDate, dir);
                    } else {
                        newDate = new Date(this.date);
                        newDate.setUTCDate(this.date.getUTCDate() + dir * 7);
                        newViewDate = new Date(this.viewDate);
                        newViewDate.setUTCDate(this.viewDate.getUTCDate() + dir * 7);
                    }
                    if (this.dateWithinRange(newDate)) {
                        this.date = newDate;
                        this.viewDate = newViewDate;
                        this.setValue();
                        this.update();
                        e.preventDefault();
                        dateChanged = true;
                    }
                    break;

                  case 13:
                    // enter
                    this.hide();
                    e.preventDefault();
                    break;

                  case 9:
                    // tab
                    this.hide();
                    break;
                }
                if (dateChanged) {
                    this._trigger("changeDate");
                    var element;
                    if (this.isInput) {
                        element = this.element;
                    } else if (this.component) {
                        element = this.element.find("input");
                    }
                    if (element) {
                        element.change();
                    }
                }
            },
            showMode: function(dir) {
                if (dir) {
                    this.viewMode = Math.max(this.o.minViewMode, Math.min(2, this.viewMode + dir));
                }
                /*
				vitalets: fixing bug of very special conditions:
				jquery 1.7.1 + webkit + show inline datepicker in bootstrap popover.
				Method show() does not set display css correctly and datepicker is not shown.
				Changed to .css('display', 'block') solve the problem.
				See https://github.com/vitalets/x-editable/issues/37

				In jquery 1.7.2+ everything works fine.
			*/
                //this.picker.find('>div').hide().filter('.datepicker-'+DPGlobal.modes[this.viewMode].clsName).show();
                this.picker.find(">div").hide().filter(".datepicker-" + DPGlobal.modes[this.viewMode].clsName).css("display", "block");
                this.updateNavArrows();
            }
        };
        var DateRangePicker = function(element, options) {
            this.element = $(element);
            this.inputs = $.map(options.inputs, function(i) {
                return i.jquery ? i[0] : i;
            });
            delete options.inputs;
            $(this.inputs).datepicker(options).bind("changeDate", $.proxy(this.dateUpdated, this));
            this.pickers = $.map(this.inputs, function(i) {
                return $(i).data("datepicker");
            });
            this.updateDates();
        };
        DateRangePicker.prototype = {
            updateDates: function() {
                this.dates = $.map(this.pickers, function(i) {
                    return i.date;
                });
                this.updateRanges();
            },
            updateRanges: function() {
                var range = $.map(this.dates, function(d) {
                    return d.valueOf();
                });
                $.each(this.pickers, function(i, p) {
                    p.setRange(range);
                });
            },
            dateUpdated: function(e) {
                var dp = $(e.target).data("datepicker"), new_date = dp.getUTCDate(), i = $.inArray(e.target, this.inputs), l = this.inputs.length;
                if (i == -1) return;
                if (new_date < this.dates[i]) {
                    // Date being moved earlier/left
                    while (i >= 0 && new_date < this.dates[i]) {
                        this.pickers[i--].setUTCDate(new_date);
                    }
                } else if (new_date > this.dates[i]) {
                    // Date being moved later/right
                    while (i < l && new_date > this.dates[i]) {
                        this.pickers[i++].setUTCDate(new_date);
                    }
                }
                this.updateDates();
            },
            remove: function() {
                $.map(this.pickers, function(p) {
                    p.remove();
                });
                delete this.element.data().datepicker;
            }
        };
        function opts_from_el(el, prefix) {
            // Derive options from element data-attrs
            var data = $(el).data(), out = {}, inkey, replace = new RegExp("^" + prefix.toLowerCase() + "([A-Z])"), prefix = new RegExp("^" + prefix.toLowerCase());
            for (var key in data) if (prefix.test(key)) {
                inkey = key.replace(replace, function(_, a) {
                    return a.toLowerCase();
                });
                out[inkey] = data[key];
            }
            return out;
        }
        function opts_from_locale(lang) {
            // Derive options from locale plugins
            var out = {};
            // Check if "de-DE" style date is available, if not language should
            // fallback to 2 letter code eg "de"
            if (!dates[lang]) {
                lang = lang.split("-")[0];
                if (!dates[lang]) return;
            }
            var d = dates[lang];
            $.each(locale_opts, function(i, k) {
                if (k in d) out[k] = d[k];
            });
            return out;
        }
        var old = $.fn.datepicker;
        var datepicker = $.fn.datepicker = function(option) {
            var args = Array.apply(null, arguments);
            args.shift();
            var internal_return, this_return;
            this.each(function() {
                var $this = $(this), data = $this.data("datepicker"), options = typeof option == "object" && option;
                if (!data) {
                    var elopts = opts_from_el(this, "date"), // Preliminary otions
                    xopts = $.extend({}, defaults, elopts, options), locopts = opts_from_locale(xopts.language), // Options priority: js args, data-attrs, locales, defaults
                    opts = $.extend({}, defaults, locopts, elopts, options);
                    if ($this.is(".input-daterange") || opts.inputs) {
                        var ropts = {
                            inputs: opts.inputs || $this.find("input").toArray()
                        };
                        $this.data("datepicker", data = new DateRangePicker(this, $.extend(opts, ropts)));
                    } else {
                        $this.data("datepicker", data = new Datepicker(this, opts));
                    }
                }
                if (typeof option == "string" && typeof data[option] == "function") {
                    internal_return = data[option].apply(data, args);
                    if (internal_return !== undefined) return false;
                }
            });
            if (internal_return !== undefined) return internal_return; else return this;
        };
        var defaults = $.fn.datepicker.defaults = {
            autoclose: false,
            beforeShowDay: $.noop,
            calendarWeeks: false,
            clearBtn: false,
            daysOfWeekDisabled: [],
            endDate: Infinity,
            forceParse: true,
            format: "mm/dd/yyyy",
            keyboardNavigation: true,
            language: "en",
            minViewMode: 0,
            rtl: false,
            startDate: -Infinity,
            startView: 0,
            todayBtn: false,
            todayHighlight: false,
            weekStart: 0
        };
        var locale_opts = $.fn.datepicker.locale_opts = [ "format", "rtl", "weekStart" ];
        $.fn.datepicker.Constructor = Datepicker;
        var dates = $.fn.datepicker.dates = {
            en: {
                days: [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ],
                daysShort: [ "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" ],
                daysMin: [ "Su", "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su" ],
                months: [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ],
                monthsShort: [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ],
                today: "Today",
                clear: "Clear"
            }
        };
        var DPGlobal = {
            modes: [ {
                clsName: "days",
                navFnc: "Month",
                navStep: 1
            }, {
                clsName: "months",
                navFnc: "FullYear",
                navStep: 1
            }, {
                clsName: "years",
                navFnc: "FullYear",
                navStep: 10
            } ],
            isLeapYear: function(year) {
                return year % 4 === 0 && year % 100 !== 0 || year % 400 === 0;
            },
            getDaysInMonth: function(year, month) {
                return [ 31, DPGlobal.isLeapYear(year) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ][month];
            },
            validParts: /dd?|DD?|mm?|MM?|yy(?:yy)?/g,
            nonpunctuation: /[^ -\/:-@\[\u3400-\u9fff-`{-~\t\n\r]+/g,
            parseFormat: function(format) {
                // IE treats \0 as a string end in inputs (truncating the value),
                // so it's a bad format delimiter, anyway
                var separators = format.replace(this.validParts, "\0").split("\0"), parts = format.match(this.validParts);
                if (!separators || !separators.length || !parts || parts.length === 0) {
                    throw new Error("Invalid date format.");
                }
                return {
                    separators: separators,
                    parts: parts
                };
            },
            parseDate: function(date, format, language) {
                if (date instanceof Date) return date;
                if (typeof format === "string") format = DPGlobal.parseFormat(format);
                if (/^[\-+]\d+[dmwy]([\s,]+[\-+]\d+[dmwy])*$/.test(date)) {
                    var part_re = /([\-+]\d+)([dmwy])/, parts = date.match(/([\-+]\d+)([dmwy])/g), part, dir;
                    date = new Date();
                    for (var i = 0; i < parts.length; i++) {
                        part = part_re.exec(parts[i]);
                        dir = parseInt(part[1]);
                        switch (part[2]) {
                          case "d":
                            date.setUTCDate(date.getUTCDate() + dir);
                            break;

                          case "m":
                            date = Datepicker.prototype.moveMonth.call(Datepicker.prototype, date, dir);
                            break;

                          case "w":
                            date.setUTCDate(date.getUTCDate() + dir * 7);
                            break;

                          case "y":
                            date = Datepicker.prototype.moveYear.call(Datepicker.prototype, date, dir);
                            break;
                        }
                    }
                    return UTCDate(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), 0, 0, 0);
                }
                var parts = date && date.match(this.nonpunctuation) || [], date = new Date(), parsed = {}, setters_order = [ "yyyy", "yy", "M", "MM", "m", "mm", "d", "dd" ], setters_map = {
                    yyyy: function(d, v) {
                        return d.setUTCFullYear(v);
                    },
                    yy: function(d, v) {
                        return d.setUTCFullYear(2e3 + v);
                    },
                    m: function(d, v) {
                        v -= 1;
                        while (v < 0) v += 12;
                        v %= 12;
                        d.setUTCMonth(v);
                        while (d.getUTCMonth() != v) d.setUTCDate(d.getUTCDate() - 1);
                        return d;
                    },
                    d: function(d, v) {
                        return d.setUTCDate(v);
                    }
                }, val, filtered, part;
                setters_map["M"] = setters_map["MM"] = setters_map["mm"] = setters_map["m"];
                setters_map["dd"] = setters_map["d"];
                date = UTCDate(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0);
                var fparts = format.parts.slice();
                // Remove noop parts
                if (parts.length != fparts.length) {
                    fparts = $(fparts).filter(function(i, p) {
                        return $.inArray(p, setters_order) !== -1;
                    }).toArray();
                }
                // Process remainder
                if (parts.length == fparts.length) {
                    for (var i = 0, cnt = fparts.length; i < cnt; i++) {
                        val = parseInt(parts[i], 10);
                        part = fparts[i];
                        if (isNaN(val)) {
                            switch (part) {
                              case "MM":
                                filtered = $(dates[language].months).filter(function() {
                                    var m = this.slice(0, parts[i].length), p = parts[i].slice(0, m.length);
                                    return m == p;
                                });
                                val = $.inArray(filtered[0], dates[language].months) + 1;
                                break;

                              case "M":
                                filtered = $(dates[language].monthsShort).filter(function() {
                                    var m = this.slice(0, parts[i].length), p = parts[i].slice(0, m.length);
                                    return m == p;
                                });
                                val = $.inArray(filtered[0], dates[language].monthsShort) + 1;
                                break;
                            }
                        }
                        parsed[part] = val;
                    }
                    for (var i = 0, s; i < setters_order.length; i++) {
                        s = setters_order[i];
                        if (s in parsed && !isNaN(parsed[s])) setters_map[s](date, parsed[s]);
                    }
                }
                return date;
            },
            formatDate: function(date, format, language) {
                if (typeof format === "string") format = DPGlobal.parseFormat(format);
                var val = {
                    d: date.getUTCDate(),
                    D: dates[language].daysShort[date.getUTCDay()],
                    DD: dates[language].days[date.getUTCDay()],
                    m: date.getUTCMonth() + 1,
                    M: dates[language].monthsShort[date.getUTCMonth()],
                    MM: dates[language].months[date.getUTCMonth()],
                    yy: date.getUTCFullYear().toString().substring(2),
                    yyyy: date.getUTCFullYear()
                };
                val.dd = (val.d < 10 ? "0" : "") + val.d;
                val.mm = (val.m < 10 ? "0" : "") + val.m;
                var date = [], seps = $.extend([], format.separators);
                for (var i = 0, cnt = format.parts.length; i <= cnt; i++) {
                    if (seps.length) date.push(seps.shift());
                    date.push(val[format.parts[i]]);
                }
                return date.join("");
            },
            headTemplate: "<thead>" + "<tr>" + '<th class="prev"><i class="icon-arrow-left"/></th>' + '<th colspan="5" class="datepicker-switch"></th>' + '<th class="next"><i class="icon-arrow-right"/></th>' + "</tr>" + "</thead>",
            contTemplate: '<tbody><tr><td colspan="7"></td></tr></tbody>',
            footTemplate: '<tfoot><tr><th colspan="7" class="today"></th></tr><tr><th colspan="7" class="clear"></th></tr></tfoot>'
        };
        DPGlobal.template = '<div class="datepicker">' + '<div class="datepicker-days">' + '<table class=" table-condensed">' + DPGlobal.headTemplate + "<tbody></tbody>" + DPGlobal.footTemplate + "</table>" + "</div>" + '<div class="datepicker-months">' + '<table class="table-condensed">' + DPGlobal.headTemplate + DPGlobal.contTemplate + DPGlobal.footTemplate + "</table>" + "</div>" + '<div class="datepicker-years">' + '<table class="table-condensed">' + DPGlobal.headTemplate + DPGlobal.contTemplate + DPGlobal.footTemplate + "</table>" + "</div>" + "</div>";
        $.fn.datepicker.DPGlobal = DPGlobal;
        /* DATEPICKER NO CONFLICT
	* =================== */
        $.fn.datepicker.noConflict = function() {
            $.fn.datepicker = old;
            return this;
        };
        /* DATEPICKER DATA-API
	* ================== */
        $(document).on("focus.datepicker.data-api click.datepicker.data-api", '[data-provide="datepicker"]', function(e) {
            var $this = $(this);
            if ($this.data("datepicker")) return;
            e.preventDefault();
            // component click requires us to explicitly show it
            datepicker.call($this, "show");
        });
        $(function() {
            //$('[data-provide="datepicker-inline"]').datepicker();
            //vit: changed to support noConflict()
            datepicker.call($('[data-provide="datepicker-inline"]'));
        });
    })(window.jQuery);
    /**
Bootstrap-datepicker.  
Description and examples: https://github.com/eternicode/bootstrap-datepicker.  
For **i18n** you should include js file from here: https://github.com/eternicode/bootstrap-datepicker/tree/master/js/locales
and set `language` option.  
Since 1.4.0 date has different appearance in **popup** and **inline** modes. 

@class date
@extends abstractinput
@final
@example
<a href="#" id="dob" data-type="date" data-pk="1" data-url="/post" data-title="Select date">15/05/1984</a>
<script>
$(function(){
    $('#dob').editable({
        format: 'yyyy-mm-dd',    
        viewformat: 'dd/mm/yyyy',    
        datepicker: {
                weekStart: 1
           }
        }
    });
});
</script>
**/
    (function($) {
        "use strict";
        //store bootstrap-datepicker as bdateicker to exclude conflict with jQuery UI one
        $.fn.bdatepicker = $.fn.datepicker.noConflict();
        if (!$.fn.datepicker) {
            //if there were no other datepickers, keep also original name
            $.fn.datepicker = $.fn.bdatepicker;
        }
        var Date = function(options) {
            this.init("date", options, Date.defaults);
            this.initPicker(options, Date.defaults);
        };
        $.fn.editableutils.inherit(Date, $.fn.editabletypes.abstractinput);
        $.extend(Date.prototype, {
            initPicker: function(options, defaults) {
                //'format' is set directly from settings or data-* attributes
                //by default viewformat equals to format
                if (!this.options.viewformat) {
                    this.options.viewformat = this.options.format;
                }
                //try parse datepicker config defined as json string in data-datepicker
                options.datepicker = $.fn.editableutils.tryParseJson(options.datepicker, true);
                //overriding datepicker config (as by default jQuery extend() is not recursive)
                //since 1.4 datepicker internally uses viewformat instead of format. Format is for submit only
                this.options.datepicker = $.extend({}, defaults.datepicker, options.datepicker, {
                    format: this.options.viewformat
                });
                //language
                this.options.datepicker.language = this.options.datepicker.language || "en";
                //store DPglobal
                this.dpg = $.fn.bdatepicker.DPGlobal;
                //store parsed formats
                this.parsedFormat = this.dpg.parseFormat(this.options.format);
                this.parsedViewFormat = this.dpg.parseFormat(this.options.viewformat);
            },
            render: function() {
                this.$input.bdatepicker(this.options.datepicker);
                //"clear" link
                if (this.options.clear) {
                    this.$clear = $('<a href="#"></a>').html(this.options.clear).click($.proxy(function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        this.clear();
                    }, this));
                    this.$tpl.parent().append($('<div class="editable-clear">').append(this.$clear));
                }
            },
            value2html: function(value, element) {
                var text = value ? this.dpg.formatDate(value, this.parsedViewFormat, this.options.datepicker.language) : "";
                Date.superclass.value2html.call(this, text, element);
            },
            html2value: function(html) {
                return this.parseDate(html, this.parsedViewFormat);
            },
            value2str: function(value) {
                return value ? this.dpg.formatDate(value, this.parsedFormat, this.options.datepicker.language) : "";
            },
            str2value: function(str) {
                return this.parseDate(str, this.parsedFormat);
            },
            value2submit: function(value) {
                return this.value2str(value);
            },
            value2input: function(value) {
                this.$input.bdatepicker("update", value);
            },
            input2value: function() {
                return this.$input.data("datepicker").date;
            },
            activate: function() {},
            clear: function() {
                this.$input.data("datepicker").date = null;
                this.$input.find(".active").removeClass("active");
                if (!this.options.showbuttons) {
                    this.$input.closest("form").submit();
                }
            },
            autosubmit: function() {
                this.$input.on("mouseup", ".day", function(e) {
                    if ($(e.currentTarget).is(".old") || $(e.currentTarget).is(".new")) {
                        return;
                    }
                    var $form = $(this).closest("form");
                    setTimeout(function() {
                        $form.submit();
                    }, 200);
                });
            },
            /*
        For incorrect date bootstrap-datepicker returns current date that is not suitable
        for datefield.
        This function returns null for incorrect date.  
       */
            parseDate: function(str, format) {
                var date = null, formattedBack;
                if (str) {
                    date = this.dpg.parseDate(str, format, this.options.datepicker.language);
                    if (typeof str === "string") {
                        formattedBack = this.dpg.formatDate(date, format, this.options.datepicker.language);
                        if (str !== formattedBack) {
                            date = null;
                        }
                    }
                }
                return date;
            }
        });
        Date.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
            /**
        @property tpl 
        @default <div></div>
        **/
            tpl: '<div class="editable-date well"></div>',
            /**
        @property inputclass 
        @default null
        **/
            inputclass: null,
            /**
        Format used for sending value to server. Also applied when converting date from <code>data-value</code> attribute.<br>
        Possible tokens are: <code>d, dd, m, mm, yy, yyyy</code>  

        @property format 
        @type string
        @default yyyy-mm-dd
        **/
            format: "yyyy-mm-dd",
            /**
        Format used for displaying date. Also applied when converting date from element's text on init.   
        If not specified equals to <code>format</code>

        @property viewformat 
        @type string
        @default null
        **/
            viewformat: null,
            /**
        Configuration of datepicker.
        Full list of options: http://bootstrap-datepicker.readthedocs.org/en/latest/options.html

        @property datepicker 
        @type object
        @default {
            weekStart: 0,
            startView: 0,
            minViewMode: 0,
            autoclose: false
        }
        **/
            datepicker: {
                weekStart: 0,
                startView: 0,
                minViewMode: 0,
                autoclose: false
            },
            /**
        Text shown as clear date button. 
        If <code>false</code> clear button will not be rendered.

        @property clear 
        @type boolean|string
        @default 'x clear'
        **/
            clear: "&times; clear"
        });
        $.fn.editabletypes.date = Date;
    })(window.jQuery);
    /**
Bootstrap datefield input - modification for inline mode.
Shows normal <input type="text"> and binds popup datepicker.  
Automatically shown in inline mode.

@class datefield
@extends date

@since 1.4.0
**/
    (function($) {
        "use strict";
        var DateField = function(options) {
            this.init("datefield", options, DateField.defaults);
            this.initPicker(options, DateField.defaults);
        };
        $.fn.editableutils.inherit(DateField, $.fn.editabletypes.date);
        $.extend(DateField.prototype, {
            render: function() {
                this.$input = this.$tpl.find("input");
                this.setClass();
                this.setAttr("placeholder");
                //bootstrap-datepicker is set `bdateicker` to exclude conflict with jQuery UI one. (in date.js)        
                this.$tpl.bdatepicker(this.options.datepicker);
                //need to disable original event handlers
                this.$input.off("focus keydown");
                //update value of datepicker
                this.$input.keyup($.proxy(function() {
                    this.$tpl.removeData("date");
                    this.$tpl.bdatepicker("update");
                }, this));
            },
            value2input: function(value) {
                this.$input.val(value ? this.dpg.formatDate(value, this.parsedViewFormat, this.options.datepicker.language) : "");
                this.$tpl.bdatepicker("update");
            },
            input2value: function() {
                return this.html2value(this.$input.val());
            },
            activate: function() {
                $.fn.editabletypes.text.prototype.activate.call(this);
            },
            autosubmit: function() {}
        });
        DateField.defaults = $.extend({}, $.fn.editabletypes.date.defaults, {
            /**
        @property tpl 
        **/
            tpl: '<div class="input-append date"><input type="text"/><span class="add-on"><i class="icon-th"></i></span></div>',
            /**
        @property inputclass 
        @default 'input-small'
        **/
            inputclass: "input-small",
            /* datepicker config */
            datepicker: {
                weekStart: 0,
                startView: 0,
                minViewMode: 0,
                autoclose: true
            }
        });
        $.fn.editabletypes.datefield = DateField;
    })(window.jQuery);
    /**
Bootstrap-datetimepicker.  
Based on [smalot bootstrap-datetimepicker plugin](https://github.com/smalot/bootstrap-datetimepicker). 
Before usage you should manually include dependent js and css:

    <link href="css/datetimepicker.css" rel="stylesheet" type="text/css"></link> 
    <script src="js/bootstrap-datetimepicker.js"></script>

For **i18n** you should include js file from here: https://github.com/smalot/bootstrap-datetimepicker/tree/master/js/locales
and set `language` option.  

@class datetime
@extends abstractinput
@final
@since 1.4.4
@example
<a href="#" id="last_seen" data-type="datetime" data-pk="1" data-url="/post" title="Select date & time">15/03/2013 12:45</a>
<script>
$(function(){
    $('#last_seen').editable({
        format: 'yyyy-mm-dd hh:ii',    
        viewformat: 'dd/mm/yyyy hh:ii',    
        datetimepicker: {
                weekStart: 1
           }
        }
    });
});
</script>
**/
    (function($) {
        "use strict";
        var DateTime = function(options) {
            this.init("datetime", options, DateTime.defaults);
            this.initPicker(options, DateTime.defaults);
        };
        $.fn.editableutils.inherit(DateTime, $.fn.editabletypes.abstractinput);
        $.extend(DateTime.prototype, {
            initPicker: function(options, defaults) {
                //'format' is set directly from settings or data-* attributes
                //by default viewformat equals to format
                if (!this.options.viewformat) {
                    this.options.viewformat = this.options.format;
                }
                //try parse datetimepicker config defined as json string in data-datetimepicker
                options.datetimepicker = $.fn.editableutils.tryParseJson(options.datetimepicker, true);
                //overriding datetimepicker config (as by default jQuery extend() is not recursive)
                //since 1.4 datetimepicker internally uses viewformat instead of format. Format is for submit only
                this.options.datetimepicker = $.extend({}, defaults.datetimepicker, options.datetimepicker, {
                    format: this.options.viewformat
                });
                //language
                this.options.datetimepicker.language = this.options.datetimepicker.language || "en";
                //store DPglobal
                this.dpg = $.fn.datetimepicker.DPGlobal;
                //store parsed formats
                this.parsedFormat = this.dpg.parseFormat(this.options.format, this.options.formatType);
                this.parsedViewFormat = this.dpg.parseFormat(this.options.viewformat, this.options.formatType);
            },
            render: function() {
                this.$input.datetimepicker(this.options.datetimepicker);
                //adjust container position when viewMode changes
                //see https://github.com/smalot/bootstrap-datetimepicker/pull/80
                this.$input.on("changeMode", function(e) {
                    var f = $(this).closest("form").parent();
                    //timeout here, otherwise container changes position before form has new size
                    setTimeout(function() {
                        f.triggerHandler("resize");
                    }, 0);
                });
                //"clear" link
                if (this.options.clear) {
                    this.$clear = $('<a href="#"></a>').html(this.options.clear).click($.proxy(function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        this.clear();
                    }, this));
                    this.$tpl.parent().append($('<div class="editable-clear">').append(this.$clear));
                }
            },
            value2html: function(value, element) {
                //formatDate works with UTCDate!
                var text = value ? this.dpg.formatDate(this.toUTC(value), this.parsedViewFormat, this.options.datetimepicker.language, this.options.formatType) : "";
                if (element) {
                    DateTime.superclass.value2html.call(this, text, element);
                } else {
                    return text;
                }
            },
            html2value: function(html) {
                //parseDate return utc date!
                var value = this.parseDate(html, this.parsedViewFormat);
                return value ? this.fromUTC(value) : null;
            },
            value2str: function(value) {
                //formatDate works with UTCDate!
                return value ? this.dpg.formatDate(this.toUTC(value), this.parsedFormat, this.options.datetimepicker.language, this.options.formatType) : "";
            },
            str2value: function(str) {
                //parseDate return utc date!
                var value = this.parseDate(str, this.parsedFormat);
                return value ? this.fromUTC(value) : null;
            },
            value2submit: function(value) {
                return this.value2str(value);
            },
            value2input: function(value) {
                if (value) {
                    this.$input.data("datetimepicker").setDate(value);
                }
            },
            input2value: function() {
                //date may be cleared, in that case getDate() triggers error
                var dt = this.$input.data("datetimepicker");
                return dt.date ? dt.getDate() : null;
            },
            activate: function() {},
            clear: function() {
                this.$input.data("datetimepicker").date = null;
                this.$input.find(".active").removeClass("active");
                if (!this.options.showbuttons) {
                    this.$input.closest("form").submit();
                }
            },
            autosubmit: function() {
                this.$input.on("mouseup", ".minute", function(e) {
                    var $form = $(this).closest("form");
                    setTimeout(function() {
                        $form.submit();
                    }, 200);
                });
            },
            //convert date from local to utc
            toUTC: function(value) {
                return value ? new Date(value.valueOf() - value.getTimezoneOffset() * 6e4) : value;
            },
            //convert date from utc to local
            fromUTC: function(value) {
                return value ? new Date(value.valueOf() + value.getTimezoneOffset() * 6e4) : value;
            },
            /*
        For incorrect date bootstrap-datetimepicker returns current date that is not suitable
        for datetimefield.
        This function returns null for incorrect date.  
       */
            parseDate: function(str, format) {
                var date = null, formattedBack;
                if (str) {
                    date = this.dpg.parseDate(str, format, this.options.datetimepicker.language, this.options.formatType);
                    if (typeof str === "string") {
                        formattedBack = this.dpg.formatDate(date, format, this.options.datetimepicker.language, this.options.formatType);
                        if (str !== formattedBack) {
                            date = null;
                        }
                    }
                }
                return date;
            }
        });
        DateTime.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
            /**
        @property tpl 
        @default <div></div>
        **/
            tpl: '<div class="editable-date well"></div>',
            /**
        @property inputclass 
        @default null
        **/
            inputclass: null,
            /**
        Format used for sending value to server. Also applied when converting date from <code>data-value</code> attribute.<br>
        Possible tokens are: <code>d, dd, m, mm, yy, yyyy, h, i</code>  
        
        @property format 
        @type string
        @default yyyy-mm-dd hh:ii
        **/
            format: "yyyy-mm-dd hh:ii",
            formatType: "standard",
            /**
        Format used for displaying date. Also applied when converting date from element's text on init.   
        If not specified equals to <code>format</code>
        
        @property viewformat 
        @type string
        @default null
        **/
            viewformat: null,
            /**
        Configuration of datetimepicker.
        Full list of options: https://github.com/smalot/bootstrap-datetimepicker

        @property datetimepicker 
        @type object
        @default { }
        **/
            datetimepicker: {
                todayHighlight: false,
                autoclose: false
            },
            /**
        Text shown as clear date button. 
        If <code>false</code> clear button will not be rendered.

        @property clear 
        @type boolean|string
        @default 'x clear'
        **/
            clear: "&times; clear"
        });
        $.fn.editabletypes.datetime = DateTime;
    })(window.jQuery);
    /**
Bootstrap datetimefield input - datetime input for inline mode.
Shows normal <input type="text"> and binds popup datetimepicker.  
Automatically shown in inline mode.

@class datetimefield
@extends datetime

**/
    (function($) {
        "use strict";
        var DateTimeField = function(options) {
            this.init("datetimefield", options, DateTimeField.defaults);
            this.initPicker(options, DateTimeField.defaults);
        };
        $.fn.editableutils.inherit(DateTimeField, $.fn.editabletypes.datetime);
        $.extend(DateTimeField.prototype, {
            render: function() {
                this.$input = this.$tpl.find("input");
                this.setClass();
                this.setAttr("placeholder");
                this.$tpl.datetimepicker(this.options.datetimepicker);
                //need to disable original event handlers
                this.$input.off("focus keydown");
                //update value of datepicker
                this.$input.keyup($.proxy(function() {
                    this.$tpl.removeData("date");
                    this.$tpl.datetimepicker("update");
                }, this));
            },
            value2input: function(value) {
                this.$input.val(this.value2html(value));
                this.$tpl.datetimepicker("update");
            },
            input2value: function() {
                return this.html2value(this.$input.val());
            },
            activate: function() {
                $.fn.editabletypes.text.prototype.activate.call(this);
            },
            autosubmit: function() {}
        });
        DateTimeField.defaults = $.extend({}, $.fn.editabletypes.datetime.defaults, {
            /**
        @property tpl 
        **/
            tpl: '<div class="input-append date"><input type="text"/><span class="add-on"><i class="icon-th"></i></span></div>',
            /**
        @property inputclass 
        @default 'input-medium'
        **/
            inputclass: "input-medium",
            /* datetimepicker config */
            datetimepicker: {
                todayHighlight: false,
                autoclose: true
            }
        });
        $.fn.editabletypes.datetimefield = DateTimeField;
    })(window.jQuery);
});

define("torabot/main/0.1.0/xeditable/xeditable-debug.css", [], function() {
    seajs.importStyle(".editableform{margin-bottom:0}.editableform .control-group{margin-bottom:0;white-space:nowrap;line-height:20px}.editableform .form-control{width:auto}.editable-buttons{display:inline-block;vertical-align:top;margin-left:7px;zoom:1;*display:inline}.editable-buttons.editable-buttons-bottom{display:block;margin-top:7px;margin-left:0}.editable-input{vertical-align:top;display:inline-block;width:auto;white-space:normal;zoom:1;*display:inline}.editable-buttons .editable-cancel{margin-left:7px}.editable-buttons button.ui-button-icon-only{height:24px;width:30px}.editableform-loading{background:url(../img/loading.gif) center center no-repeat;height:25px;width:auto;min-width:25px}.editable-inline .editableform-loading{background-position:left 5px}.editable-error-block{max-width:300px;margin:5px 0 0;width:auto;white-space:normal}.editable-error-block.ui-state-error{padding:3px}.editable-error{color:red}.editableform .editable-date{padding:0;margin:0;float:left}.editable-inline .add-on .icon-th{margin-top:3px;margin-left:1px}.editable-checklist label input[type=checkbox],.editable-checklist label span{vertical-align:middle;margin:0}.editable-checklist label{white-space:nowrap}.editable-wysihtml5{width:566px;height:250px}.editable-clear{clear:both;font-size:.9em;text-decoration:none;text-align:right}.editable-clear-x{background:url(../img/clear.png) center center no-repeat;display:block;width:13px;height:13px;position:absolute;opacity:.6;z-index:100;top:50%;right:6px;margin-top:-6px}.editable-clear-x:hover{opacity:1}.editable-pre-wrapped{white-space:pre-wrap}.editable-container.editable-popup{max-width:none!important}.editable-container.popover{width:auto}.editable-container.editable-inline{display:inline-block;vertical-align:middle;width:auto;zoom:1;*display:inline}.editable-container.ui-widget{font-size:inherit;z-index:9990}.editable-click,a.editable-click,a.editable-click:hover{text-decoration:none;border-bottom:dashed 1px #08c}.editable-click.editable-disabled,a.editable-click.editable-disabled,a.editable-click.editable-disabled:hover{color:#585858;cursor:default;border-bottom:0}.editable-empty,.editable-empty:hover,.editable-empty:focus{font-style:italic;color:#D14;text-decoration:none}.editable-unsaved{font-weight:700}.editable-bg-transition{-webkit-transition:background-color 1400ms ease-out;-moz-transition:background-color 1400ms ease-out;-o-transition:background-color 1400ms ease-out;-ms-transition:background-color 1400ms ease-out;transition:background-color 1400ms ease-out}.form-horizontal .editable{padding-top:5px;display:inline-block}.datepicker{padding:4px;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;direction:ltr}.datepicker-inline{width:220px}.datepicker.datepicker-rtl{direction:rtl}.datepicker.datepicker-rtl table tr td span{float:right}.datepicker-dropdown{top:0;left:0}.datepicker-dropdown:before{content:'';display:inline-block;border-left:7px solid transparent;border-right:7px solid transparent;border-bottom:7px solid #ccc;border-bottom-color:rgba(0,0,0,.2);position:absolute;top:-7px;left:6px}.datepicker-dropdown:after{content:'';display:inline-block;border-left:6px solid transparent;border-right:6px solid transparent;border-bottom:6px solid #fff;position:absolute;top:-6px;left:7px}.datepicker>div{display:none}.datepicker.days div.datepicker-days{display:block}.datepicker.months div.datepicker-months{display:block}.datepicker.years div.datepicker-years{display:block}.datepicker table{margin:0}.datepicker td,.datepicker th{text-align:center;width:20px;height:20px;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;border:0}.table-striped .datepicker table tr td,.table-striped .datepicker table tr th{background-color:transparent}.datepicker table tr td.day:hover{background:#eee;cursor:pointer}.datepicker table tr td.old,.datepicker table tr td.new{color:#999}.datepicker table tr td.disabled,.datepicker table tr td.disabled:hover{background:0;color:#999;cursor:default}.datepicker table tr td.today,.datepicker table tr td.today:hover,.datepicker table tr td.today.disabled,.datepicker table tr td.today.disabled:hover{background-color:#fde19a;background-image:-moz-linear-gradient(top,#fdd49a,#fdf59a);background-image:-ms-linear-gradient(top,#fdd49a,#fdf59a);background-image:-webkit-gradient(linear,0 0,0 100%,from(#fdd49a),to(#fdf59a));background-image:-webkit-linear-gradient(top,#fdd49a,#fdf59a);background-image:-o-linear-gradient(top,#fdd49a,#fdf59a);background-image:linear-gradient(top,#fdd49a,#fdf59a);background-repeat:repeat-x;filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#fdd49a', endColorstr='#fdf59a', GradientType=0);border-color:#fdf59a #fdf59a #fbed50;border-color:rgba(0,0,0,.1) rgba(0,0,0,.1) rgba(0,0,0,.25);filter:progid:DXImageTransform.Microsoft.gradient(enabled=false);color:#000}.datepicker table tr td.today:hover,.datepicker table tr td.today:hover:hover,.datepicker table tr td.today.disabled:hover,.datepicker table tr td.today.disabled:hover:hover,.datepicker table tr td.today:active,.datepicker table tr td.today:hover:active,.datepicker table tr td.today.disabled:active,.datepicker table tr td.today.disabled:hover:active,.datepicker table tr td.today.active,.datepicker table tr td.today:hover.active,.datepicker table tr td.today.disabled.active,.datepicker table tr td.today.disabled:hover.active,.datepicker table tr td.today.disabled,.datepicker table tr td.today:hover.disabled,.datepicker table tr td.today.disabled.disabled,.datepicker table tr td.today.disabled:hover.disabled,.datepicker table tr td.today[disabled],.datepicker table tr td.today:hover[disabled],.datepicker table tr td.today.disabled[disabled],.datepicker table tr td.today.disabled:hover[disabled]{background-color:#fdf59a}.datepicker table tr td.today:active,.datepicker table tr td.today:hover:active,.datepicker table tr td.today.disabled:active,.datepicker table tr td.today.disabled:hover:active,.datepicker table tr td.today.active,.datepicker table tr td.today:hover.active,.datepicker table tr td.today.disabled.active,.datepicker table tr td.today.disabled:hover.active{background-color:#fbf069 \\9}.datepicker table tr td.today:hover:hover{color:#000}.datepicker table tr td.today.active:hover{color:#fff}.datepicker table tr td.range,.datepicker table tr td.range:hover,.datepicker table tr td.range.disabled,.datepicker table tr td.range.disabled:hover{background:#eee;-webkit-border-radius:0;-moz-border-radius:0;border-radius:0}.datepicker table tr td.range.today,.datepicker table tr td.range.today:hover,.datepicker table tr td.range.today.disabled,.datepicker table tr td.range.today.disabled:hover{background-color:#f3d17a;background-image:-moz-linear-gradient(top,#f3c17a,#f3e97a);background-image:-ms-linear-gradient(top,#f3c17a,#f3e97a);background-image:-webkit-gradient(linear,0 0,0 100%,from(#f3c17a),to(#f3e97a));background-image:-webkit-linear-gradient(top,#f3c17a,#f3e97a);background-image:-o-linear-gradient(top,#f3c17a,#f3e97a);background-image:linear-gradient(top,#f3c17a,#f3e97a);background-repeat:repeat-x;filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#f3c17a', endColorstr='#f3e97a', GradientType=0);border-color:#f3e97a #f3e97a #edde34;border-color:rgba(0,0,0,.1) rgba(0,0,0,.1) rgba(0,0,0,.25);filter:progid:DXImageTransform.Microsoft.gradient(enabled=false);-webkit-border-radius:0;-moz-border-radius:0;border-radius:0}.datepicker table tr td.range.today:hover,.datepicker table tr td.range.today:hover:hover,.datepicker table tr td.range.today.disabled:hover,.datepicker table tr td.range.today.disabled:hover:hover,.datepicker table tr td.range.today:active,.datepicker table tr td.range.today:hover:active,.datepicker table tr td.range.today.disabled:active,.datepicker table tr td.range.today.disabled:hover:active,.datepicker table tr td.range.today.active,.datepicker table tr td.range.today:hover.active,.datepicker table tr td.range.today.disabled.active,.datepicker table tr td.range.today.disabled:hover.active,.datepicker table tr td.range.today.disabled,.datepicker table tr td.range.today:hover.disabled,.datepicker table tr td.range.today.disabled.disabled,.datepicker table tr td.range.today.disabled:hover.disabled,.datepicker table tr td.range.today[disabled],.datepicker table tr td.range.today:hover[disabled],.datepicker table tr td.range.today.disabled[disabled],.datepicker table tr td.range.today.disabled:hover[disabled]{background-color:#f3e97a}.datepicker table tr td.range.today:active,.datepicker table tr td.range.today:hover:active,.datepicker table tr td.range.today.disabled:active,.datepicker table tr td.range.today.disabled:hover:active,.datepicker table tr td.range.today.active,.datepicker table tr td.range.today:hover.active,.datepicker table tr td.range.today.disabled.active,.datepicker table tr td.range.today.disabled:hover.active{background-color:#efe24b \\9}.datepicker table tr td.selected,.datepicker table tr td.selected:hover,.datepicker table tr td.selected.disabled,.datepicker table tr td.selected.disabled:hover{background-color:#9e9e9e;background-image:-moz-linear-gradient(top,#b3b3b3,gray);background-image:-ms-linear-gradient(top,#b3b3b3,gray);background-image:-webkit-gradient(linear,0 0,0 100%,from(#b3b3b3),to(gray));background-image:-webkit-linear-gradient(top,#b3b3b3,gray);background-image:-o-linear-gradient(top,#b3b3b3,gray);background-image:linear-gradient(top,#b3b3b3,gray);background-repeat:repeat-x;filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#b3b3b3', endColorstr='#808080', GradientType=0);border-color:gray #808080 #595959;border-color:rgba(0,0,0,.1) rgba(0,0,0,.1) rgba(0,0,0,.25);filter:progid:DXImageTransform.Microsoft.gradient(enabled=false);color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,.25)}.datepicker table tr td.selected:hover,.datepicker table tr td.selected:hover:hover,.datepicker table tr td.selected.disabled:hover,.datepicker table tr td.selected.disabled:hover:hover,.datepicker table tr td.selected:active,.datepicker table tr td.selected:hover:active,.datepicker table tr td.selected.disabled:active,.datepicker table tr td.selected.disabled:hover:active,.datepicker table tr td.selected.active,.datepicker table tr td.selected:hover.active,.datepicker table tr td.selected.disabled.active,.datepicker table tr td.selected.disabled:hover.active,.datepicker table tr td.selected.disabled,.datepicker table tr td.selected:hover.disabled,.datepicker table tr td.selected.disabled.disabled,.datepicker table tr td.selected.disabled:hover.disabled,.datepicker table tr td.selected[disabled],.datepicker table tr td.selected:hover[disabled],.datepicker table tr td.selected.disabled[disabled],.datepicker table tr td.selected.disabled:hover[disabled]{background-color:gray}.datepicker table tr td.selected:active,.datepicker table tr td.selected:hover:active,.datepicker table tr td.selected.disabled:active,.datepicker table tr td.selected.disabled:hover:active,.datepicker table tr td.selected.active,.datepicker table tr td.selected:hover.active,.datepicker table tr td.selected.disabled.active,.datepicker table tr td.selected.disabled:hover.active{background-color:#666 \\9}.datepicker table tr td.active,.datepicker table tr td.active:hover,.datepicker table tr td.active.disabled,.datepicker table tr td.active.disabled:hover{background-color:#006dcc;background-image:-moz-linear-gradient(top,#08c,#04c);background-image:-ms-linear-gradient(top,#08c,#04c);background-image:-webkit-gradient(linear,0 0,0 100%,from(#08c),to(#04c));background-image:-webkit-linear-gradient(top,#08c,#04c);background-image:-o-linear-gradient(top,#08c,#04c);background-image:linear-gradient(top,#08c,#04c);background-repeat:repeat-x;filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#0088cc', endColorstr='#0044cc', GradientType=0);border-color:#04c #04c #002a80;border-color:rgba(0,0,0,.1) rgba(0,0,0,.1) rgba(0,0,0,.25);filter:progid:DXImageTransform.Microsoft.gradient(enabled=false);color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,.25)}.datepicker table tr td.active:hover,.datepicker table tr td.active:hover:hover,.datepicker table tr td.active.disabled:hover,.datepicker table tr td.active.disabled:hover:hover,.datepicker table tr td.active:active,.datepicker table tr td.active:hover:active,.datepicker table tr td.active.disabled:active,.datepicker table tr td.active.disabled:hover:active,.datepicker table tr td.active.active,.datepicker table tr td.active:hover.active,.datepicker table tr td.active.disabled.active,.datepicker table tr td.active.disabled:hover.active,.datepicker table tr td.active.disabled,.datepicker table tr td.active:hover.disabled,.datepicker table tr td.active.disabled.disabled,.datepicker table tr td.active.disabled:hover.disabled,.datepicker table tr td.active[disabled],.datepicker table tr td.active:hover[disabled],.datepicker table tr td.active.disabled[disabled],.datepicker table tr td.active.disabled:hover[disabled]{background-color:#04c}.datepicker table tr td.active:active,.datepicker table tr td.active:hover:active,.datepicker table tr td.active.disabled:active,.datepicker table tr td.active.disabled:hover:active,.datepicker table tr td.active.active,.datepicker table tr td.active:hover.active,.datepicker table tr td.active.disabled.active,.datepicker table tr td.active.disabled:hover.active{background-color:#039 \\9}.datepicker table tr td span{display:block;width:23%;height:54px;line-height:54px;float:left;margin:1%;cursor:pointer;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px}.datepicker table tr td span:hover{background:#eee}.datepicker table tr td span.disabled,.datepicker table tr td span.disabled:hover{background:0;color:#999;cursor:default}.datepicker table tr td span.active,.datepicker table tr td span.active:hover,.datepicker table tr td span.active.disabled,.datepicker table tr td span.active.disabled:hover{background-color:#006dcc;background-image:-moz-linear-gradient(top,#08c,#04c);background-image:-ms-linear-gradient(top,#08c,#04c);background-image:-webkit-gradient(linear,0 0,0 100%,from(#08c),to(#04c));background-image:-webkit-linear-gradient(top,#08c,#04c);background-image:-o-linear-gradient(top,#08c,#04c);background-image:linear-gradient(top,#08c,#04c);background-repeat:repeat-x;filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#0088cc', endColorstr='#0044cc', GradientType=0);border-color:#04c #04c #002a80;border-color:rgba(0,0,0,.1) rgba(0,0,0,.1) rgba(0,0,0,.25);filter:progid:DXImageTransform.Microsoft.gradient(enabled=false);color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,.25)}.datepicker table tr td span.active:hover,.datepicker table tr td span.active:hover:hover,.datepicker table tr td span.active.disabled:hover,.datepicker table tr td span.active.disabled:hover:hover,.datepicker table tr td span.active:active,.datepicker table tr td span.active:hover:active,.datepicker table tr td span.active.disabled:active,.datepicker table tr td span.active.disabled:hover:active,.datepicker table tr td span.active.active,.datepicker table tr td span.active:hover.active,.datepicker table tr td span.active.disabled.active,.datepicker table tr td span.active.disabled:hover.active,.datepicker table tr td span.active.disabled,.datepicker table tr td span.active:hover.disabled,.datepicker table tr td span.active.disabled.disabled,.datepicker table tr td span.active.disabled:hover.disabled,.datepicker table tr td span.active[disabled],.datepicker table tr td span.active:hover[disabled],.datepicker table tr td span.active.disabled[disabled],.datepicker table tr td span.active.disabled:hover[disabled]{background-color:#04c}.datepicker table tr td span.active:active,.datepicker table tr td span.active:hover:active,.datepicker table tr td span.active.disabled:active,.datepicker table tr td span.active.disabled:hover:active,.datepicker table tr td span.active.active,.datepicker table tr td span.active:hover.active,.datepicker table tr td span.active.disabled.active,.datepicker table tr td span.active.disabled:hover.active{background-color:#039 \\9}.datepicker table tr td span.old,.datepicker table tr td span.new{color:#999}.datepicker th.datepicker-switch{width:145px}.datepicker thead tr:first-child th,.datepicker tfoot tr th{cursor:pointer}.datepicker thead tr:first-child th:hover,.datepicker tfoot tr th:hover{background:#eee}.datepicker .cw{font-size:10px;width:12px;padding:0 2px 0 5px;vertical-align:middle}.datepicker thead tr:first-child th.cw{cursor:default;background-color:transparent}.input-append.date .add-on i,.input-prepend.date .add-on i{display:block;cursor:pointer;width:16px;height:16px}.input-daterange input{text-align:center}.input-daterange input:first-child{-webkit-border-radius:3px 0 0 3px;-moz-border-radius:3px 0 0 3px;border-radius:3px 0 0 3px}.input-daterange input:last-child{-webkit-border-radius:0 3px 3px 0;-moz-border-radius:0 3px 3px 0;border-radius:0 3px 3px 0}.input-daterange .add-on{display:inline-block;width:auto;min-width:16px;height:18px;padding:4px 5px;font-weight:400;line-height:18px;text-align:center;text-shadow:0 1px 0 #fff;vertical-align:middle;background-color:#eee;border:1px solid #ccc;margin-left:-5px;margin-right:-5px}");
});

define("torabot/main/0.1.0/jquery.storage-debug", [], function(require) {
    (function($, window, document) {
        "use strict";
        $.map([ "localStorage", "sessionStorage" ], function(method) {
            var defaults = {
                cookiePrefix: "fallback:" + method + ":",
                cookieOptions: {
                    path: "/",
                    domain: document.domain,
                    expires: "localStorage" === method ? {
                        expires: 365
                    } : undefined
                }
            };
            try {
                $.support[method] = method in window && window[method] !== null;
            } catch (e) {
                $.support[method] = false;
            }
            $[method] = function(key, value) {
                var options = $.extend({}, defaults, $[method].options);
                this.getItem = function(key) {
                    var returns = function(key) {
                        return JSON.parse($.support[method] ? window[method].getItem(key) : $.cookie(options.cookiePrefix + key));
                    };
                    if (typeof key === "string") return returns(key);
                    var arr = [], i = key.length;
                    while (i--) arr[i] = returns(key[i]);
                    return arr;
                };
                this.setItem = function(key, value) {
                    value = JSON.stringify(value);
                    return $.support[method] ? window[method].setItem(key, value) : $.cookie(options.cookiePrefix + key, value, options.cookieOptions);
                };
                this.removeItem = function(key) {
                    return $.support[method] ? window[method].removeItem(key) : $.cookie(options.cookiePrefix + key, null, $.extend(options.cookieOptions, {
                        expires: -1
                    }));
                };
                this.clear = function() {
                    if ($.support[method]) {
                        return window[method].clear();
                    } else {
                        var reg = new RegExp("^" + options.cookiePrefix, ""), opts = $.extend(options.cookieOptions, {
                            expires: -1
                        });
                        if (document.cookie && document.cookie !== "") {
                            $.map(document.cookie.split(";"), function(cookie) {
                                if (reg.test(cookie = $.trim(cookie))) {
                                    $.cookie(cookie.substr(0, cookie.indexOf("=")), null, opts);
                                }
                            });
                        }
                    }
                };
                if (typeof key !== "undefined") {
                    return typeof value !== "undefined" ? value === null ? this.removeItem(key) : this.setItem(key, value) : this.getItem(key);
                }
                return this;
            };
            $[method].options = defaults;
        });
    })(jQuery, window, document);
});
