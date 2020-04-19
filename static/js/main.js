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
});

var createThreadFunc = function() {
    var title = $('#threadName').val();
    var message = $('#firestThreadMessage').val();

    if(isWhitespace(title) || isWhitespace(message)) {
        alert('Введите название треда и первое сообщение');
        return false;
    }
}
