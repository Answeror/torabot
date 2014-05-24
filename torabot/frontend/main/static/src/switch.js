define(function(require){
    require('./bootstrap-switch/bootstrap-switch');
    $('.dropdown-menu .bootstrap-switch').click(function(e) {
        e.stopPropagation();
    });
});
