function isWhitespace(str) {
    return /^\s*$/.test(str);
}

var edit = false;

var sendMsg = function() {
    // Даша, начни использовать jQuery, а не дефолтный JS
    var message = $('#threadmessage').val();

    var empty = isWhitespace(message);
    if(empty){
        alert('Не допускается ввод пустого сообщения');
        return false;
    }
    else {
        update_posts(message);
        $('#threadmessage').val('');
    }
}

var editPost = function(post_id) {
    var message = $('#threadmessage').val();
    var post = $('#posts h5[post_id=' + post_id + ']');
    if (post == undefined) {
        return;
    }
    var ajax = $.ajax({
        url: '/api/edit/post/' + post_id,
        method: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            'message': message
        }, null, '\t')
    }).done(function(result) {
        if (result['status'] == 'ok') {
            $(post).children('p').html(message);
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
