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


function isWhitespace(str) {
  return /^\s*$/.test(str);
}

$('#thread_send_mes').click(function() {
    var message = document.querySelector('#threadmessage').value;

    var empty = isWhitespace(message);
    if(empty){
        alert('Не допускается ввод пустого сообщения');
        return false;
    }
    else {
        update_posts(message);
        $('#threadmessage').val('');
    }
})

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

$('#create_thread').click(function() {
    var title = document.querySelector('#threadName').value;
    var message = document.querySelector('#firstThreadMessage').value;

    if(isWhitespace(title) || isWhitespace(message)){
        alert('Введите название треда и первое сообщение');
        return false;
    }
    else {
        update_threads(title, message);
        $('#threadName').val('');
        $('#firstThreadMessage').val('');
    }
})

if (board_prefix != '') {
    if (thread_id != '') {
        setInterval(update_posts, 3000, '')
    }
    else {
        setInterval(update_threads, 10000, '', '')
    }
}
