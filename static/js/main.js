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

$('#asd').click(function() {
    var message = $('#message').val();
    update_posts(message);
    $('#message').val('');
})

setInterval(update_posts, 3000, '')
