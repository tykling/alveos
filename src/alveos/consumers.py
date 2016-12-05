from channels import Channel
from channels.sessions import channel_and_http_session, http_session 
import json, irc3, asyncio, os
from django.db import connection
from django.core.management import call_command


# Connected to websocket.connect
@channel_and_http_session
def ws_connect(message):
    # save the name of the reply channel for this websocket session in the django http session
    message.http_session['reply_channel'] = message.reply_channel.name

    # close DB connection before forking
    connection.close()
    new_pid = os.fork()
    if not new_pid:
        # Inside the forked process, run the irc worker
        call_command('irc', session_key=message.http_session.session_key)


# Connected to websocket.receive
@channel_and_http_session
def ws_message(message):
    if not message.http_session:
        print("No http_session found in message, bailing out")
        return

    # Parse incoming json message
    try:
        payload = json.loads(message.content['text'])
    except ValueError:
        print("Unable to parse json of incoming message :(")
        print(message.content['text'])
        return

    # TODO: Handle commands (stuff beginning with a /) here, for now just pass everything to the irc worker
    channelname = 'irc-worker-%s' % message.http_session.session_key
    Channel(channelname).send(payload)


# Connected to websocket.disconnect
@channel_and_http_session
def ws_disconnect(message):
    print("the websocket for session %s was disconnected, sending kill command to the irc worker" % message.http_session.session_key)
    channelname = 'to-ircbot-%s' % message.http_session.session_key
    Channel(channelname).send({
        'text': {
            'alveos_type': 'alveos_worker_command',
            'alveos_version': 'alveos_v1',
            'payload': {
                'command': 'die',
                'reason': 'websocket disconnected'
            }
        }
    })
    # the reply channel is no longer needed
    del message.http_session['reply_channel']


