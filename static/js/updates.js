var urlpath = new URL(window.location.href).pathname;
var paths = urlpath.split('/');

var board_prefix = paths[1];
var thread_id = paths[2];

var last_thread_id = 0;
var last_post_id = 0;

var update_posts = function(message) {
    var ajax;

    if (message == undefined) {
        ajax = $.ajax({
            url: '/api/board/' + board_prefix + '/thread/' + thread_id,
            method: 'GET',
            data: {
                'last_id': last_post_id
            }
        });
    }
    else {
        ajax = $.ajax({
            url: '/api/board/' + board_prefix + '/thread/' + thread_id,
            method: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'message': message,
                'last_id': last_post_id
            }, null, '\t')
        });
    }

    ajax.done(function(result) {
        var postsString = $('#posts').html();
        for (var post in result) {
            postsString += '<br><h5><p>' + result[post].datetime + ': ' + result[post].message + '</p></h5>';
        }
        if (result.length > 1) last_post_id = result[result.length - 1].id
        $('#posts').html(postsString);
    });
}

var update_threads = function(title, message) {
    var ajax;

    if (message == undefined) {
        ajax = $.ajax({
            url: '/api/board/' + board_prefix,
            method: 'GET',
            data: {
                'last_id': last_thread_id
            }
        });
    }
    else {
        ajax = $.ajax({
            url: '/api/board/' + board_prefix,
            method: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'title': title,
                'message': message
            }, null, '\t')
        });
    }

    ajax.done(function(result) {
        var threadsString = $('#threads').html();
        for (var thread in result) {
            var link = '/' + board_prefix + '/' + result[thread].id + '/';
            threadsString += '<p><a href="' + link + '">' + result[thread].title + '</a></p>';
        }
        if (result.length > 1) last_thread_id = result[result.length - 1].id;
        $('#threads').html(threadsString);
    });
}

// Select update function to loop
if (board_prefix != '') {
    if (thread_id != '') {
        update_posts();
        setInterval(update_posts, 3000)     // Every 3 sec
    }
    else {
        update_threads();
        setInterval(update_threads, 10000)  // Every 10 sec
    }
}
