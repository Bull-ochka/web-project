var urlpath = new URL(window.location.href).pathname;
var paths = urlpath.split('/');
var board_prefix = paths[1];
var thread_id = paths[2];

var update_posts = function(message) {
    var ajax;

    if (message == '') {
        ajax = $.ajax({
            url: '/api/board/' + board_prefix + '/thread/' + thread_id,
            method: 'GET'
        });
    }
    else {
        ajax = $.ajax({
            url: '/api/board/' + board_prefix + '/thread/' + thread_id,
            method: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'message': message
            }, null, '\t')
        });
    }

    ajax.done(function(result) {
        var postsString = '';
        for (var post in result) {
            postsString += '<br><h5><p>' + result[post].datetime + ': ' + result[post].message + '</p></h5>'
        }
        $('#posts').html(postsString);
    });
}

var update_threads = function(title, message) {
    var ajax;

    if (message == '') {
        ajax = $.ajax({
            url: '/api/board/' + board_prefix,
            method: 'GET'
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
        var threadsString = '';
        for (var post in result) {
            var link = '/' + board_prefix + '/' + result[post].id + '/';
            threadsString += '<p><a href="' + link + '">' + result[post].title + '</a></p>'
        }
        $('#threads').html(threadsString);
    });
}

$('#sendBtn').click(function() {
    var message = $('#message').val();
    update_posts(message);
    $('#message').val('');
});


if (board_prefix != '') {
    if (thread_id != '') {
        setInterval(update_posts, 3000, '')
    }
    else {
        setInterval(update_threads, 10000, '', '')
    }
}
