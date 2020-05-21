function isWhitespace(str) {
    return /^\s*$/.test(str);
}

var edit = false;
var edit_post_id = 0;

var changeSendBtnFunction = function(isEdit, post_id) {
    edit = isEdit;
    edit_post_id = post_id;
    if (edit) {
        var post = $('#posts h5[post_id=' + post_id + ']');
        var message = $(post).children('p').html();
        $('#threadmessage').val(message);
    }
}

var sendMsg = function() {
    // Даша, начни использовать jQuery, а не дефолтный JS
    var message = $('#threadmessage').val();

    var empty = isWhitespace(message);
    if (empty) {
        alert('Не допускается ввод пустого сообщения');
        return false;
    }
    if (edit)  {
        editPost(edit_post_id, message);
        edit = false;
    } else {
        update_posts(message);
    }
    $('#threadmessage').val('');
}

var addPost = function(post_id, message, bEdit, datetime) {
    var postString;

    edit = '';
    if (bEdit) {
        edit = '<a onclick="changeSendBtnFunction(true, ' + post_id + ')">Редактировать</a>';
    }
    postString = '<h5 post_id="' + post_id + '"><span>' + datetime + ': </span><p>' + message + '</p>' + edit + '</h5>';

    $('#posts').append(postString);
}

// Изменает содержимое поста на стороне клиента
var updatePost = function(post_id, message, datetime=undefined) {
    var post = $('#posts h5[post_id=' + post_id + ']');
    if (post == undefined) {
        return;
    }

    $(post).children('p').html(message);
    if (datetime != undefined) {
        $(post).children('span').html(datetime + ': ');
    }
}

// Отправляет изменения на сервер
var editPost = function(post_id, message) {
    var ajax = $.ajax({
        url: '/api/edit/post/' + post_id,
        method: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            'message': message
        }, null, '\t')
    }).done(function(result) {
        if (result['status'] == 'ok') {
            updatePost(post_id, message);
        }
    });
}

var createThreadFunc = function() {
    var title = $('#threadName').val();
    var message = $('#firestThreadMessage').val();

    if(isWhitespace(title) || isWhitespace(message)) {
        alert('Введите название треда и первое сообщение');
        return false;
    }
}

$('#thread_send_mes').click(sendMsg);
