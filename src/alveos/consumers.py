from channels import Channel
from channels.sessions import channel_and_http_session, http_session 
import json, irc3, asyncio


# Connected to websocket.connect
@channel_and_http_session
def ws_connect(message):
    # save reply channel name in http session
    message.http_session['reply_channel'] = message.reply_channel.name
    #message.reply_channel.send({'text': 'Connected to alveos server!'})


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

    # Add the message to the channel for the irc bot handling this session
    channelname = 'to-ircbot-%s' % message.http_session.session_key
    Channel(channelname).send(payload)
    print("added incoming websocket message to channel %s" % channelname)


# Connected to websocket.disconnect
def ws_disconnect(message):
    # TODO: the websocket was disconnected, kill the irc session here
    pass


