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
        }).done(function(result) {
            if (result['status'] == 'ok') {
                var posts = result['posts'];
                var postsString = $('#posts').html();

                for (var post in posts) {
                    postsString += '<br><h5><p>' + posts[post].datetime + ': ' + posts[post].message + '</p></h5>';
                }
                if (posts.length > 0) last_post_id = posts[posts.length - 1].id
                $('#posts').html(postsString);
            }
            if (result['status'] == 'error') {
                $('#messages').html(result['message']);
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
        }).done(function(result) {
            if (result['status'] == 'ok') {
                // Nothing to do
            }
            if (result['status'] == 'error') {
                $('#messages') = result['message'];
            }
        });
    }
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
        }).done(function(result) {
            if (result['status'] == 'ok') {
                var threads = result['threads'];
                var threadsString = $('#threads').html();

                for (var thread in threads) {
                    var link = '/' + board_prefix + '/' + threads[thread].id + '/';
                    threadsString += '<p><a href="' + link + '">' + threads[thread].title + '</a></p>';
                }
                if (threads.length > 0) last_thread_id = threads[threads.length - 1].id;
                $('#threads').html(threadsString);
            }
            if (result['status'] == 'error') {
                $('messages').html(result['message']);
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
        }).done(function(result) {
            if (result['status'] == 'ok') {
                window.location.replace(result['url']);
            }
            if (result['status'] == 'error') {
                $('messages') = result['message'];
            }
        });
    }
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
