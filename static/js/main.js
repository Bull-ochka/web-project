var urlpath = new URL(window.location.href).pathname;
var paths = urlpath.split('/');
var board_prefix = paths[1];
var thread_id = paths[2];

var update_posts = function() {
    $.ajax({
        url: '/api/board/' + board_prefix + '/thread/' + thread_id,
        method: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            'message': $('#message').val()
        }, null, '\t'),
    }).done(function(result) {
        var postsString = '';
        for (var post in result) {
            postsString += '<br><h5><p>' + result[post].datetime + ': ' + result[post].message + '</p></h5>'
        }
        $('#posts').html(postsString);
    });
    $('#message').val('');
}

$('#asd').click(update_posts)
