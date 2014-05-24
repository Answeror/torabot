define(function(require){
    require('./moment/moment');
    require('./moment/lang/zh-cn');
    $('.momentjs').each(function() {
        $this = $(this);
        $this.text(function() {
            var format = $this.data('format');
            if (format == 'fromnow') return moment($this.text()).fromNow();
            if (format == 'calendar') return moment($this.text()).calendar();
            return moment($this.text()).format(format);
        }());
    });
});
