// PhantomJS script
// Takes screeshot of a given page. This correctly handles pages which
// dynamically load content making AJAX requests.

// Instead of waiting fixed amount of time before rendering, we give a short
// time for the page to make additional requests.


var render = function(url, file){
    var ajax_timeout = 2000;
    var timeout = 10000;
    var request_count = 0;
    var ajax_timer;
    var page = require('webpage').create();
    page.viewportSize = {
        width: 1280,
        height: 800
    };
    // silence confirmation messages and errors
    page.onConfirm = page.onPrompt = page.onError = function(){};
    page.onResourceRequested = function(request) {
        request_count += 1;
        clearTimeout(ajax_timer);
    };
    page.onResourceReceived = function(response) {
        if (!response.stage || response.stage === 'end') {
            request_count -= 1;
            if (request_count === 0) {
                ajax_timer = setTimeout(render_and_exit, ajax_timeout);
            }
        }
    };
    function render_and_exit() {
        page.render(file);
        phantom.exit();
    }
    page.open(url, function(status) {
        if (status !== "success") {
            console.error('Unable to load url:', url);
            phantom.exit(1);
        } else {
            setTimeout(render_and_exit, timeout);
        }
    });
};

function die(error) {
    console.error(error);
    phantom.exit(1);
}

function main() {
    var args = require('system').args;
    if (args.length < 3) {
        return die('wrong args: [uri] [file]');
    }
    render(args[1], args[2]);
}

main();
