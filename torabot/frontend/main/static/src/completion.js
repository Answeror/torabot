define(function(require, exports, module){
    exports.make = function(options){
        options = $.extend({source: null}, options);
        var self = {
            _activated: false,
            activated: function() { return self._activated; },
            activate: function(){
                if (self._activated) return;
                var last_query = null;
                var update_query = function(suggestion, options){
                    options = $.extend({
                        query: null,
                        set: function(value){
                            return require('./search').$q.val(value);
                        }
                    }, options);
                    var query = options.query;
                    if (!query) {
                        last_query = query = require('./search').$q.typeahead('val');
                    }
                    var tags = query.split(' ').slice(0, -1);
                    tags.push(suggestion.value);
                    return options.set(tags.join(' '));
                };
                require('./search').$q.typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1
                }, {
                    name: 'completion',
                    displayKey: 'value',
                    source: options.source,
                    templates: {
                        suggestion: require('handlebars').compile([
                            "<p class=completion-item>",
                            "<strong class=ellipsis>{{value}}</strong>",
                            "{{#if alias}}<br>{{#each alias}}<span class='ellipsis label label-default'>{{value}}</span> {{/each}}{{/if}}",
                            "</p>"
                        ].join(''))
                    }
                }).on('typeahead:cursorchanged', function(e, suggestion, dataset){
                    update_query(suggestion);
                    e.preventDefault();
                }).on('typeahead:selected', function(e, suggestion, dataset){
                    var $this = $(this);
                    update_query(suggestion, {
                        query: last_query,
                        set: function(value) { return $this.typeahead('val', value); }
                    });
                    e.preventDefault();
                });
                self._activated = true;
            },
            deactivate: function(){
                if (!self._activated) return;
                require('./search').$q.typeahead('destroy');
                self._activated = false;
            }
        };
        return self;
    };
});
