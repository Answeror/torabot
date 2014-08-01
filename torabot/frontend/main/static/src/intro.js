define(function(require, exports, module){
    require('./init');
    require('./introjs.min.css');
    var introJs = require('./introjs').introJs;
    Cookie = require('cookie');
    var self = {
        init: function(options){
            self.options = options;

            $('body').addClass('intro');
            var restore = function() {
                $('body').removeClass('intro');
            };
            var exit = function(){
                restore();
                Cookie.set('intro', '0', {path: '/'});
                setTimeout(function(){
                    introJs().setOptions({
                        steps: [
                            {
                                element: '#start-intro',
                                intro: '点击这里重新开始教程, 点击背景结束教程.',
                                position: 'top'
                            }
                        ],
                        showStepNumbers: false,
                        exitOnOverlayClick: true,
                        scrollToElement: true,
                        showButtons: false,
                        showBullets: false
                    }).start();
                }, 0);
            };
            var nextpage = '<strong class=text-success>进入下一页</strong>';
            if (['/', '/intro'].contains($(location).prop('pathname'))) {
                introJs().setOptions({
                    steps: [
                        {
                            intro: '欢迎来到torabot. Torabot是一个网络事件订阅工具, 您可以订阅感兴趣的新番, 画师等, 在目标更新时您会收到来自torabot的邮件通知. 这个1分钟教程将引导您快速上手torabot.'
                        },
                        {
                            element: '.intro-select-mod',
                            intro: '从这里选择感兴趣的模块. 假设您希望使用torabot在虎穴抢本子.',
                            position: 'bottom'
                        },
                        {
                            element: '.intro-query',
                            intro: '填写查询条件. 例如您想订阅东方相关的本子信息, 就填入"东方".',
                            position: 'bottom'
                        },
                        {
                            element: '.intro-search',
                            intro: '点击这里开始搜索.',
                            position: 'bottom'
                        }
                    ],
                    nextLabel: '下一步',
                    prevLabel: '上一步',
                    skipLabel: '跳过教程',
                    doneLabel: nextpage,
                    tooltipClass: 'intro-tooltip',
                    showStepNumbers: false,
                    exitOnOverlayClick: true,
                    scrollToElement: true,
                    showButtons: true,
                    showBullets: true
                }).onbeforechange(function(e){
                    var $e = $(e);
                    if ($e.hasClass('intro-query')) {
                        $e.find('input[name="q"]').prop('value', '东方');
                    }
                }).onexit(exit).oncomplete(function(){
                    restore();
                    $('.intro-search').click();
                }).start();
            } else if ($(location).prop('pathname') == '/search/tora') {
                introJs().setOptions({
                    steps: [
                        {
                            element: '.intro-watch',
                            intro: '如果您已经登录, 点击该按钮订阅该查询, 当查询结果更新时即可收到通知.',
                            position: 'bottom'
                        },
                        {
                            element: '.intro-advanced-search',
                            intro: '您可能并不满足于简单查询, 点击这里进行高级搜索. 下面我们来试试订阅pixiv日榜.',
                            position: 'bottom'
                        }
                    ],
                    nextLabel: '下一步',
                    prevLabel: '上一步',
                    skipLabel: '跳过教程',
                    doneLabel: nextpage,
                    tooltipClass: 'intro-tooltip',
                    showStepNumbers: false,
                    exitOnOverlayClick: true,
                    scrollToElement: true,
                    showButtons: true,
                    showBullets: true
                }).onexit(exit).oncomplete(function(){
                    restore();
                    $(location).attr('href', self.options.pixiv_search_options_uri);
                }).start();
            } else if ($(location).prop('pathname') == '/search/advanced/pixiv') {
                introJs().setOptions({
                    steps: [
                        {
                            element: '.intro-pixiv-methods',
                            intro: '高级搜索里通常包含多种搜索方式.',
                            position: 'bottom'
                        },
                        {
                            element: '.intro-pixiv-ranking-form',
                            intro: '指定搜索条件, 系统会自动记录下每日新上榜的作品, 并邮件通知您.',
                            position: 'bottom'
                        }
                    ],
                    nextLabel: '下一步',
                    prevLabel: '上一步',
                    skipLabel: '跳过教程',
                    doneLabel: nextpage,
                    tooltipClass: 'intro-tooltip',
                    showStepNumbers: false,
                    exitOnOverlayClick: true,
                    scrollToElement: true,
                    showButtons: true,
                    showBullets: true
                }).onexit(exit).oncomplete(function(){
                    restore();
                    $(location).attr('href', self.options.pixiv_search_result_uri);
                }).start();
            } else if ($(location).prop('pathname') == '/search/pixiv') {
                introJs().setOptions({
                    steps: [
                        {
                            element: '.intro-help',
                            intro: '现在您已经学会了torabot的基本使用方法. 如果需要进一步了解各个模块的功能, 请在下拉菜单选择模块, 然后猛戳这里 :)',
                            position: 'bottom'
                        }
                    ],
                    nextLabel: '下一步',
                    prevLabel: '上一步',
                    skipLabel: '跳过教程',
                    doneLabel: '开始使用torabot',
                    showStepNumbers: false,
                    exitOnOverlayClick: true,
                    scrollToElement: true,
                    showButtons: true,
                    showBullets: false
                }).onexit(exit).oncomplete(exit).start();
            }
        }
    };
    exports.init = self.init;
});
