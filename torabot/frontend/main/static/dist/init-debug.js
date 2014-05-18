define("torabot/main/0.1.0/init-debug", [ "seajs/seajs-style/1.0.2/seajs-style-debug", "./ut-debug", "./search-debug", "arale/cookie/1.0.2/cookie-debug", "./intro-debug", "./introjs.min-debug.css", "./introjs-debug" ], function(require) {
    require("seajs/seajs-style/1.0.2/seajs-style-debug");
    require("./ut-debug");
    require("./search-debug");
    Cookie = require("arale/cookie/1.0.2/cookie-debug");
    if (Cookie.get("intro") != "0") {
        require("./intro-debug");
    }
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
});

define("torabot/main/0.1.0/search-debug", [], function(require, exports, module) {
    $(function() {
        $.torabot = {};
        $.torabot.cast = function(type, value) {
            return {
                text: function(x) {
                    return x.toString();
                },
                "int": parseInt
            }[type](value);
        };
    });
    $(function() {
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
    });
    $(function() {
        var form = $('form[name="search"]');
        var $q = form.find('input[name="q"]');
        var $mods = form.find('select[name="kind"]');
        form.find('button[name="help"]').click(function(e) {
            e.preventDefault();
            $(location).attr("href", "/help/" + $mods.find("option:selected").val());
        });
        var $search = form.find('button[name="search"]');
        $search.click(function(e) {
            e.preventDefault();
            var $selected = $mods.find("option:selected");
            var kind = $selected.val();
            var text = $q.val();
            if (!text && !$selected.data("allow-empty-query")) {
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
        var $advanced = form.find('button[name="advanced"]');
        $advanced.click(function(e) {
            e.preventDefault();
            $(location).attr("href", "/search/advanced/" + $mods.find("option:selected").val());
        });
        var $buttons = form.find('span[name="buttons"]');
        var on_change_mod = function() {
            var $selected = $(this).find("option:selected");
            $advanced.prop("disabled", !$selected.data("has-advanced-search"));
            $q.prop("disabled", !$selected.data("has-normal-search"));
            $search.prop("disabled", !$selected.data("has-normal-search"));
            if ($selected.data("has-normal-search")) {
                $q.prop("placeholder", $selected.data("normal-search-prompt"));
            } else {
                $q.prop("placeholder", "请使用高级搜索");
            }
        };
        $mods.ready(on_change_mod).change(on_change_mod);
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

define("torabot/main/0.1.0/intro-debug", [ "torabot/main/0.1.0/introjs-debug", "arale/cookie/1.0.2/cookie-debug" ], function(require, exports, module) {
    require("torabot/main/0.1.0/introjs.min-debug.css");
    var introJs = require("torabot/main/0.1.0/introjs-debug").introJs;
    Cookie = require("arale/cookie/1.0.2/cookie-debug");
    $(function() {
        $("body").addClass("intro");
        $(".navbar").removeClass("navbar-fixed-top");
        var restore = function() {
            $("body").removeClass("intro");
            $(".navbar").addClass("navbar-fixed-top");
        };
        var exit = function() {
            restore();
            Cookie.set("intro", "0", {
                path: "/"
            });
            setTimeout(function() {
                introJs().setOptions({
                    steps: [ {
                        element: "#start-intro",
                        intro: "点击这里重新开始教程, 点击背景结束教程.",
                        position: "top"
                    } ],
                    showStepNumbers: false,
                    exitOnOverlayClick: true,
                    scrollToElement: true,
                    showButtons: false,
                    showBullets: false
                }).start();
            }, 0);
        };
        var nextpage = "<strong class=text-success>进入下一页</strong>";
        if ([ "/", "/intro" ].contains($(location).prop("pathname"))) {
            introJs().setOptions({
                steps: [ {
                    intro: "欢迎来到torabot. Torabot是一个网络事件订阅工具, 您可以订阅感兴趣的新番, 画师等, 在目标更新时您会收到来自torabot的邮件通知. 这个1分钟教程将引导您快速上手torabot."
                }, {
                    element: ".intro-select-mod",
                    intro: "从这里选择感兴趣的模块. 假设您希望使用torabot在虎穴抢本子.",
                    position: "bottom"
                }, {
                    element: ".intro-query",
                    intro: '填写查询条件. 例如您想订阅东方相关的本子信息, 就填入"东方".',
                    position: "bottom"
                }, {
                    element: ".intro-search",
                    intro: "点击这里开始搜索.",
                    position: "bottom"
                } ],
                nextLabel: "下一步",
                prevLabel: "上一步",
                skipLabel: "跳过教程",
                doneLabel: nextpage,
                tooltipClass: "intro-tooltip",
                showStepNumbers: false,
                exitOnOverlayClick: true,
                scrollToElement: true,
                showButtons: true,
                showBullets: true
            }).onbeforechange(function(e) {
                var $e = $(e);
                if ($e.hasClass("intro-query")) {
                    $e.prop("value", "东方");
                }
            }).onexit(exit).oncomplete(function() {
                restore();
                $(".intro-search").click();
            }).start();
        } else if ($(location).prop("pathname") == "/search/tora") {
            introJs().setOptions({
                steps: [ {
                    element: ".intro-watch",
                    intro: "如果您已经登录, 点击该按钮订阅该查询, 当查询结果更新时即可收到通知.",
                    position: "bottom"
                }, {
                    element: ".intro-advanced-search",
                    intro: "您可能并不满足于简单查询, 点击这里进行高级搜索. 下面我们来试试订阅pixiv日榜.",
                    position: "bottom"
                } ],
                nextLabel: "下一步",
                prevLabel: "上一步",
                skipLabel: "跳过教程",
                doneLabel: nextpage,
                tooltipClass: "intro-tooltip",
                showStepNumbers: false,
                exitOnOverlayClick: true,
                scrollToElement: true,
                showButtons: true,
                showBullets: true
            }).onexit(exit).oncomplete(function() {
                restore();
                $(location).attr("href", '{{ url_for("main.advanced_search", kind="pixiv", method="ranking") }}');
            }).start();
        } else if ($(location).prop("pathname") == "/search/advanced/pixiv") {
            introJs().setOptions({
                steps: [ {
                    element: ".intro-pixiv-methods",
                    intro: "高级搜索里通常包含多种搜索方式.",
                    position: "bottom"
                }, {
                    element: ".intro-pixiv-ranking-form",
                    intro: "指定搜索条件, 系统会自动记录下每日新上榜的作品, 并邮件通知您.",
                    position: "bottom"
                } ],
                nextLabel: "下一步",
                prevLabel: "上一步",
                skipLabel: "跳过教程",
                doneLabel: nextpage,
                tooltipClass: "intro-tooltip",
                showStepNumbers: false,
                exitOnOverlayClick: true,
                scrollToElement: true,
                showButtons: true,
                showBullets: true
            }).onexit(exit).oncomplete(function() {
                restore();
                $(location).attr("href", '{{ url_for("main.search", kind="pixiv", method="ranking", mode="daily", limit=10)|safe }}');
            }).start();
        } else if ($(location).prop("pathname") == "/search/pixiv") {
            introJs().setOptions({
                steps: [ {
                    element: ".intro-help",
                    intro: "现在您已经学会了torabot的基本使用方法. 如果需要进一步了解各个模块的功能, 请在下拉菜单选择模块, 然后猛戳这里 :)",
                    position: "bottom"
                } ],
                nextLabel: "下一步",
                prevLabel: "上一步",
                skipLabel: "跳过教程",
                doneLabel: "开始使用torabot",
                showStepNumbers: false,
                exitOnOverlayClick: true,
                scrollToElement: true,
                showButtons: true,
                showBullets: false
            }).onexit(exit).oncomplete(exit).start();
        }
    });
});

define("torabot/main/0.1.0/introjs.min-debug.css", [], function() {
    seajs.importStyle(".introjs-overlay{position:absolute;z-index:999999;background-color:#000;opacity:0;background:-moz-radial-gradient(center,ellipse cover,rgba(0,0,0,.4) 0,rgba(0,0,0,.9) 100%);background:-webkit-gradient(radial,center center,0,center center,100%,color-stop(0%,rgba(0,0,0,.4)),color-stop(100%,rgba(0,0,0,.9)));background:-webkit-radial-gradient(center,ellipse cover,rgba(0,0,0,.4) 0,rgba(0,0,0,.9) 100%);background:-o-radial-gradient(center,ellipse cover,rgba(0,0,0,.4) 0,rgba(0,0,0,.9) 100%);background:-ms-radial-gradient(center,ellipse cover,rgba(0,0,0,.4) 0,rgba(0,0,0,.9) 100%);background:radial-gradient(center,ellipse cover,rgba(0,0,0,.4) 0,rgba(0,0,0,.9) 100%);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#66000000', endColorstr='#e6000000', GradientType=1);-ms-filter:\"alpha(opacity=50)\";filter:alpha(opacity=50);-webkit-transition:all .3s ease-out;-moz-transition:all .3s ease-out;-ms-transition:all .3s ease-out;-o-transition:all .3s ease-out;transition:all .3s ease-out}.introjs-fixParent{z-index:auto!important;opacity:1!important}.introjs-showElement{z-index:9999999!important}.introjs-relativePosition{position:relative}.introjs-helperLayer{position:absolute;z-index:9999998;background-color:#FFF;background-color:rgba(255,255,255,.9);border:1px solid #777;border:1px solid rgba(0,0,0,.5);border-radius:4px;box-shadow:0 2px 15px rgba(0,0,0,.4);-webkit-transition:all .3s ease-out;-moz-transition:all .3s ease-out;-ms-transition:all .3s ease-out;-o-transition:all .3s ease-out;transition:all .3s ease-out}.introjs-helperNumberLayer{position:absolute;top:-16px;left:-16px;z-index:9999999999!important;padding:2px;font-family:Arial,verdana,tahoma;font-size:13px;font-weight:700;color:#fff;text-align:center;text-shadow:1px 1px 1px rgba(0,0,0,.3);background:#ff3019;background:-webkit-linear-gradient(top,#ff3019 0,#cf0404 100%);background:-webkit-gradient(linear,left top,left bottom,color-stop(0%,#ff3019),color-stop(100%,#cf0404));background:-moz-linear-gradient(top,#ff3019 0,#cf0404 100%);background:-ms-linear-gradient(top,#ff3019 0,#cf0404 100%);background:-o-linear-gradient(top,#ff3019 0,#cf0404 100%);background:linear-gradient(to bottom,#ff3019 0,#cf0404 100%);width:20px;height:20px;line-height:20px;border:3px solid #fff;border-radius:50%;filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ff3019', endColorstr='#cf0404', GradientType=0);filter:progid:DXImageTransform.Microsoft.Shadow(direction=135, strength=2, color=ff0000);box-shadow:0 2px 5px rgba(0,0,0,.4)}.introjs-arrow{border:5px solid #fff;content:'';position:absolute}.introjs-arrow.top{top:-10px;border-top-color:transparent;border-right-color:transparent;border-bottom-color:#fff;border-left-color:transparent}.introjs-arrow.right{right:-10px;top:10px;border-top-color:transparent;border-right-color:transparent;border-bottom-color:transparent;border-left-color:#fff}.introjs-arrow.bottom{bottom:-10px;border-top-color:#fff;border-right-color:transparent;border-bottom-color:transparent;border-left-color:transparent}.introjs-arrow.left{left:-10px;top:10px;border-top-color:transparent;border-right-color:#fff;border-bottom-color:transparent;border-left-color:transparent}.introjs-tooltip{position:absolute;padding:10px;background-color:#fff;min-width:200px;max-width:300px;border-radius:3px;box-shadow:0 1px 10px rgba(0,0,0,.4);-webkit-transition:opacity .1s ease-out;-moz-transition:opacity .1s ease-out;-ms-transition:opacity .1s ease-out;-o-transition:opacity .1s ease-out;transition:opacity .1s ease-out}.introjs-tooltipbuttons{text-align:right}.introjs-button{position:relative;overflow:visible;display:inline-block;padding:.3em .8em;border:1px solid #d4d4d4;margin:0;text-decoration:none;text-shadow:1px 1px 0 #fff;font:11px/normal sans-serif;color:#333;white-space:nowrap;cursor:pointer;outline:0;background-color:#ececec;background-image:-webkit-gradient(linear,0 0,0 100%,from(#f4f4f4),to(#ececec));background-image:-moz-linear-gradient(#f4f4f4,#ececec);background-image:-o-linear-gradient(#f4f4f4,#ececec);background-image:linear-gradient(#f4f4f4,#ececec);-webkit-background-clip:padding;-moz-background-clip:padding;-o-background-clip:padding-box;-webkit-border-radius:.2em;-moz-border-radius:.2em;border-radius:.2em;zoom:1;*display:inline;margin-top:10px}.introjs-button:hover{border-color:#bcbcbc;text-decoration:none;box-shadow:0 1px 1px #e3e3e3}.introjs-button:focus,.introjs-button:active{background-image:-webkit-gradient(linear,0 0,0 100%,from(#ececec),to(#f4f4f4));background-image:-moz-linear-gradient(#ececec,#f4f4f4);background-image:-o-linear-gradient(#ececec,#f4f4f4);background-image:linear-gradient(#ececec,#f4f4f4)}.introjs-button::-moz-focus-inner{padding:0;border:0}.introjs-skipbutton{margin-right:5px;color:#7a7a7a}.introjs-prevbutton{-webkit-border-radius:.2em 0 0 .2em;-moz-border-radius:.2em 0 0 .2em;border-radius:.2em 0 0 .2em;border-right:0}.introjs-nextbutton{-webkit-border-radius:0 .2em .2em 0;-moz-border-radius:0 .2em .2em 0;border-radius:0 .2em .2em 0}.introjs-disabled,.introjs-disabled:hover,.introjs-disabled:focus{color:#9a9a9a;border-color:#d4d4d4;box-shadow:none;cursor:default;background-color:#f4f4f4;background-image:none;text-decoration:none}.introjs-bullets{text-align:center}.introjs-bullets ul{clear:both;margin:15px auto 0;padding:0;display:inline-block}.introjs-bullets ul li{list-style:none;float:left;margin:0 2px}.introjs-bullets ul li a{display:block;width:6px;height:6px;background:#ccc;border-radius:10px;-moz-border-radius:10px;-webkit-border-radius:10px;text-decoration:none}.introjs-bullets ul li a:hover{background:#999}.introjs-bullets ul li a.active{background:#999}.introjsFloatingElement{position:absolute;height:0;width:0;left:50%;top:50%}");
});

define("torabot/main/0.1.0/introjs-debug", [], function(require, exports, module) {
    (function(q, f) {
        "object" === typeof exports ? f(exports) : "function" === typeof define && define.amd ? define([ "exports" ], f) : f(q);
    })(this, function(q) {
        function f(a) {
            this._targetElement = a;
            this._options = {
                nextLabel: "Next &rarr;",
                prevLabel: "&larr; Back",
                skipLabel: "Skip",
                doneLabel: "Done",
                tooltipPosition: "bottom",
                tooltipClass: "",
                exitOnEsc: !0,
                exitOnOverlayClick: !0,
                showStepNumbers: !0,
                keyboardNavigation: !0,
                showButtons: !0,
                showBullets: !0,
                scrollToElement: !0
            };
        }
        function s(a) {
            if (null == a || "object" != typeof a || "undefined" != typeof a.nodeType) return a;
            var b = {}, c;
            for (c in a) b[c] = s(a[c]);
            return b;
        }
        function t() {
            this._direction = "forward";
            "undefined" === typeof this._currentStep ? this._currentStep = 0 : ++this._currentStep;
            if (this._introItems.length <= this._currentStep) "function" === typeof this._introCompleteCallback && this._introCompleteCallback.call(this), 
            u.call(this, this._targetElement); else {
                var a = this._introItems[this._currentStep];
                "undefined" !== typeof this._introBeforeChangeCallback && this._introBeforeChangeCallback.call(this, a.element);
                A.call(this, a);
            }
        }
        function y() {
            this._direction = "backward";
            if (0 === this._currentStep) return !1;
            var a = this._introItems[--this._currentStep];
            "undefined" !== typeof this._introBeforeChangeCallback && this._introBeforeChangeCallback.call(this, a.element);
            A.call(this, a);
        }
        function u(a) {
            var b = a.querySelector(".introjs-overlay");
            if (null != b) {
                b.style.opacity = 0;
                setTimeout(function() {
                    b.parentNode && b.parentNode.removeChild(b);
                }, 500);
                (a = a.querySelector(".introjs-helperLayer")) && a.parentNode.removeChild(a);
                (a = document.querySelector(".introjsFloatingElement")) && a.parentNode.removeChild(a);
                if (a = document.querySelector(".introjs-showElement")) a.className = a.className.replace(/introjs-[a-zA-Z]+/g, "").replace(/^\s+|\s+$/g, "");
                if ((a = document.querySelectorAll(".introjs-fixParent")) && 0 < a.length) for (var c = a.length - 1; 0 <= c; c--) a[c].className = a[c].className.replace(/introjs-fixParent/g, "").replace(/^\s+|\s+$/g, "");
                window.removeEventListener ? window.removeEventListener("keydown", this._onKeyDown, !0) : document.detachEvent && document.detachEvent("onkeydown", this._onKeyDown);
                this._currentStep = void 0;
            }
        }
        function B(a, b, c, d) {
            b.style.top = null;
            b.style.right = null;
            b.style.bottom = null;
            b.style.left = null;
            b.style.marginLeft = null;
            b.style.marginTop = null;
            c.style.display = "inherit";
            "undefined" != typeof d && null != d && (d.style.top = null, d.style.left = null);
            if (this._introItems[this._currentStep]) {
                var e = "", e = this._introItems[this._currentStep], e = "string" === typeof e.tooltipClass ? e.tooltipClass : this._options.tooltipClass;
                b.className = ("introjs-tooltip " + e).replace(/^\s+|\s+$/g, "");
                switch (this._introItems[this._currentStep].position) {
                  case "top":
                    b.style.left = "15px";
                    b.style.top = "-" + (p(b).height + 10) + "px";
                    c.className = "introjs-arrow bottom";
                    break;

                  case "right":
                    b.style.left = p(a).width + 20 + "px";
                    c.className = "introjs-arrow left";
                    break;

                  case "left":
                    !0 == this._options.showStepNumbers && (b.style.top = "15px");
                    b.style.right = p(a).width + 20 + "px";
                    c.className = "introjs-arrow right";
                    break;

                  case "floating":
                    c.style.display = "none";
                    a = p(b);
                    b.style.left = "50%";
                    b.style.top = "50%";
                    b.style.marginLeft = "-" + a.width / 2 + "px";
                    b.style.marginTop = "-" + a.height / 2 + "px";
                    "undefined" != typeof d && null != d && (d.style.left = "-" + (a.width / 2 + 18) + "px", 
                    d.style.top = "-" + (a.height / 2 + 18) + "px");
                    break;

                  default:
                    b.style.bottom = "-" + (p(b).height + 10) + "px", c.className = "introjs-arrow top";
                }
            }
        }
        function w(a) {
            if (a && this._introItems[this._currentStep]) {
                var b = this._introItems[this._currentStep], c = p(b.element), d = 10;
                "floating" == b.position && (d = 0);
                a.setAttribute("style", "width: " + (c.width + d) + "px; height:" + (c.height + d) + "px; top:" + (c.top - 5) + "px;left: " + (c.left - 5) + "px;");
            }
        }
        function A(a) {
            var b;
            "undefined" !== typeof this._introChangeCallback && this._introChangeCallback.call(this, a.element);
            var c = this, d = document.querySelector(".introjs-helperLayer");
            p(a.element);
            if (null != d) {
                var e = d.querySelector(".introjs-helperNumberLayer"), C = d.querySelector(".introjs-tooltiptext"), g = d.querySelector(".introjs-arrow"), n = d.querySelector(".introjs-tooltip"), j = d.querySelector(".introjs-skipbutton"), m = d.querySelector(".introjs-prevbutton"), k = d.querySelector(".introjs-nextbutton");
                n.style.opacity = 0;
                if (null != e && (b = this._introItems[0 <= a.step - 2 ? a.step - 2 : 0], null != b && "forward" == this._direction && "floating" == b.position || "backward" == this._direction && "floating" == a.position)) e.style.opacity = 0;
                w.call(c, d);
                var l = document.querySelectorAll(".introjs-fixParent");
                if (l && 0 < l.length) for (b = l.length - 1; 0 <= b; b--) l[b].className = l[b].className.replace(/introjs-fixParent/g, "").replace(/^\s+|\s+$/g, "");
                b = document.querySelector(".introjs-showElement");
                b.className = b.className.replace(/introjs-[a-zA-Z]+/g, "").replace(/^\s+|\s+$/g, "");
                c._lastShowElementTimer && clearTimeout(c._lastShowElementTimer);
                c._lastShowElementTimer = setTimeout(function() {
                    null != e && (e.innerHTML = a.step);
                    C.innerHTML = a.intro;
                    B.call(c, a.element, n, g, e);
                    d.querySelector(".introjs-bullets li > a.active").className = "";
                    d.querySelector('.introjs-bullets li > a[data-stepnumber="' + a.step + '"]').className = "active";
                    n.style.opacity = 1;
                    e.style.opacity = 1;
                }, 350);
            } else {
                var j = document.createElement("div"), l = document.createElement("div"), h = document.createElement("div"), m = document.createElement("div"), k = document.createElement("div"), f = document.createElement("div");
                j.className = "introjs-helperLayer";
                w.call(c, j);
                this._targetElement.appendChild(j);
                l.className = "introjs-arrow";
                m.className = "introjs-tooltiptext";
                m.innerHTML = a.intro;
                k.className = "introjs-bullets";
                !1 === this._options.showBullets && (k.style.display = "none");
                var q = document.createElement("ul");
                b = 0;
                for (var v = this._introItems.length; b < v; b++) {
                    var s = document.createElement("li"), r = document.createElement("a");
                    r.onclick = function() {
                        c.goToStep(this.getAttribute("data-stepnumber"));
                    };
                    0 === b && (r.className = "active");
                    r.href = "javascript:void(0);";
                    r.innerHTML = "&nbsp;";
                    r.setAttribute("data-stepnumber", this._introItems[b].step);
                    s.appendChild(r);
                    q.appendChild(s);
                }
                k.appendChild(q);
                f.className = "introjs-tooltipbuttons";
                !1 === this._options.showButtons && (f.style.display = "none");
                h.className = "introjs-tooltip";
                h.appendChild(m);
                h.appendChild(k);
                if (!0 == this._options.showStepNumbers) {
                    var x = document.createElement("span");
                    x.className = "introjs-helperNumberLayer";
                    x.innerHTML = a.step;
                    j.appendChild(x);
                }
                h.appendChild(l);
                j.appendChild(h);
                k = document.createElement("a");
                k.onclick = function() {
                    c._introItems.length - 1 != c._currentStep && t.call(c);
                };
                k.href = "javascript:void(0);";
                k.innerHTML = this._options.nextLabel;
                m = document.createElement("a");
                m.onclick = function() {
                    0 != c._currentStep && y.call(c);
                };
                m.href = "javascript:void(0);";
                m.innerHTML = this._options.prevLabel;
                j = document.createElement("a");
                j.className = "introjs-button introjs-skipbutton";
                j.href = "javascript:void(0);";
                j.innerHTML = this._options.skipLabel;
                j.onclick = function() {
                    c._introItems.length - 1 == c._currentStep && "function" === typeof c._introCompleteCallback && c._introCompleteCallback.call(c);
                    c._introItems.length - 1 != c._currentStep && "function" === typeof c._introExitCallback && c._introExitCallback.call(c);
                    u.call(c, c._targetElement);
                };
                f.appendChild(j);
                1 < this._introItems.length && (f.appendChild(m), f.appendChild(k));
                h.appendChild(f);
                B.call(c, a.element, h, l, x);
            }
            0 == this._currentStep && 1 < this._introItems.length ? (m.className = "introjs-button introjs-prevbutton introjs-disabled", 
            k.className = "introjs-button introjs-nextbutton", j.innerHTML = this._options.skipLabel) : this._introItems.length - 1 == this._currentStep || 1 == this._introItems.length ? (j.innerHTML = this._options.doneLabel, 
            m.className = "introjs-button introjs-prevbutton", k.className = "introjs-button introjs-nextbutton introjs-disabled") : (m.className = "introjs-button introjs-prevbutton", 
            k.className = "introjs-button introjs-nextbutton", j.innerHTML = this._options.skipLabel);
            k.focus();
            a.element.className += " introjs-showElement";
            b = z(a.element, "position");
            "absolute" !== b && "relative" !== b && (a.element.className += " introjs-relativePosition");
            for (b = a.element.parentNode; null != b && "body" !== b.tagName.toLowerCase(); ) {
                l = z(b, "z-index");
                h = parseFloat(z(b, "opacity"));
                if (/[0-9]+/.test(l) || 1 > h) b.className += " introjs-fixParent";
                b = b.parentNode;
            }
            b = a.element.getBoundingClientRect();
            !(0 <= b.top && 0 <= b.left && b.bottom + 80 <= window.innerHeight && b.right <= window.innerWidth) && !0 === this._options.scrollToElement && (h = a.element.getBoundingClientRect(), 
            b = void 0 != window.innerWidth ? window.innerHeight : document.documentElement.clientHeight, 
            l = h.bottom - (h.bottom - h.top), h = h.bottom - b, 0 > l || a.element.clientHeight > b ? window.scrollBy(0, l - 30) : window.scrollBy(0, h + 100));
            "undefined" !== typeof this._introAfterChangeCallback && this._introAfterChangeCallback.call(this, a.element);
        }
        function z(a, b) {
            var c = "";
            a.currentStyle ? c = a.currentStyle[b] : document.defaultView && document.defaultView.getComputedStyle && (c = document.defaultView.getComputedStyle(a, null).getPropertyValue(b));
            return c && c.toLowerCase ? c.toLowerCase() : c;
        }
        function D(a) {
            var b = document.createElement("div"), c = "", d = this;
            b.className = "introjs-overlay";
            if ("body" === a.tagName.toLowerCase()) c += "top: 0;bottom: 0; left: 0;right: 0;position: fixed;", 
            b.setAttribute("style", c); else {
                var e = p(a);
                e && (c += "width: " + e.width + "px; height:" + e.height + "px; top:" + e.top + "px;left: " + e.left + "px;", 
                b.setAttribute("style", c));
            }
            a.appendChild(b);
            b.onclick = function() {
                !0 == d._options.exitOnOverlayClick && (u.call(d, a), void 0 != d._introExitCallback && d._introExitCallback.call(d));
            };
            setTimeout(function() {
                c += "opacity: .8;";
                b.setAttribute("style", c);
            }, 10);
            return !0;
        }
        function p(a) {
            var b = {};
            b.width = a.offsetWidth;
            b.height = a.offsetHeight;
            for (var c = 0, d = 0; a && !isNaN(a.offsetLeft) && !isNaN(a.offsetTop); ) c += a.offsetLeft, 
            d += a.offsetTop, a = a.offsetParent;
            b.top = d;
            b.left = c;
            return b;
        }
        var v = function(a) {
            if ("object" === typeof a) return new f(a);
            if ("string" === typeof a) {
                if (a = document.querySelector(a)) return new f(a);
                throw Error("There is no element with given selector.");
            }
            return new f(document.body);
        };
        v.version = "0.8.0";
        v.fn = f.prototype = {
            clone: function() {
                return new f(this);
            },
            setOption: function(a, b) {
                this._options[a] = b;
                return this;
            },
            setOptions: function(a) {
                var b = this._options, c = {}, d;
                for (d in b) c[d] = b[d];
                for (d in a) c[d] = a[d];
                this._options = c;
                return this;
            },
            start: function() {
                a: {
                    var a = this._targetElement, b = [], c = this;
                    if (this._options.steps) for (var d = [], e = 0, d = this._options.steps.length; e < d; e++) {
                        var f = s(this._options.steps[e]);
                        f.step = b.length + 1;
                        "string" === typeof f.element && (f.element = document.querySelector(f.element));
                        if ("undefined" === typeof f.element || null == f.element) {
                            var g = document.querySelector(".introjsFloatingElement");
                            null == g && (g = document.createElement("div"), g.className = "introjsFloatingElement", 
                            document.body.appendChild(g));
                            f.element = g;
                            f.position = "floating";
                        }
                        null != f.element && b.push(f);
                    } else {
                        d = a.querySelectorAll("*[data-intro]");
                        if (1 > d.length) break a;
                        e = 0;
                        for (f = d.length; e < f; e++) {
                            var g = d[e], n = parseInt(g.getAttribute("data-step"), 10);
                            0 < n && (b[n - 1] = {
                                element: g,
                                intro: g.getAttribute("data-intro"),
                                step: parseInt(g.getAttribute("data-step"), 10),
                                tooltipClass: g.getAttribute("data-tooltipClass"),
                                position: g.getAttribute("data-position") || this._options.tooltipPosition
                            });
                        }
                        e = n = 0;
                        for (f = d.length; e < f; e++) if (g = d[e], null == g.getAttribute("data-step")) {
                            for (;"undefined" != typeof b[n]; ) n++;
                            b[n] = {
                                element: g,
                                intro: g.getAttribute("data-intro"),
                                step: n + 1,
                                tooltipClass: g.getAttribute("data-tooltipClass"),
                                position: g.getAttribute("data-position") || this._options.tooltipPosition
                            };
                        }
                    }
                    e = [];
                    for (d = 0; d < b.length; d++) b[d] && e.push(b[d]);
                    b = e;
                    b.sort(function(a, b) {
                        return a.step - b.step;
                    });
                    c._introItems = b;
                    D.call(c, a) && (t.call(c), a.querySelector(".introjs-skipbutton"), a.querySelector(".introjs-nextbutton"), 
                    c._onKeyDown = function(b) {
                        if (27 === b.keyCode && !0 == c._options.exitOnEsc) u.call(c, a), void 0 != c._introExitCallback && c._introExitCallback.call(c); else if (37 === b.keyCode) y.call(c); else if (39 === b.keyCode || 13 === b.keyCode) t.call(c), 
                        b.preventDefault ? b.preventDefault() : b.returnValue = !1;
                    }, c._onResize = function() {
                        w.call(c, document.querySelector(".introjs-helperLayer"));
                    }, window.addEventListener ? (this._options.keyboardNavigation && window.addEventListener("keydown", c._onKeyDown, !0), 
                    window.addEventListener("resize", c._onResize, !0)) : document.attachEvent && (this._options.keyboardNavigation && document.attachEvent("onkeydown", c._onKeyDown), 
                    document.attachEvent("onresize", c._onResize)));
                }
                return this;
            },
            goToStep: function(a) {
                this._currentStep = a - 2;
                "undefined" !== typeof this._introItems && t.call(this);
                return this;
            },
            nextStep: function() {
                t.call(this);
                return this;
            },
            previousStep: function() {
                y.call(this);
                return this;
            },
            exit: function() {
                u.call(this, this._targetElement);
            },
            refresh: function() {
                w.call(this, document.querySelector(".introjs-helperLayer"));
                return this;
            },
            onbeforechange: function(a) {
                if ("function" === typeof a) this._introBeforeChangeCallback = a; else throw Error("Provided callback for onbeforechange was not a function");
                return this;
            },
            onchange: function(a) {
                if ("function" === typeof a) this._introChangeCallback = a; else throw Error("Provided callback for onchange was not a function.");
                return this;
            },
            onafterchange: function(a) {
                if ("function" === typeof a) this._introAfterChangeCallback = a; else throw Error("Provided callback for onafterchange was not a function");
                return this;
            },
            oncomplete: function(a) {
                if ("function" === typeof a) this._introCompleteCallback = a; else throw Error("Provided callback for oncomplete was not a function.");
                return this;
            },
            onexit: function(a) {
                if ("function" === typeof a) this._introExitCallback = a; else throw Error("Provided callback for onexit was not a function.");
                return this;
            }
        };
        return q.introJs = v;
    });
});
