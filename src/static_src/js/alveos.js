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
        targetwindow = $( "div#chatdiv > div > ul > li.active > a" ).text();
        var sendObj = {text: {type: 'irc_message', target: targetwindow, message: input}};
        socket.send(JSON.stringify(sendObj));
        console.log("sent over WS: " + JSON.stringify(sendObj));

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

function ShowMessage(message, tab, style="") {
    console.log("going to show message in tab " + tab + ": " + message);
    message = message.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    now = new Date($.now());
    $( "div #chatdiv > div > div.tab-content > div.tab-pane#" + tab + " > table" ).append( "<tr><td class='" + style + "'>" + now + ": " + message + "</td></tr>" );
}

// message handler
function HandleMessage(message) {
    console.log("received message: " + message);
    try {
        messageObj = JSON.parse(message);
    } catch(err) {
        alert('error parsing json!\n' + err.message + '\n' + message);
        return;
    }

    if ('alveos_version' in messageObj && messageObj.alveos_version == 'alveos-v1') {
        // show the message
        if (messageObj.type == "irc_message") {
            switch (messageObj.payload.event) {
                case "PRIVMSG":
                    ShowMessage("<" + messageObj.payload.mask + "> " + messageObj.payload.data, tab=messageObj.payload.target.replace("#", "¤"))
                break;
                case "JOIN":
                case "PART":
                case "QUIT":
                    tabname = messageObj.payload.channel.replace("#", "¤");
                    if (messageObj.payload.event == "JOIN") {
                        // if we just joined a new channel, pop open a new tab
                        if ( ! $( "div #chatdiv > div > ul > li#li-" + tabname ).length ) {
                            $( "div #chatdiv > div > ul" ).append('<li role="presentation"><a href="#' + tabname + '" aria-controls="' + tabname + '" role="tab" data-toggle="tab" class="tabs">' + messageObj.payload.channel + '</a></li>');
                            $( "div #chatdiv > div > div.tab-content" ).append('<div role="tabpanel" class="tab-pane" id="' + tabname + '"><table class="table table-condensed table-responsive chatwindow"></table></div>');
                            $( '#' + tabname ).tab('show'); // switch to the new tab right away
                        }
                    }
                    ShowMessage(messageObj.payload.event + ": " + messageObj.payload.mask, tab=tabname, style="info")
                break;
            }
        } else if (messageObj.type == 'system_message') {
            ShowMessage(messageObj.payload.message, tab="status", style="info");
        } else {
            alert('error, unsupported message type received!\n' + message);
            return;
        }
  } else {
        alert('error, unsupported message received!\n' + message);
        return;
    }
}

// when the page is done loading ...
$( document ).ready(function() {
    ShowMessage('Welcome to Alveos!', tab="status");
    ShowMessage('Connecting websocket to alveos server...', tab="status");

    // connect the websocket
    socket = new WebSocket("ws://" + window.location.host + "/");

    // function to call every time a message is received on the WS
    socket.onmessage = function(e) {
        HandleMessage(e.data);
    }

    // when websocket is done connecting
    socket.onopen = function() {
        $( "#wsstatus" ).removeClass("alert-danger alert-info").addClass("alert-success").text("Websocket is connected");
        ShowMessage('Websocket connected!', tab="status");
    }

    // when websocket is done disconnecting
    socket.onclose = function() {
        $( "#wsstatus" ).removeClass("alert-success alert-info").addClass("alert-danger").text("Websocket has been disconnected");
        ShowMessage('Websocket has been disconnected...', tab="status");
    }

    // If the page was reloaded the socket is already open, so call onopen() manually here
    if (socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }
});

// make tabs tabbable
$('a.tabs').click(function (e) {
  e.preventDefault();
  $(this).tab('show');
});


