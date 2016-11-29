// input box history handler
current_history_index=-1;
inputhistory = [];
$('#chatinput').keydown(function (e) {
    if (e.which == 13) {
        // enter pressed, get the input
        var input = $('#chatinput').val();

        // add message to inputhistory
        inputhistory.unshift($('#chatinput').val());
        $('#chatinput').val('');
        current_history_index=-1;

        // send message
        var sendObj = {text: {target: '#tyktest', message: input}};
        socket.send(JSON.stringify(sendObj));

    } else if (e.which == 38) {
        // arrow up pressed, go one item backwards in history (if possible)
        if (current_history_index < inputhistory.length-1) {
            current_history_index++;
            $('#chatinput').val(inputhistory[current_history_index]);
        }

    } else if (e.which == 40) {
        // arrow down pressed, move one item forwards in history (if possible)
        if (current_history_index > -1) {
            current_history_index--;
            $('#chatinput').val(inputhistory[current_history_index]);
        }
    }
});

// output function
function ShowMessage(message) {
    now = new Date($.now());
    line = now + ': ' + message;
    $('#chatwindow').val($('#chatwindow').val() + line + '\n');
}

// when the page is done loading ...
$( document ).ready(function() {
    ShowMessage('Connecting websocket to alveos server...');

    // connect the websocket
    socket = new WebSocket("ws://" + window.location.host + "/");

    // function to call every time a message is received on the WS
    socket.onmessage = function(e) {
        ShowMessage(e.data);
    }

    // when websocket is done connecting
    socket.onopen = function() {
        ShowMessage('Websocket connected...');
    }

    // If the page was reloaded the socket is already open, so call onopen() manually here
    if (socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }
});

